import platform
import datetime
from enhanced_versioning import SemanticVersion, NonSemanticVersion
from dataclasses import dataclass
from typing import Optional, List, Tuple, Union
# * Локальные импорт
try:
    import SupportHandler as sh
except:
    from . import SupportHandler as sh

# ! Исключения
class NvidiaSMIError(Exception):
    """Called if there is an error parsing information from NVIDIA-SMI, usually a problem in the absence of NVIDIA Corporation"""
    def __init__(self, *args) -> None:
        if len(args) != 0:
            self.msg = " ".join([str(args) for i in args])
        else:
            self.msg = "NVIDIA-SMI couldn't find 'nvml.dll' library in your system"

    def __str__(self) -> str:
        return self.msg

# ! Инициализация
supporter = sh.Supported()

# ! Проверка поддержки системы и импорт соответвуещего парсера
if platform.system() == "Windows":
    try:
        from . import WindowsParser as Parser
    except:
        import WindowsParser as Parser
elif platform.system() == "Linux":
    try:
        from . import LinuxParser as Parser
    except:
        import LinuxParser as Parser
else:
    try:
        from . import PassParser as Parser
    except:
        import PassParser as Parser

# ! Другое
@dataclass
class Temperature:
    C: int
    F: int

@dataclass
class Language:
    id: str
    mark: str
    encoding: str

# ! Dataclasses Types Classes
@dataclass
class CPUCache:
    l2_size: int
    l3_size: int

@dataclass
class CPU:
    name: str
    model: int
    family: int
    stepping: int
    architecture: str
    bits: int
    frequency: float
    cores_count: int
    flags: List[str]
    cache: CPUCache

@dataclass
class RAMBank:
    device_location: str
    form_factor: str
    type: str
    serial_number: str
    part_number: str
    capacity: int
    frequency: int
    data_width: int

@dataclass
class GPU:
    name: str
    model: str
    company: str
    driver_version: Union[SemanticVersion, NonSemanticVersion]
    driver_date: datetime.datetime
    memory_capacity: int
    memory_type: str
    architecture: str
    availability: int

@dataclass
class NGPUStatus:
    utilization: int
    memory_total: float
    memory_used: float
    memory_free: float
    temperature: Temperature
    fan_speed: int

@dataclass
class NGPU:
    name: str
    id: int
    uuid: str
    driver_version: Union[SemanticVersion, NonSemanticVersion]
    serial_number: str
    display_active: str
    display_mode: str
    status: NGPUStatus

@dataclass
class Monitor:
    name: str
    size: Tuple[int, int]
    size_mm: Tuple[int, int]
    is_primary: bool

@dataclass
class Motherboard:
    name: str
    tag: str
    version: Optional[Union[SemanticVersion, NonSemanticVersion]]
    product: str
    serial_number: Optional[str]
    manufacturer: str
    power_on: Optional[bool]
    removable: Optional[bool]
    replaceable: Optional[bool]
    rdb: Optional[bool]
    hosting_board: Optional[bool]
    hot_swappable: Optional[bool]

@dataclass
class SMBIOS:
    version: str
    major_version: str
    minor_version: str
    present: bool

@dataclass
class BIOS:
    name: str
    manufacturer: str
    release_date: datetime.datetime
    languages: List[Language]
    current_language: Language
    is_primary: bool
    serial_number: str
    version: Union[SemanticVersion, NonSemanticVersion]
    smbios: SMBIOS
    characteristics: List[str]

@dataclass
class SoundDevice:
    name: str
    product_name: str
    manufacturer: str
    device_ids: List[str]
    pnp_device_ids: List[str]
    pms: bool

# ! Внутринние функции
def __Ft(C: int) -> int:
    """Celsius (С) to Fahrenheit (F)"""
    return int((C*(9/5))+32)

# ! Открытые функции
@supporter.add_support(["Windows", "Linux"])
def get_cpu_info() -> CPU:
    """Returns the `CPU` dataclass containing information about the CPU"""
    cpu_info = Parser.get_cpu()
    cache = CPUCache(
        cpu_info["cache"]["l2_size"],
        cpu_info["cache"]["l3_size"]
    )
    del cpu_info["cache"]
    return CPU(**cpu_info, cache=cache)

@supporter.add_support(["Windows"], [])
def get_ram_info() -> List[RAMBank]:
    """Returns a `list` with `RAMBank` dataclasses containing information about each RAM die"""
    return [RAMBank(**bank) for bank in Parser.get_ram()]

@supporter.add_support(["Windows"], [])
def get_gpu_info() -> List[GPU]:
    """Returns a `list` with `GPU` dataclasses containing information about each video card"""
    gpus = []
    for info in Parser.get_videocards():
        if info["driver_version"] is not None:
            try:
                info["driver_version"] = SemanticVersion(info["driver_version"].replace(" ", ""))
            except:
                try:
                    info["driver_version"] = NonSemanticVersion(info["driver_version"].replace(" ", ""))
                except:
                    pass
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
    if info["version"] is not None:
        info["version"] = info["version"].replace(" ", "")
        try:
            info["version"] = SemanticVersion(info["version"])
        except:
            try:
                info["version"] = NonSemanticVersion(info["version"])
            except:
                pass
    return Motherboard(**info)

@supporter.add_support(["Windows"])
def get_bios_info() -> BIOS:
    """Returns the `BIOS` dataclass, containing information about the BIOS"""
    info = Parser.get_bios()
    smbios = SMBIOS(
        info["smbios_version"],
        info["smbios_major_version"],
        info["smbios_minor_version"],
        info["smbios_present"]
    )
    del info["smbios_version"], info["smbios_major_version"], info["smbios_minor_version"], info["smbios_present"]
    try:
        info["languages"] = [Language(*i) for i in info["languages"]]
        info["current_language"] = Language(*info["current_language"])
    except:
        info["languages"] = None
        info["current_language"] = None
    if info["version"] is not None:
        info["version"] = info["version"].replace(" ", "")
        try:
            info["version"] = SemanticVersion(info["version"])
        except:
            try:
                info["version"] = NonSemanticVersion(info["version"])
            except:
                pass
    return BIOS(**info, smbios=smbios)

@supporter.add_support(["Windows"], [])
def get_ngpu_info() -> List[NGPU]:
    """Returns the `NGPU` dataclass, containing video card information (ONLY FOR NVIDIA VIDEO CARDS)"""
    ngpus: List[NGPU] = []
    try:
        for i in Parser.get_nvidia_videocards():
            i["status"]["temperature"] = Temperature(i["status"]["temperature"], __Ft(i["status"]["temperature"]))
            i["status"] = NGPUStatus(**i["status"])
            if i["driver_version"] is not None:
                try:
                    i["driver_version"] = SemanticVersion(i["driver_version"].replace(" ", ""))
                except:
                    try:
                        i["driver_version"] = NonSemanticVersion(i["driver_version"].replace(" ", ""))
                    except:
                        pass
            ngpus.append(NGPU(**i))
    except Parser.subprocess.CalledProcessError:
        raise NvidiaSMIError()
    return ngpus

@supporter.add_support(["Windows"], [], errors="view")
def get_sound_device_info() -> List[SoundDevice]:
    return [SoundDevice(**i) for i in Parser.get_sound_device()]