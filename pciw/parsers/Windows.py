import os
import sys
import glob
import cpuinfo
import platform
import screeninfo
import subprocess
from dateutil import parser
from datetime import datetime
# > Typing
from typing import Any, List, Tuple, Optional, Dict, Union
# > Local Imports
from .Base import BaseParser
from ..exceptions import NSMINotFoundError
from ..units import WindowsTypes, NONE_VALUES
from ..functions import from_csv, to_bool, to_int, replaces, sn, removes, oround, aripti
from ..models import BIOS, NGPU, SMBIOS, CPU, CPUCache, Motherboard, RAMBank, Monitor, GPU, Version, Language, NGPU, NGPUStatus, Temperature

# ! Vars
NSMI_POSSIBLE_PATHS = [
    "{sd}\\Windows\\System32\\DriverStore\\FileRepository\\*\\nvidia-smi.exe",
    "{sd}\\Program Files\\NVIDIA Corporation\\NVSMI\\*\\nvidia-smi.exe"
]

# ! Call Functions
def wmic(*args: str, **kwargs: str) -> str:
    return subprocess.check_output(["wmic", *args, *[f"/{i}:{kwargs[i]}" for i in kwargs]]).decode(errors="ignore")

# ! Get Functions
def get_mff(code: int) -> str:
    return WindowsTypes.MEMORY_FORM_FACTOR.get(code, None)

def get_mtype(code: int) -> str:
    return WindowsTypes.MEMORY_TYPE.get(code, None)

def get_vmtype(code: int) -> str:
    return WindowsTypes.VIDEO_MEMORY_TYPE.get(code, None)

def get_varch(code: int) -> str:
    return WindowsTypes.VIDEO_ARCHITECTURE.get(code, None)

def get_vaval(code: int) -> str:
    return WindowsTypes.VIDEO_ALAILABILITY.get(code, None)

# ! Spetific Functions
def chrct(code: int) -> str:
    bios_char = WindowsTypes.BIOS_CHARACTERISTICS.get(code, None)
    if bios_char is not None:
        bios_char = bios_char.format(code=code)
    else:
        bios_char = f"<UNKNOWN{code}>"
    return bios_char

def tnvv(value: Optional[str]) -> Optional[str]:
    if value is not None:
        if value.lower().replace(" ", "") in NONE_VALUES:
            return None
    return value

def get_nv_actiovitions(code: Optional[str]) -> Optional[bool]:
    if code is not None:
        if code == "Enabled":
            return True
        elif code == "Disabled":
            return False

# ! Windows Spetific Functions
def windate_to_datetime(string: str) -> Optional[datetime]:
    try:
        return parser.parse(
            "{year}.{month}.{day} {hour}:{min}.{sec}"\
            .format(
                year=string[0:4],
                month=string[4:6],
                day=string[6:8],
                hour=string[8:10],
                min=string[10:12],
                sec=string[12:14]
            )
        )
    except: pass

def winlang_to_tuple(string: Union[List[str], str], *, string_sep=";") -> Optional[Union[List[Tuple[str, str, str]], Tuple[str, str, str]]]:
    try:
        if isinstance(string, list):
            return [tuple(i.split("|")) for i in string]
        elif isinstance(string, str):
            return tuple(string.split("|"))
    except: pass

# ! Main Class
class WindowsParser(BaseParser):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.system_drive = os.getenv("SystemDrive")
        self.nvidia_smi = "nvidia-smi.exe"
        
        for possible_path in NSMI_POSSIBLE_PATHS:
            gwnsmi = glob.glob(possible_path.format(sd=self.system_drive), recursive=True)
            if len(gwnsmi) != 0:
                self.nvidia_smi = gwnsmi[0]
                break
    
    @staticmethod
    def is_supported() -> bool:
        return platform.system() == 'Windows'
    
    def nsmi(self, *args: str, **kwargs: str) -> str:
        try:
            return subprocess.check_output([self.nvidia_smi, *args, *[f"{i}={kwargs[i]}" for i in kwargs]]).decode(errors="ignore")
        except:
            raise NSMINotFoundError()
    
    def get_cpu(self, *args, **kwargs) -> CPU:
        info: Dict[str, Any] = cpuinfo.get_cpu_info()
        frequency = round(info.get("hz_advertised", [0])[0] / 1e9, 1)
        return CPU(
            info.get("brand_raw", None),
            info.get("model", None),
            info.get("family", None),
            info.get("stepping", None),
            info.get("arch", None),
            info.get("bits", None),
            frequency,
            info.get("count", None),
            CPUCache(
                info.get("l2_cache_size", None),
                info.get("l3_cache_size", None)
            ),
            [i.upper() for i in info.get("flags", [])]
        )
    
    def get_ram(self, *args, **kwargs) -> List[RAMBank]:
        d, out = from_csv(wmic("MEMORYCHIP", "LIST", FORMAT="CSV")[3:-3]), []
        for i in d:
            out.append(
                RAMBank(
                    i.get("DeviceLocator", None),
                    get_mff(to_int(i.get("FormFactor", None))),
                    get_mtype(to_int(i.get("MemoryType", None))),
                    sn(tnvv(i.get("SerialNumber", None))),
                    replaces(i.get("PartNumber", None), {" ": ""}),
                    to_int(i.get("Capacity", None)),
                    to_int(i.get("Speed", None)),
                    to_int(i.get("DataWidth", None))
                )
            )
        return out
    
    def get_monitors(self, *args, **kwargs) -> List[Monitor]:
        return [
            Monitor(
                replaces(i.name, {"\\": "", ".": ""}),
                (i.width, i.height),
                (i.width_mm, i.height),
                i.is_primary
            ) for i in screeninfo.get_monitors()
        ]
    
    def get_videocards(self, *args, **kwargs) -> List[GPU]:
        d, out = from_csv(
            wmic(
                "path",
                "win32_VideoController",
                "GET",
                "Name,VideoProcessor,AdapterRAM,Availability,AdapterCompatibility,VideoArchitecture,VideoMemoryType,DriverDate,DriverVersion",
                FORMAT="CSV"
            )[3:-3]
        ), []
        for i in d:
            out.append(
                GPU(
                    i.get("Name", None),
                    i.get("VideoProcessor", None),
                    i.get("AdapterCompatibility", None),
                    Version(i.get("DriverVersion", None)),
                    windate_to_datetime(i.get("DriverDate", None)),
                    to_int(i.get("AdapterRAM", None)),
                    get_vmtype(to_int(i.get("VideoMemoryType", None))),
                    get_varch(to_int(i.get("VideoArchitecture", None))),
                    get_vaval(to_int(i.get("Availability", None)))
                )
            )
        return out
    
    def get_motherboard(self, *args, **kwargs) -> Motherboard:
        info = from_csv(
            wmic(
                "BASEBOARD",
                "GET",
                "Name,PoweredOn,Product,Removable,Replaceable,RequiresDaughterBoard,SerialNumber,Tag,Version,HostingBoard,HotSwappable,Manufacturer",
                FORMAT="CSV"
            )[3:-3]
        )[0]
        return Motherboard(
            info.get("Name", None),
            info.get("Tag", None),
            Version(info.get("Version", None)),
            info.get("Product", None),
            sn(tnvv(info.get("SerialNumber", None))),
            info.get("Manufacturer", None),
            to_bool(info.get("PoweredOn", None)),
            to_bool(info.get("Removable", None)),
            to_bool(info.get("Replaceable", None)),
            to_bool(info.get("RequiresDaughterBoard", None)),
            to_bool(info.get("HostingBoard", None)),
            to_bool(info.get("HotSwappable", None))
        )
    
    def get_bios(self, *args, **kwargs) -> BIOS:
        info = from_csv(wmic("BIOS", "LIST", FORMAT="csv")[3:-3])[0]
        try:
            langs = winlang_to_tuple(removes(replaces(info.get("ListOfLanguages", ""), {";": ",", "{": "", "}": "", "\"": ""}).split(","), [""]))
        except:
            langs = []
        try:
            clang = winlang_to_tuple(info.get("CurrentLanguage", ""))
        except:
            clang = None
        try:
            characteristics = [chrct(int(i)) for i in eval(info.get("BiosCharacteristics", "{}").replace(";", ","))]
        except:
            characteristics = []
        return BIOS(
            info.get("Name", None),
            info.get("Manufacturer", None),
            windate_to_datetime(info.get("ReleaseDate", None)),
            [Language(*i) for i in langs],
            Language(*clang),
            to_bool(info.get("PrimaryBIOS", None)),
            sn(tnvv(info.get("SerialNumber", None))),
            Version(info.get("Version", None)),
            SMBIOS(
                Version(
                    "{}.{}.{}".format(
                        info.get("SMBIOSMajorVersion", "0"),
                        info.get("SMBIOSMinorVersion", "0"),
                        info.get("SMBIOSBIOSVersion", "0")
                    )
                ),
                to_bool(info.get("SMBIOSPresent", None)),
            ),
            characteristics
        )
    
    def get_nvidia_videocards_nsmi(self) -> List[NGPU]:
        d, out = from_csv(
            self.nsmi(
                "--query-gpu=index,uuid,utilization.gpu,utilization.memory,utilization.encoder,utilization.decoder,utilization.jpeg,utilization.ofa,driver_version,name,gpu_serial,display_active,display_mode,memory.total,memory.used,memory.free,temperature.gpu,fan.speed,power.draw,power.max_limit,clocks.gr,clocks.mem,clocks.sm,clocks.max.gr,clocks.max.mem,clocks.max.sm",
                "--format=csv,noheader,nounits"
            ),
            header=[
                'index', 'uuid', 'utilization.gpu',
                'utilization.memory', 'utilization.encoder',
                'utilization.decoder', 'utilization.jpeg',
                'utilization.ofa', 'driver_version', 'name',
                'gpu_serial', 'display_active', 'display_mode',
                'memory.total', 'memory.used', 'memory.free',
                'temperature.gpu', 'fan.speed',
                'power.draw', 'power.max_limit', 
                'clocks.graphics', 'clocks.memory', 'clocks.sm',
                'clocks.max.graphics', 'clocks.max.memory', 'clocks.max.sm'
            ],
            sep=", ",
            end="\r\n"
        ), []
        for i in d:
            out.append(
                NGPU(
                    to_int(i.get("index", None)),
                    i.get("name", None),
                    i.get("uuid", None),
                    i.get("driver_version", None),
                    sn(tnvv(i.get("gpu_serial", None))),
                    get_nv_actiovitions(tnvv(i.get("display_active", None))),
                    get_nv_actiovitions(tnvv(i.get("display_mode", None))),
                    NGPUStatus(
                        to_int(i.get("utilization.gpu", None)),
                        to_int(i.get("utilization.memory", None)),
                        to_int(i.get("utilization.encoder", None)),
                        to_int(i.get("utilization.decoder", None)),
                        to_int(i.get("utilization.jpeg", None)),
                        to_int(i.get("utilization.ofa", None)),
                        oround(aripti(to_int(i.get("memory.total", None)), "*1048576")),
                        oround(aripti(to_int(i.get("memory.used", None)), "*1048576")),
                        oround(aripti(to_int(i.get("memory.free", None)), "*1048576")),
                        to_int(i.get("power.draw", None)),
                        to_int(i.get("power.max_limit", None)),
                        Temperature.init(to_int(i.get("temperature.gpu", None))),
                        to_int(i.get("fan.speed", None)),
                        to_int(i.get("clocks.graphics", None)),
                        to_int(i.get("clocks.memory", None)),
                        to_int(i.get("clocks.sm", None)),
                        to_int(i.get("clocks.max.graphics", None)),
                        to_int(i.get("clocks.max.memory", None)),
                        to_int(i.get("clocks.max.sm", None))
                    )
                )
            )
        return out
    
    def get_nvidia_videocards(self, *args, **kwargs) -> List[NGPU]:
        return self.get_nvidia_videocards_nsmi()
