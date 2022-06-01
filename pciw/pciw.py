from . import units
import platform
import datetime
from dataclasses import dataclass
from typing import Optional, List, Tuple, Union
# * Локальным импорт

# ! Исключения
class SystemIsNotSupportedError(Exception):
    def __init__(self, *args) -> None:
        """Called if your system is not supported by the module"""
        if args.__len__() != 0:
            self.msg = " ".join([str(i) for i in args])
        else:
            self.msg = "Your operating system is not supported"
    
    def __str__(self) -> str:
        return self.msg

# ! Проверка поддержки системы
if platform.system() not in units.SUPPORTED_SYSTEMS:
    raise SystemIsNotSupportedError()
else:
    if platform.system() == "Windows":
        try:
            from . import WindowsParser as Parser
        except:
            import WindowsParser as Parser

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
    l2_size: Optional[int]
    l3_size: Optional[int]

@dataclass
class CPU:
    name: str
    model: str
    family: str
    stepping: str
    architecture: str
    bits: int
    frequency: float
    cores_count: int
    flags: List[str]
    cache: CPUCache

@dataclass
class RAMBank:
    device_location: str
    form_factor: Optional[str]
    type: str
    serial_number: Optional[str]
    part_number: str
    capacity: int
    frequency: int
    data_width: int

@dataclass
class GPU:
    name: str
    model: str
    company: str
    driver_version: str
    driver_date: datetime.datetime
    memory_capacity: int
    memory_type: Optional[str]
    architecture: Optional[str]
    availability: Optional[int]

@dataclass
class NGPU:
    name: str
    id: int
    uuid: str
    ugpu: Optional[str]
    driver_version: Optional[str]
    serial_number: Optional[str]
    display_active: Optional[str]
    display_mode: Optional[str]

@dataclass
class NGPUStatus:
    id: int
    memory_total: float
    memory_used: float
    memory_free: float
    temperature: Temperature
    fan_speed: int

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
    version: str
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
    present: Optional[bool]

@dataclass
class BIOS:
    name: str
    manufacturer: str
    release_date: datetime.datetime
    languages: List[Language]
    current_language: Language
    is_primary: Optional[bool]
    serial_number: Optional[str]
    version: str
    smbios: SMBIOS

# ! Внутринние функции
def __Ft(C: int) -> int:
    return int((C*(9/5))+32)

# ! Открытые функции
def get_cpu_info() -> CPU:
    """Returns the `CPU` dataclass containing information about the CPU"""
    cpu_info = Parser.get_cpu()
    cache = CPUCache(
        cpu_info["cache"]["l2_size"],
        cpu_info["cache"]["l3_size"]
    )
    del cpu_info["cache"]
    return CPU(**cpu_info, cache=cache)

def get_ram_info() -> List[RAMBank]:
    """Returns a `list` with `RAMBank` dataclasses containing information about each RAM die"""
    return [RAMBank(**bank) for bank in Parser.get_ram()]

def get_gpu_info() -> List[GPU]:
    """Returns a `list` with `GPU` dataclasses containing information about each video card"""
    return [GPU(**va) for va in Parser.get_videocards()]

def get_monitors_info() -> List[Monitor]:
    """Returns a `list` with `Monitor` dataclasses, containing information about each monitor"""
    return [Monitor(**monitor) for monitor in Parser.get_monitors()]

def get_motherboard_info() -> Motherboard:
    """Returns the dataclass `Motherboard`, containing information about the motherboard"""
    info = Parser.get_motherboard()
    return Motherboard(**info)

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
    return BIOS(**info, smbios=smbios)

if units.NVIDIA_SMI_PATH is not None:
    def get_ngpu_info() -> List[NGPU]:
        """Returns the `NGPU` dataclass, containing video card information (ONLY FOR NVIDIA VIDEO CARDS)"""
        return [NGPU(**ngpu) for ngpu in Parser.get_nvidia_videocards()]

    def get_ngpu_status(id: Optional[int]=None) -> Optional[Union[List[NGPUStatus], NGPUStatus]]:
        """Returns the `NGPUStatus` dataclass, containing data about the status of the video cards (ONLY FOR NVIDIA VIDEO CARDS)"""
        statuses = []
        for i in Parser.get_nvidia_videocards_status():
            i["temperature"] = Temperature(i["temperature"], __Ft(i["temperature"]))
            statuses.append(NGPUStatus(**i))

        if id is not None:
            for i in statuses:
                if i.id == id:
                    return i
        else:
            return statuses
