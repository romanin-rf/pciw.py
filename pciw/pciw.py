import platform
from typing import Literal, Optional, List
# * Локальные импорт
from .Types import *
from . import SupportHandler as sh

# ! Исключения
class NvidiaSMIError(Exception):
    """Called if there is an error parsing information from NVIDIA-SMI, usually a problem in the absence of NVIDIA Corporation"""
    def __init__(self, *args) -> None:
        if len(args) != 0: self.msg = " ".join([str(i) for i in args])
        else: self.msg = "NVIDIA-SMI couldn't find 'nvml.dll' library in your system"

    def __str__(self) -> str: return self.msg

# ! Инициализация
supporter = sh.Supported()

# ! Проверка поддержки системы и импорт соответвуещего парсера
if platform.system() == "Windows":
    try: from . import WindowsParser as Parser
    except: pass
elif platform.system() == "Linux":
    try: from . import LinuxParser as Parser
    except: pass
else:
    try: from . import PassParser as Parser
    except: pass

# ! Внутринние функции
def __Ft(C: int) -> int:
    """Celsius (`С`) `to` Fahrenheit (`F`)"""
    return int((C*(9/5))+32)

def __Ct(F: int) -> int:
    """Fahrenheit (`F`) `to` Celsius (`С`)"""
    return int((F-32)/1.8)

def __gt(value: int, tp: Optional[Literal["C", "F"]]=None) -> Optional[Temperature]:
    tp = tp or "C"
    try:
        if tp == "C": return Temperature(value, __Ft(value))
        elif tp == "F": return Temperature(__Ct(value), value)
    except: pass

def _gV(version: Optional[str]) -> Optional[Version]:
    if version is not None: return Version(version.replace(" ", ""))

# ! Открытые функции
@supporter.add_support(["Windows", "Linux"])
def get_cpu_info() -> CPU:
    """Returns the `CPU` dataclass containing information about the CPU"""
    cpu_info = Parser.get_cpu()
    cache = CPUCache(cpu_info["cache"]["l2_size"], cpu_info["cache"]["l3_size"])
    del cpu_info["cache"]
    return CPU(**cpu_info, cache=cache)

@supporter.add_support(["Windows"])
def get_cpu_status(is_admin: bool=False) -> CPUStatus:
    """
    Returns dataclass `CPUStatus` containing the CPU status.
    """
    d, c = Parser.get_cpu_status(is_admin), 0
    for i in d["cores"]:
        d["cores"][c]["temperature"] = __gt(i["temperature"])
        c += 1
    d["cores"] = [CPUCore(**i) for i in d["cores"]]
    d["package_temperature"] = __gt(d["package_temperature"], "C")
    return CPUStatus(**d)

@supporter.add_support(["Windows"], [])
def get_ram_info() -> List[RAMBank]:
    """Returns a `list` with `RAMBank` dataclasses containing information about each RAM die"""
    return [RAMBank(**bank) for bank in Parser.get_ram()]

@supporter.add_support(["Windows"], [])
def get_gpu_info() -> List[GPU]:
    """Returns a `list` with `GPU` dataclasses containing information about each video card"""
    gpus = []
    for info in Parser.get_videocards():
        info["driver_version"] = _gV(info["driver_version"])
        if info["availability"] is not None:
            info["availability"] = info["availability"].upper()
        gpus.append(GPU(**info))
    return gpus

@supporter.add_support(["Windows"], [])
def get_monitors_info() -> List[Monitor]:
    """Returns a `list` with `Monitor` dataclasses, containing information about each monitor"""
    return [Monitor(**monitor) for monitor in Parser.get_monitors()]

@supporter.add_support(["Windows"])
def get_motherboard_info() -> Motherboard:
    """Returns the dataclass `Motherboard`, containing information about the motherboard"""
    info = Parser.get_motherboard()
    info["version"] = _gV(info["version"])
    return Motherboard(**info)

@supporter.add_support(["Windows"])
def get_bios_info() -> BIOS:
    """Returns the `BIOS` dataclass, containing information about the BIOS"""
    info = Parser.get_bios()
    try: smbios_version = Version(".".join([info["smbios_major_version"], info["smbios_minor_version"], info["smbios_version"]]))
    except: smbios_version = None
    smbios = SMBIOS(
        smbios_version,
        info["smbios_present"]
    )
    del info["smbios_version"], info["smbios_major_version"], info["smbios_minor_version"], info["smbios_present"]
    try:
        info["languages"] = [Language(*i) for i in info["languages"]]
        info["current_language"] = Language(*info["current_language"])
    except:
        info["languages"] = None
        info["current_language"] = None
    info["version"] = _gV(info["version"])
    return BIOS(**info, smbios=smbios)

@supporter.add_support(["Windows", "Linux"], [])
def get_ngpu_info(priority: Literal['nsmi', 'nvml']='nsmi') -> List[NGPU]:
    """Returns the `NGPU` dataclass, containing video card information (ONLY FOR NVIDIA VIDEO CARDS)"""
    ngpus: List[NGPU] = []
    try:
        for i in Parser.get_nvidia_videocards(priority):
            i["status"]["temperature"] = __gt(i["status"]["temperature"], "C")
            i["status"] = NGPUStatus(**i["status"])
            i["driver_version"] = _gV(i["driver_version"])
            ngpus.append(NGPU(**i))
    except Parser.subprocess.CalledProcessError:
        raise NvidiaSMIError()
    return ngpus