import subprocess
import cpuinfo
from typing import Union, Any, List, Optional, Literal, Tuple, Dict
# Local Import's
from . import conv
from . import units

# ! REQs
def wmic(*args: str, **kwargs: str) -> str:
    return subprocess.check_output(["wmic", *args, *[f"/{i}:{kwargs[i]}" for i in kwargs]]).decode(errors="ignore")

# ! Функции определения
def get_mff(code: int) -> str: return units.NT.MEMORY_FORM_FACTOR.get(code, None)
def get_mtype(code: int) -> str: return units.NT.MEMORY_TYPE.get(code, None)
def get_vmtype(code: int) -> str: return units.NT.VIDEO_MEMORY_TYPE.get(code, None)
def get_varch(code: int) -> str: return units.NT.VIDEO_ARCHITECTURE.get(code, None)
def get_vaval(code: int) -> str: return units.NT.VIDEO_ALAILABILITY.get(code, None)
def chrct(code: int) -> str: return units.NT.BIOS_CHARACTERISTICS.get(code, None)
def tnvv(value: Optional[str]) -> str:
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

# ! Parsers
def get_cpu() -> Dict[str, Any]:
    info = dict(cpuinfo.get_cpu_info())
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
            "l2_size": info.get("l2_cache_size", None),
            "l3_size": info.get("l3_cache_size", None)
        },
        "flags": [i.upper() for i in info.get("flags", [])]
    }

def get_ram() -> List[Dict[str, Any]]:
    d, out = conv.from_csv(wmic("MEMORYCHIP", "LIST", FORMAT="CSV")), []
    for i in d:
        out.append(
            {
                "device_location": i.get("DeviceLocator", None),
                "form_factor": get_mff(conv.str_to_int(i.get("FormFactor", None))),
                "type": get_mtype(conv.str_to_int(i.get("MemoryType", None))),
                "serial_number": conv.sn(i.get("SerialNumber", None)),
                "part_number": conv.replaces(i.get("PartNumber", None), {" ": ""}),
                "capacity": conv.str_to_int(i.get("Capacity", None)),
                "frequency": conv.str_to_int(i.get("Speed", None)),
                "data_width": conv.str_to_int(i.get("DataWidth", None))
            }
        )
    return out