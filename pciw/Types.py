import datetime
from dataclasses import dataclass
from typing import List, Union, Tuple, Optional
from enhanced_versioning import SemanticVersion, NonSemanticVersion

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