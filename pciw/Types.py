import datetime
from dataclasses import dataclass
from typing import List, Tuple

# ! MO
class Version:
    def __init__(self, version: str) -> None:
        self.__version = version
        self.__hash = hash(self.__version)
    
    def __str__(self) -> str:
        return self.__version
    
    def __repr__(self) -> str:
        return f"Version('{self.__version}', {self.__hash})"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Version):
            return self.__hash == other.__hash
        return False
    
    def __ne__(self, other: object) -> bool:
        if isinstance(other, Version):
            return self.__hash != other.__hash
        return True
    
    def __lt__(self, other: object) -> bool:
        if isinstance(other, Version):
            return self.__hash < other.__hash
        return False
    
    def __le__(self, other: object) -> bool:
        if isinstance(other, Version):
            return self.__hash <= other.__hash
        return False
    
    def __gt__(self, other: object) -> bool:
        if isinstance(other, Version):
            return self.__hash > other.__hash
        return False
    
    def __ge__(self, other: object) -> bool:
        if isinstance(other, Version):
            return self.__hash >= other.__hash
        return False

# ! Other
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
    driver_version: Version
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
    driver_version: Version
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

@dataclass
class SMBIOS:
    version: Version
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
    version: Version
    smbios: SMBIOS
    characteristics: List[str]
