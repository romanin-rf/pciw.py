from . import units
import platform
import datetime
from dataclasses import dataclass
from typing import Optional, List, Tuple
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
class RAM:
    device_location: str
    form_factor: Optional[str]
    type: str
    serial_number: str
    part_number: str
    capacity: int
    frequency: int
    data_width: int

@dataclass
class VideoAdapter:
    name: str
    model: str
    company: str
    driver_version: str
    driver_date: datetime.datetime
    memory_capacity: int
    memory_type: Optional[str]
    architecture: Optional[str]

@dataclass
class Monitor:
    name: str
    size: Tuple[int, int]
    size_mm: Tuple[int, int]
    is_primary: bool

# ! Открытые функции
def get_cpu_info() -> CPU:
    cpu_info = Parser.get_cpu()
    cache = CPUCache(
        cpu_info["cache"]["l2_size"],
        cpu_info["cache"]["l3_size"]
    )
    del cpu_info["cache"]
    return CPU(**cpu_info, cache=cache)

def get_ram_info() -> List[RAM]:
    return [RAM(**bank) for bank in Parser.get_ram()]

def get_video_info() -> List[VideoAdapter]:
    return [VideoAdapter(**va) for va in Parser.get_videocards()]

def get_monitors_info() -> List[Monitor]:
    return [Monitor(**monitor) for monitor in Parser.get_monitors()]