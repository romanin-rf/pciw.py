import cpuinfo
from typing import Any, Dict
try:
    import Converter
except:
    from . import Converter

# ! Функции парсинга
def get_cpu() -> Dict[str, Any]:
    info = cpuinfo.get_cpu_info()
    return {
        "name": info["brand_raw"],
        "model": info["model"],
        "family": info["family"],
        "stepping": info["stepping"],
        "architecture": info["arch"],
        "bits": int(info["bits"]),
        "frequency": round(info["hz_actual"][0] / 1e9, 1),
        "cores_count": info["count"],
        "cache": {
            "l2_size": Converter.linux_bytes(
                Converter.exists_key("l2_cache_size", info)[1]
            ),
            "l3_size": Converter.linux_bytes(
                Converter.exists_key("l3_cache_size", info)[1]
            )
        },
        "flags": [i.upper() for i in info["flags"]]
    }
