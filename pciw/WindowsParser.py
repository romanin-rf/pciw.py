import cpuinfo
import screeninfo
import subprocess
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
                "form_factor": get_mff(conv.to_int(i.get("FormFactor", None))),
                "type": get_mtype(conv.to_int(i.get("MemoryType", None))),
                "serial_number": conv.sn(i.get("SerialNumber", None)),
                "part_number": conv.replaces(i.get("PartNumber", None), {" ": ""}),
                "capacity": conv.to_int(i.get("Capacity", None)),
                "frequency": conv.to_int(i.get("Speed", None)),
                "data_width": conv.to_int(i.get("DataWidth", None))
            }
        )
    return out

def get_monitors() -> List[Dict[str, Any]]:
    return [
        {
            "name": conv.replaces(i.name, {"\\": "", ".": ""}),
            "size": (i.width, i.height),
            "size_mm": (i.width_mm, i.height),
            "is_primary": i.is_primary
        } for i in screeninfo.get_monitors()
    ]

def get_videocards_pynvml() -> List[Dict[str, Any]]:
    pass

def get_videocards_nsmi() -> List[Dict[str, Any]]:
    pass

def get_videocards() -> List[Dict[str, Any]]:
    d, out = conv.from_csv(wmic("path", "win32_VideoController", "GET", "Name,VideoProcessor,AdapterRAM,Availability,AdapterCompatibility,VideoArchitecture,VideoMemoryType,DriverDate,DriverVersion", FORMAT="CSV")), []
    for i in d:
        ...
    return out

def get_motherboard() -> Dict[str, Any]: 
    info = conv.from_csv(wmic("BASEBOARD", "GET", "Name,PoweredOn,Product,Removable,Replaceable,RequiresDaughterBoard,SerialNumber,Tag,Version,HostingBoard,HotSwappable,Manufacturer", FORMAT="CSV"))[0]
    return {
        "name": info.get("Name", None),
        "tag": info.get("Tag", None),
        "version": info.get("Version", None),
        "product": info.get("Product", None),
        "serial_number": conv.sn(info.get("SerialNumber", None)),
        "manufacturer": info.get("Manufacturer", None),
        "power_on": conv.to_bool(info.get("PoweredOn", None)),
        "removable": conv.to_bool(info.get("Removable", None)),
        "replaceable": conv.to_bool(info.get("Replaceable", None)),
        "rdb": conv.to_bool(info.get("RequiresDaughterBoard", None)),
        "hosting_board": conv.to_bool(info.get("HostingBoard", None)),
        "hot_swappable": conv.to_bool(info.get("HotSwappable", None))
    }

def get_bios() -> Dict[str, Any]:
    info = conv.from_csv(wmic("BIOS", "LIST", FORMAT="CSV"))[0]
    """
    try:
        langs = info.get("ListOfLanguages", "{}")
    except: langs = []
    try: clang = info.get("")
    try: characteristics = list([chrct(i) for i in eval(info.get("BiosCharacteristics", "[]")).replace(";", ",")])
    except: pass
    
    return {
        "name": ek("Name", info)[1],
        "manufacturer": ek("Manufacturer", info)[1],
        "release_date": conv.windate_to_datetime(
            ek("ReleaseDate", info)[1]
        ),
        "languages": langs,
        "current_language": clang,
        "is_primary": conv.str_to_bool(
            ek("PrimaryBIOS", info)[1]
        ),
        "serial_number": conv.sn(
            ek("SerialNumber", info)[1]
        ),
        "version": ek("Version", info)[1],
        "smbios_version": ek("SMBIOSBIOSVersion", info)[1],
        "smbios_major_version": ek("SMBIOSMajorVersion", info)[1],
        "smbios_minor_version": ek("SMBIOSMinorVersion", info)[1],
        "smbios_present": conv.str_to_bool(
            ek("SMBIOSPresent", info)[1]
        ),
        "characteristics": characteristics
    """
