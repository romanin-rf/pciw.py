from typing import List, Optional
# > Local Import's
from ..models import CPU, CPUStatus, RAMBank, Monitor, GPU, Motherboard, BIOS, NGPU

# ! Main Class
class BaseParser:
    def __init__(self, *args, **kwargs) -> None:
        pass
    
    @staticmethod
    def is_supported() -> bool:
        return True
    
    def get_cpu(self, *args, **kwargs) -> Optional[CPU]:
        return None
    
    def get_cpu_status(self, *args, **kwargs) -> Optional[CPUStatus]:
        return None
    
    def get_ram(self, *args, **kwargs) -> List[RAMBank]:
        return []
    
    def get_monitors(self, *args, **kwargs) -> List[Monitor]:
        return []
    
    def get_videocards(self, *args, **kwargs) -> List[GPU]:
        return []
    
    def get_motherboard(self, *args, **kwargs) -> Optional[Motherboard]:
        return None
    
    def get_bios(self, *args, **kwargs) -> Optional[BIOS]:
        return None
    
    def get_nvidia_videocards(self, *args, **kwargs) -> List[NGPU]:
        return []
