from datetime import datetime
from dataclasses import dataclass
from typing import List, Literal, Tuple, Optional

# ! Custom Models
class Version:
    def __init__(self, version: str) -> None:
        self.__version, self.__hash = version, hash(version)

    def __str__(self) -> str: return self.__version
    def __repr__(self) -> str: return f"{self.__class__.__name__}({repr(self.__version)}, {self.__hash})"
    def __eq__(self, other: object) -> bool: return self.__hash == other.__hash if isinstance(other, Version) else False
    def __ne__(self, other: object) -> bool: return self.__hash != other.__hash if isinstance(other, Version) else True
    def __lt__(self, other: object) -> bool: return self.__hash < other.__hash if isinstance(other, Version) else False
    def __le__(self, other: object) -> bool: return self.__hash <= other.__hash if isinstance(other, Version) else False
    def __gt__(self, other: object) -> bool: return self.__hash > other.__hash if isinstance(other, Version) else False
    def __ge__(self, other: object) -> bool: return self.__hash >= other.__hash if isinstance(other, Version) else False

# ! Units Models
@dataclass
class Temperature:
    C: float
    F: float
    K: float
    
    @staticmethod
    def init(t: Optional[float], unit: Literal['C', 'F', 'K']='C'):
        if t is not None:
            t = float(t)
            
            if unit == 'C':
                kw = dict(C=t, F=t*(9/5)+32, K=t+273.15)
            elif unit == 'F':
                kw = dict(C=(t-32)*(5/9), F=t, K=(t+459.67)*(5/9))
            elif unit == 'K':
                kw = dict(C=t-273.15, F=(t*1.8)-459.67, K=t)
            else:
                kw = None
            
            if kw is not None:
                return Temperature(**kw)

@dataclass
class Language:
    id: str
    mark: str
    encoding: str

# ! CPU Models
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
class CPUCore:
    index: int
    load: float
    temperature: Temperature
    clock: float

@dataclass
class CPUStatus:
    cores: List[CPUCore]
    total_load: float
    package_temperature: Temperature
    package_power: float
    cores_power: float

# ! RAM Models
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

# ! Monitor Models
@dataclass
class Monitor:
    name: str
    size: Tuple[int, int]
    size_mm: Tuple[int, int]
    is_primary: bool

# ! GPU Models
@dataclass
class GPU:
    name: str
    model: str
    company: str
    driver_version: Version
    driver_date: datetime
    memory_capacity: int
    memory_type: str
    architecture: str
    availability: int

# ! NVIDIA GPU Models
@dataclass
class NGPUStatus:
    utilization_gpu: int
    utilization_memory: int
    utilization_encoder: int
    utilization_decoder: int
    utilization_jpeg: int
    utilization_ofa: int
    memory_total: float
    memory_used: float
    memory_free: float
    power_currect: int
    power_maximum: int
    temperature: Temperature
    fan_speed: int
    clocks_currect_graphics: int
    clocks_currect_memory: int
    clocks_currect_sm: int
    clocks_max_graphics: int
    clocks_max_memory: int
    clocks_max_sm: int

@dataclass
class NGPU:
    name: str
    id: int
    uuid: str
    driver_version: Version
    serial_number: str
    display_active: str
    display_mode: str
    status: NGPUStatus

# ! Motherboard Models
@dataclass
class Motherboard:
    name: str
    tag: str
    version: Version
    product: str
    serial_number: str
    manufacturer: str
    power_on: bool
    removable: bool
    replaceable: bool
    rdb: bool
    hosting_board: bool
    hot_swappable: bool

# ! BIOS Models
@dataclass
class SMBIOS:
    version: Version
    present: bool

@dataclass
class BIOS:
    name: str
    manufacturer: str
    release_date: datetime
    languages: List[Language]
    current_language: Language
    is_primary: bool
    serial_number: str
    version: Version
    smbios: SMBIOS
    characteristics: List[str]