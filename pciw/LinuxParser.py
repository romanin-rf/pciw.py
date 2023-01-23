import cpuinfo
import subprocess
from typing import Any, Dict, List, Optional
# Local Import's
from . import conv
from . import units

# ! REQs
def nsmi(*args: str, **kwargs: str) -> str:
    if units.NVIDIA_SMI_PATH is not None:
        try: return subprocess.check_output([units.NVIDIA_SMI_PATH, *args, *[f"{i}={kwargs[i]}" for i in kwargs]]).decode(errors="ignore")
        except: pass
    return ""

def nsmi2(*args: str) -> List[Dict[str, Any]]:
    out = []
    try:
        from pynvml.smi import nvidia_smi
        nsmi = nvidia_smi.getInstance()
        gpus = nsmi.DeviceQuery(",".join(args))
        for i in gpus["gpu"]: out.append({**i, "driver_version": gpus["driver_version"]})
    except: pass
    return out

# ! Функции определения
def tnvv(value: Optional[str]) -> Optional[str]:
    if value is not None:
        if value in units.NONE_TYPE_EXCEPTIONS:
            return None
    return value
def get_nv_actiovitions(code: Optional[str]) -> Optional[bool]:
    if code is not None:
        if code == "Enabled":
            return True
        elif code == "Disabled":
            return False

# ! Функционал
def get_cpu() -> Dict[str, Any]:
    info = dict(cpuinfo.get_cpu_info())
    try: freq = round(info.get("hz_actual", None)[0] / 1e9, 1)
    except: freq = None
    return {
        "name": info.get("brand_raw", None),
        "model": info.get("model", None),
        "family": info.get("family", None),
        "stepping": info.get("stepping", None),
        "architecture": info.get("arch", None),
        "bits": info.get("bits", None),
        "frequency": freq,
        "cores_count": info.get("count", None),
        "cache": {
            "l2_size": conv.linux_bytes(info.get("l2_cache_size", None)),
            "l3_size": conv.linux_bytes(info.get("l3_cache_size", None))
        },
        "flags": [i.upper() for i in info.get("flags", [])]
    }

def get_nvidia_videocards_pynvml() -> List[Dict[str, Any]]:
    d, out = nsmi2('index', 'uuid', 'utilization.gpu', 'driver_version', 'name', 'gpu_serial', 'display_active', 'display_mode', 'memory.total', 'memory.used', 'memory.free', 'temperature.gpu', 'fan.speed'), []
    for idx, i in enumerate(d):
        out.append(
            {
                "name": i.get("product_name", None),
                "id": idx,
                "uuid": i.get("uuid", None),
                "driver_version": i.get("driver_version", None),
                "serial_number": conv.sn(i.get("serial", None)),
                "display_active": get_nv_actiovitions(i.get("display_active", None)),
                "display_mode": get_nv_actiovitions(i.get("display_mode", None)),
                "status": {
                    "utilization": i.get("utilization", {}).get("gpu_util", None),
                    "memory_total": i.get("total", None),
                    "memory_used": i.get("used", None),
                    "memory_free": i.get("free", None),
                    "temperature": i.get("temperature", {}).get("gpu_temp", None),
                    "fan_speed": conv.to_int(i.get("fan_speed", None))
                }
            }
        )
    return out

def get_nvidia_videocards_nsmi() -> List[Dict[str, Any]]:
    d, out = conv.from_csv(
        nsmi(
            "--query-gpu=index,uuid,utilization.gpu,driver_version,name,gpu_serial,display_active,display_mode,memory.total,memory.used,memory.free,temperature.gpu,fan.speed",
            "--format=csv,noheader,nounits"
        ), 
        header=[
            "index", "uuid", "utilization.gpu",
            "driver_version", "name", "gpu_serial",
            "display_active", "display_mode", "memory.total",
            "memory.used", "memory.free", "temperature.gpu",
            "fan.speed"
        ],
        sep=", ",
        end="\n"
    ), []
    for i in d:
        out.append(
            {
                "id": conv.to_int(i.get("index", None)),
                "name": i.get("name", None),
                "uuid": i.get("uuid", None),
                "driver_version": i.get("driver_version", None),
                "serial_number": conv.sn(i.get("gpu_serial", None)),
                "display_active": tnvv(i.get("display_active", None)),
                "display_mode": tnvv(i.get("display_mode", None)),
                "status": {
                    "utilization": conv.to_int(i.get("utilization.gpu", None)),
                    "memory_total": conv.to_int(i.get("memory.total", None)),
                    "memory_used": conv.to_int(i.get("memory.used", None)),
                    "memory_free": conv.to_int(i.get("memory.free", None)),
                    "temperature": conv.to_int(i.get("temperature.gpu", None)),
                    "fan_speed": conv.to_int(i.get("fan.speed", None))
                }
            }
        )
    return out

def get_nvidia_videocards() -> List[Dict[str, Any]]:
    if len(data:=get_nvidia_videocards_nsmi()) == 0:
        data = get_nvidia_videocards_pynvml()
    return data
