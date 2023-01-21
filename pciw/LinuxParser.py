import cpuinfo
from typing import Any, Dict
from . import conv

# ! Функции парсинга
def get_cpu() -> Dict[str, Any]:
    info = cpuinfo.get_cpu_info()
    return {
        "name": info.get("brand_raw", None),
        "model": info.get("model", None),
        "family": info.get("family", None),
        "stepping": info.get("stepping", None),
        "architecture": info.get("arch", None),
        "bits": info.get(info["bits"], None),
        "frequency": round(info.get("hz_actual", 0) / 1e9, 1),
        "cores_count": info.get("count", None),
        "cache": {
            "l2_size": conv.linux_bytes(info.get("l2_cache_size", None)),
            "l3_size": conv.linux_bytes(info.get("l3_cache_size", None))
        },
        "flags": [i.upper() for i in info.get("flags", [])]
    }

