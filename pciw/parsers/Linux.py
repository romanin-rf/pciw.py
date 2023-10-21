import cpuinfo
import platform
import screeninfo
import subprocess
from typing import Dict, Any, List, Optional, Union
# > Local Imports
from .Base import BaseParser
from ..units import NONE_VALUES
from ..exceptions import NSMINotFoundError
from ..functions import to_int, oround, aripti, replaces, from_csv, sn
from ..models import CPU, CPUCache, Monitor, NGPU, NGPUStatus, Temperature

# ! Vars
LINUX_BYTES_NAMES: Dict[str, int] = {
    "KiB": 1024,
    "MiB": 1024**2,
    "GiB": 1024**3,
    "TiB": 1024**4,
}

# ! Linux Specific Functions
def linux_bytes(string: Optional[Union[str, int]]) -> Optional[int]:
    if not isinstance(string, int):
        if string is not None:
            ls = string.split(' ')
            try: return int(ls[0]) * LINUX_BYTES_NAMES[ls[1]]
            except: pass
    return string

# ! Specific Functions
def tnvv(value: Optional[str]) -> Optional[str]:
    if value is not None:
        if value.lower().replace(" ", "") in NONE_VALUES:
            return None
    return value

def get_nv_actiovitions(code: Optional[str]) -> Optional[bool]:
    if code is not None:
        if code == "Enabled":
            return True
        elif code == "Disabled":
            return False

# ! Main Class
class LinuxParser(BaseParser):
    nvidia_smi = "nvidia-smi"
    
    @staticmethod
    def is_supported() -> bool:
        return platform.system() == 'Linux'
    
    def nsmi(self, *args: str, **kwargs: str) -> str:
        try:
            return subprocess.check_output([self.nvidia_smi, *args, *[f"{i}={kwargs[i]}" for i in kwargs]]).decode(errors="ignore")
        except:
            raise NSMINotFoundError()
    
    def get_cpu(self, *args, **kwargs) -> Dict[str, Any]:
        info: Dict[str, Any] = cpuinfo.get_cpu_info()
        frequency = round(info.get("hz_advertised", [0])[0] / 1e9, 1)
        return CPU(
            info.get("brand_raw", None),
            info.get("model", None),
            info.get("family", None),
            info.get("stepping", None),
            info.get("arch", None),
            info.get("bits", None),
            frequency,
            info.get("count", None),
            CPUCache(
                linux_bytes(info.get("l2_cache_size", None)),
                linux_bytes(info.get("l3_cache_size", None))
            ),
            [i.upper() for i in info.get("flags", [])]
        )
    
    def get_monitors(self, *args, **kwargs) -> List[Monitor]:
        return [
            Monitor(
                replaces(i.name, {"\\": "", ".": ""}),
                (i.width, i.height),
                (i.width_mm, i.height),
                i.is_primary
            ) for i in screeninfo.get_monitors()
        ]
    
    def get_nvidia_videocards_nsmi(self) -> List[NGPU]:
        d, out = from_csv(
            self.nsmi(
                "--query-gpu=index,uuid,utilization.gpu,utilization.memory,utilization.encoder,utilization.decoder,utilization.jpeg,utilization.ofa,driver_version,name,gpu_serial,display_active,display_mode,memory.total,memory.used,memory.free,temperature.gpu,fan.speed,power.draw,power.max_limit,clocks.gr,clocks.mem,clocks.sm,clocks.max.gr,clocks.max.mem,clocks.max.sm",
                "--format=csv,noheader,nounits"
            ),
            header=[
                'index', 'uuid', 'utilization.gpu',
                'utilization.memory', 'utilization.encoder',
                'utilization.decoder', 'utilization.jpeg',
                'utilization.ofa', 'driver_version', 'name',
                'gpu_serial', 'display_active', 'display_mode',
                'memory.total', 'memory.used', 'memory.free',
                'temperature.gpu', 'fan.speed',
                'power.draw', 'power.max_limit', 
                'clocks.graphics', 'clocks.memory', 'clocks.sm',
                'clocks.max.graphics', 'clocks.max.memory', 'clocks.max.sm'
            ],
            sep=", ",
            end="\r\n"
        ), []
        for i in d:
            out.append(
                NGPU(
                    to_int(i.get("index", None)),
                    i.get("name", None),
                    i.get("uuid", None),
                    i.get("driver_version", None),
                    sn(tnvv(i.get("gpu_serial", None))),
                    get_nv_actiovitions(tnvv(i.get("display_active", None))),
                    get_nv_actiovitions(tnvv(i.get("display_mode", None))),
                    NGPUStatus(
                        to_int(i.get("utilization.gpu", None)),
                        to_int(i.get("utilization.memory", None)),
                        to_int(i.get("utilization.encoder", None)),
                        to_int(i.get("utilization.decoder", None)),
                        to_int(i.get("utilization.jpeg", None)),
                        to_int(i.get("utilization.ofa", None)),
                        oround(aripti(to_int(i.get("memory.total", None)), "*1048576")),
                        oround(aripti(to_int(i.get("memory.used", None)), "*1048576")),
                        oround(aripti(to_int(i.get("memory.free", None)), "*1048576")),
                        to_int(i.get("power.draw", None)),
                        to_int(i.get("power.max_limit", None)),
                        Temperature.init(to_int(i.get("temperature.gpu", None))),
                        to_int(i.get("fan.speed", None)),
                        to_int(i.get("clocks.graphics", None)),
                        to_int(i.get("clocks.memory", None)),
                        to_int(i.get("clocks.sm", None)),
                        to_int(i.get("clocks.max.graphics", None)),
                        to_int(i.get("clocks.max.memory", None)),
                        to_int(i.get("clocks.max.sm", None))
                    )
                )
            )
        return out