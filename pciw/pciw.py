from typing import List, Literal
from .parsers import __parsers__
from .exceptions import NotSupportedError
from .models import CPU, CPUStatus, GPU, NGPU, RAMBank, Monitor, Motherboard, BIOS

# ! Parser Initialization
parser_model = None
for pm in __parsers__:
    if pm.is_supported():
        parser_model = pm
        break
if parser_model is None:
    raise NotSupportedError()
parser = parser_model()

# ! Fucntions
def get_cpu_info() -> CPU:
    """Returns the `CPU` dataclass containing information about the CPU"""
    return parser.get_cpu()

def get_cpu_status() -> CPUStatus:
    """
    Returns dataclass `CPUStatus` containing the CPU status.
    """
    return parser.get_cpu_status()

def get_ram_info() -> List[RAMBank]:
    """Returns a `list` with `RAMBank` dataclasses containing information about each RAM die"""
    return parser.get_ram()

def get_gpu_info() -> List[GPU]:
    """Returns a `list` with `GPU` dataclasses containing information about each video card"""
    return parser.get_videocards()

def get_monitors_info() -> List[Monitor]:
    """Returns a `list` with `Monitor` dataclasses, containing information about each monitor"""
    return parser.get_monitors()

def get_motherboard_info() -> Motherboard:
    """Returns the dataclass `Motherboard`, containing information about the motherboard"""
    return parser.get_motherboard()

def get_bios_info() -> BIOS:
    """Returns the `BIOS` dataclass, containing information about the BIOS"""
    return parser.get_bios()

def get_ngpu_info(priority: Literal['nsmi', 'nvml']='nsmi') -> List[NGPU]:
    """Returns the `NGPU` dataclass, containing video card information (ONLY FOR NVIDIA VIDEO CARDS)"""
    return parser.get_nvidia_videocards()