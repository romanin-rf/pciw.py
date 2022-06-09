import cpuinfo
import screeninfo
import subprocess
from typing import Union, Any, List, Optional, Literal, Tuple, Dict

# ! Локальные импорты
try:
    import units
    import Converter
except:
    from . import units
    from . import Converter

# ! Функции
def ek(
    key: Union[str, int],
    data: Union[dict, list, tuple]
) -> Tuple[bool, Optional[Any]]:
    try:
        return True, data[key]
    except:
        return False, None

def removes(l: list, ldv: list) -> list:
    for value in ldv:
        for i in range(0, l.count(value)):
            l.remove(value)
    return l

def replaces(s: str, d: Dict[str, str]) -> str:
    for i in d.items():
        s = s.replace(i[0], i[1])
    return s

def startswiths(string: str, sl: List[str]) -> bool:
    for i in sl:
        if string.startswith(i):
            return True
    return False

# ! Функция запросов к WMIC
def request(
    method: str,
    treq: Optional[Literal["GET", "LIST"]]=None,
    data: Optional[Union[List[str], str]]=None,
    form: Optional[Literal["VALUE", "CSV"]]=None
) -> str:
    form = form or "VALUE"
    treq = treq or "LIST"
    if data is not None:
        req = subprocess.check_output(
            "wmic {0} {2} {1} /format:{3}"\
                .format(
                    method,
                    (",".join(data) if isinstance(data, list) else data),
                    treq,
                    form
                )
        )
    else:
        req = subprocess.check_output(f"wmic {method} {treq} /format:{form}")
    return req.decode(errors="ignore")

def request_nsmi(qgpu: List[str], form: List[str]) -> str:
    return subprocess.check_output(
        [
            units.NVIDIA_SMI_PATH,
            "--query-gpu={}".format(",".join(qgpu)),
            "--format={}".format(",".join(form))
        ]
    ).decode(errors="ignore")

# ! Функции определения
def get_mff(code: int) -> str:
    return units.NT_TYPES.MEMORY_FORM_FACTOR[code]

def get_mtype(code: int) -> str:
    return units.NT_TYPES.MEMORY_TYPE[code]

def get_vmtype(code: int) -> str:
    return units.NT_TYPES.VIDEO_MEMORY_TYPE[code]

def get_varch(code: int) -> str:
    return units.NT_TYPES.VIDEO_ARCHITECTURE[code]

def get_vaval(code: int) -> str:
    return units.NT_TYPES.VIDEO_ALAILABILITY[code]

def tnvv(value: Optional[str]) -> str:
    if value is not None:
        if value in units.NVIDIA_VALUES_EXCEPTIONS:
            return None
    return value

def chrct(code: int) -> str:
    return units.NT_TYPES.BIOS_CHARACTERISTICS[code]

# ! Get-функции
def get_cpu() -> Dict[str, Any]:
    info = cpuinfo.get_cpu_info()
    return {
        "name": info["brand_raw"],
        "model": info["model"],
        "family": info["family"],
        "stepping": info["stepping"],
        "architecture": info["arch"],
        "bits": int(info["bits"]),
        "frequency": round(info["hz_actual"][0] / 1e9, 1),
        "cores_count": info["count"],
        "cache": {
            "l2_size": ek("l2_cache_size", info)[1],
            "l3_size": ek("l3_cache_size", info)[1]
        },
        "flags": [i.upper() for i in info["flags"]]
    }

def get_ram() -> List[Dict[str, Any]]:
    ld, uld = Converter.value_to_dict(request("MEMORYCHIP")), []
    for i in ld:
        uld.append(
            {
                "device_location": i["DeviceLocator"],
                "form_factor": get_mff(Converter.str_to_int(i["FormFactor"])),
                "type": get_mtype(Converter.str_to_int(i["MemoryType"])),
                "serial_number": Converter.sn(i["SerialNumber"]),
                "part_number": i["PartNumber"].replace(" ", ""),
                "capacity": Converter.str_to_int(i["Capacity"]),
                "frequency": Converter.str_to_int(i["Speed"]),
                "data_width": Converter.str_to_int(i["DataWidth"])
            }
        )
    return uld

def get_monitors() -> List[Dict[str, Any]]:
    return [
        {
            "name": replaces(i.name, {"\\": "", ".": ""}),
            "size": (i.width, i.height),
            "size_mm": (i.width_mm, i.height),
            "is_primary": i.is_primary
        } for i in screeninfo.get_monitors()
    ]

def get_videocards() -> List[Dict[str, Any]]:
    ld, uld = Converter.value_to_dict(
        request(
            "path win32_VideoController", "GET", "Name,VideoProcessor,AdapterRAM,Availability,AdapterCompatibility,VideoArchitecture,VideoMemoryType,DriverDate,DriverVersion"
        )
    ), []
    for i in ld:
        uld.append(
            {
                "name": ek("Name", i)[1],
                "model": ek("VideoProcessor", i)[1],
                "company": ek("AdapterCompatibility", i)[1],
                "driver_version": ek("DriverVersion", i)[1],
                "driver_date": Converter.windate_to_datetime(i["DriverDate"]),
                "memory_capacity": Converter.str_to_int(ek("AdapterRAM", i)[1]),
                "memory_type": get_vmtype(Converter.str_to_int(i["VideoMemoryType"])),
                "architecture": get_varch(Converter.str_to_int(i["VideoArchitecture"])),
                "availability": get_vaval(Converter.str_to_int(i["Availability"]))
            }
        )
    return uld

def get_nvidia_videocards() -> List[Dict[str, Any]]:
    info, nvidia_videocards = \
    Converter.from_csv(
        request_nsmi(
            [
                "index",
                "uuid",
                "utilization.gpu",
                "driver_version",
                "name",
                "gpu_serial",
                "display_active",
                "display_mode",
                "memory.total",
                "memory.used",
                "memory.free",
                "temperature.gpu",
                "fan.speed"
            ],
            ["csv", "noheader", "nounits"]
        ), 
        ", ",
        "\r\n"
    ), []
    for i in info:
        nvidia_videocards.append(
            {
                "name": ek(4, i)[1],
                "id": Converter.str_to_int(
                    ek(0, i)[1]
                ),
                "uuid": ek(1, i)[1],
                "ugpu": tnvv(
                    ek(2, i)[1]
                ),
                "driver_version": ek(3, i)[1],
                "serial_number": Converter.sn(
                    tnvv(
                        ek(5, i)[1]
                    )
                ),
                "display_active": tnvv(
                    ek(6, i)[1]
                ),
                "display_mode": tnvv(
                    ek(7, i)[1]
                ),
                "status": {
                    "memory_total": Converter.str_to_int(
                        ek(8, i)[1]
                    ),
                    "memory_used": Converter.str_to_int(
                        ek(9, i)[1]
                    ),
                    "memory_free": Converter.str_to_int(
                        ek(10, i)[1]
                    ),
                    "temperature": Converter.str_to_int(
                        ek(11, i)[1]
                    ),
                    "fan_speed": Converter.str_to_int(
                        ek(12, i)[1]
                    )
                }
            }
        )
    return nvidia_videocards

def get_motherboard() -> Dict[str, Any]:
    info = Converter.value_to_dict(request(
            "BASEBOARD", "GET", "Name,PoweredOn,Product,Removable,Replaceable,RequiresDaughterBoard,SerialNumber,Tag,Version,HostingBoard,HotSwappable,Manufacturer"
        )
    )[0]
    return {
        "name": ek("Name", info)[1],
        "tag": ek("Tag", info)[1],
        "version": ek("Version", info)[1],
        "product": ek("Product", info)[1],
        "serial_number": Converter.sn(
            ek("SerialNumber", info)[1]
        ),
        "manufacturer": ek("Manufacturer", info)[1],
        "power_on": Converter.str_to_bool(
            ek("PoweredOn", info)[1]
        ),
        "removable": Converter.str_to_bool(
            ek("Removable", info)[1]
        ),
        "replaceable": Converter.str_to_bool(
            ek("Replaceable", info)[1]
        ),
        "rdb": Converter.str_to_bool(
            ek("RequiresDaughterBoard", info)[1]
        ),
        "hosting_board": Converter.str_to_bool(
            ek("HostingBoard", info)[1]
        ),
        "hot_swappable": Converter.str_to_bool(
            ek("HotSwappable", info)[1]
        )
    }

def get_bios() -> Dict[str, Any]:
    info = Converter.value_to_dict(request(
            "BIOS", "LIST", "FULL"
        )
    )[0]
    try:
        langs = Converter.winlang_to_tuple(list(eval(info["ListOfLanguages"])))
        clang = Converter.winlang_to_tuple(info["CurrentLanguage"])
    except:
        langs, clang = [], None
    try:
        characteristics = list(set([chrct(i).upper() for i in eval(ek("BiosCharacteristics", info)[1])]))
    except:
        characteristics = []
    
    return {
        "name": ek("Name", info)[1],
        "manufacturer": ek("Manufacturer", info)[1],
        "release_date": Converter.windate_to_datetime(
            ek("ReleaseDate", info)[1]
        ),
        "languages": langs,
        "current_language": clang,
        "is_primary": Converter.str_to_bool(
            ek("PrimaryBIOS", info)[1]
        ),
        "serial_number": Converter.sn(
            ek("SerialNumber", info)[1]
        ),
        "version": ek("Version", info)[1],
        "smbios_version": ek("SMBIOSBIOSVersion", info)[1],
        "smbios_major_version": ek("SMBIOSMajorVersion", info)[1],
        "smbios_minor_version": ek("SMBIOSMinorVersion", info)[1],
        "smbios_present": Converter.str_to_bool(
            ek("SMBIOSPresent", info)[1]
        ),
        "characteristics": characteristics
    }
