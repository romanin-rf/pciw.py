import os
import sys
import cpuinfo
import screeninfo
import subprocess
from typing import Any, List, Optional, Dict, Literal
# Local Import's
from . import conv
from . import units

# ! REQs
def wmic(*args: str, **kwargs: str) -> str:
    return subprocess.check_output(["wmic", *args, *[f"/{i}:{kwargs[i]}" for i in kwargs]]).decode(errors="ignore")

def nsmi(*args: str, **kwargs: str) -> str:
    if units.NVIDIA_SMI_PATH is not None:
        try:
            return subprocess.check_output([units.NVIDIA_SMI_PATH, *args, *[f"{i}={kwargs[i]}" for i in kwargs]]).decode(errors="ignore")
        except: pass
    return ""

def nsmi2(*args: str) -> List[Dict[str, Any]]:
    out = []
    try:
        from pynvml.smi import nvidia_smi
        nsmi = nvidia_smi.getInstance()
        gpus = nsmi.DeviceQuery(",".join(args))
        for i in gpus["gpu"]:
            out.append({**i, "driver_version": gpus["driver_version"]})
    except:
        pass
    return out

def tcpu() -> str:
    subprocess.check_output([sys.executable, units.T_CPU_PATH])
    with open(os.path.join(os.path.dirname(units.T_CPU_PATH), "req.log"), "rb") as file:
        return file.read().decode(errors="ignore")

def tcpu_admin() -> str:
    return subprocess.check_output([units.T_CPU_PATH_ADMIN]).decode(errors="ignore")

# ! Функции определения
def get_mff(code: int) -> str:
    return units.NT.MEMORY_FORM_FACTOR.get(code, None)

def get_mtype(code: int) -> str:
    return units.NT.MEMORY_TYPE.get(code, None)

def get_vmtype(code: int) -> str:
    return units.NT.VIDEO_MEMORY_TYPE.get(code, None)

def get_varch(code: int) -> str:
    return units.NT.VIDEO_ARCHITECTURE.get(code, None)

def get_vaval(code: int) -> str:
    return units.NT.VIDEO_ALAILABILITY.get(code, None)

def chrct(code: int) -> str:
    bios_char = units.NT.BIOS_CHARACTERISTICS.get(code, None)
    if bios_char is not None:
        bios_char = bios_char.format(code=code)
    else:
        bios_char = f"<UNKNOWN{code}>"
    return bios_char

def tnvv(value: Optional[str]) -> Optional[str]:
    if value is not None:
        if value.lower().replace(" ", "") in units.NONE_TYPE_EXCEPTIONS:
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
    try: Hz = round(info.get("hz_actual", 0)[0] / 1e9, 1)
    except: Hz = 0
    return {
        "name": info.get("brand_raw", None),
        "model": info.get("model", None),
        "family": info.get("family", None),
        "stepping": info.get("stepping", None),
        "architecture": info.get("arch", None),
        "bits": info.get("bits", None),
        "frequency": Hz,
        "cores_count": info.get("count", None),
        "cache": {
            "l2_size": info.get("l2_cache_size", None),
            "l3_size": info.get("l3_cache_size", None)
        },
        "flags": [i.upper() for i in info.get("flags", [])]
    }

def get_cpu_status(is_admin: bool=False) -> Dict[str, List[Dict[str, Any]]]:
    t_cpu_func = tcpu_admin if is_admin else tcpu
    d, out, c = conv.from_tcpu_data(t_cpu_func()), {"cores": []}, 1
    out["total_load"] = d.get("cpu.cpu_total.load")
    out["package_temperature"] = d.get("cpu.cpu_package.temperature")
    out["package_power"] = d.get("cpu.cpu_package.power")
    out["cores_power"] = d.get("cpu.cpu_cores.power")
    while True:
        if d.get(f"cpu.cpu_core_#{c}.load") is not None:
            out["cores"].append(
                {
                    "index": c,
                    "load": d.get(f"cpu.cpu_core_#{c}.load"),
                    "temperature": d.get(f"cpu.cpu_core_#{c}.temperature"),
                    "clock": d.get(f"cpu.cpu_core_#{c}.clock")
                }
            )
        else: break
        c += 1
    return out

def get_ram() -> List[Dict[str, Any]]:
    d, out = conv.from_values(wmic("MEMORYCHIP", "LIST", FORMAT="VALUE")), []
    for i in d:
        out.append(
            {
                "device_location": i.get("DeviceLocator", None),
                "form_factor": get_mff(conv.to_int(i.get("FormFactor", None))),
                "type": get_mtype(conv.to_int(i.get("MemoryType", None))),
                "serial_number": conv.sn(tnvv(i.get("SerialNumber", None))),
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

def get_nvidia_videocards_pynvml() -> List[Dict[str, Any]]:
    d, out = nsmi2(
        'index', 'uuid', 'utilization.gpu',
        'utilization.memory', 'utilization.encoder',
        'utilization.decoder', 'utilization.jpeg',
        'utilization.ofa', 'driver_version',
        'name', 'gpu_serial', 'display_active',
        'display_mode', 'memory.total',
        'memory.used', 'memory.free',
        'temperature.gpu', 'fan.speed',
        'power.draw', 'power.max_limit', 
        'clocks.gr','clocks.mem','clocks.sm',
        'clocks.max.gr','clocks.max.mem','clocks.max.sm'
    ), []
    for idx, i in enumerate(d):
        out.append(
            {
                "id": idx,
                "name": i.get("product_name", None),
                "uuid": i.get("uuid", None),
                "driver_version": i.get("driver_version", None),
                "serial_number": conv.sn(tnvv(i.get("serial", None))),
                "display_active": get_nv_actiovitions(i.get("display_active", None)),
                "display_mode": get_nv_actiovitions(i.get("display_mode", None)),
                "status": {
                    "utilization_gpu": i.get("utilization", {}).get("gpu_util", None),
                    "utilization_memory": i.get("utilization", {}).get("memory_util", None),
                    "utilization_encoder": i.get("utilization", {}).get("encoder_util", None),
                    "utilization_decoder": i.get("utilization", {}).get("decoder_util", None),
                    "utilization_jpeg": i.get("utilization", {}).get("jpeg_util", None),
                    "utilization_ofa": i.get("utilization", {}).get("ofa_util", None),
                    "memory_total": conv.oround(conv.aripti(i.get("fb_memory_usage", {}).get("total", None), "*1048576")),
                    "memory_used": conv.oround(conv.aripti(i.get("fb_memory_usage", {}).get("used", None), "*1048576")),
                    "memory_free": conv.oround(conv.aripti(i.get("fb_memory_usage", {}).get("free", None), "*1048576")),
                    "temperature": i.get("temperature", {}).get("gpu_temp", None),
                    "fan_speed": conv.to_int(i.get("fan_speed", None)),
                    "power_currect": conv.to_int(i.get("power_readings", {}).get("power_draw", None)),
                    "power_maximum": conv.to_int(i.get("power_readings", {}).get("max_power_limit", None)),
                    "clocks_currect_graphics": conv.to_int(i.get("clocks", {}).get("graphics_clock", None)),
                    "clocks_currect_memory": conv.to_int(i.get("clocks", {}).get("mem_clock", None)),
                    "clocks_currect_sm": conv.to_int(i.get("clocks", {}).get("sm_clock", None)),
                    "clocks_max_graphics": conv.to_int(i.get("max_clocks", {}).get("graphics_clock", None)),
                    "clocks_max_memory": conv.to_int(i.get("max_clocks", {}).get("mem_clock", None)),
                    "clocks_max_sm": conv.to_int(i.get("max_clocks", {}).get("sm_clock", None))
                }
            }
        )
    return out

def get_nvidia_videocards_nsmi() -> List[Dict[str, Any]]:
    d, out = conv.from_csv(
        nsmi(
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
            {
                "id": conv.to_int(i.get("index", None)),
                "name": i.get("name", None),
                "uuid": i.get("uuid", None),
                "driver_version": i.get("driver_version", None),
                "serial_number": conv.sn(tnvv(i.get("gpu_serial", None))),
                "display_active": get_nv_actiovitions(tnvv(i.get("display_active", None))),
                "display_mode": get_nv_actiovitions(tnvv(i.get("display_mode", None))),
                "status": {
                    "utilization_gpu": conv.to_int(i.get("utilization.gpu", None)),
                    "utilization_memory": conv.to_int(i.get("utilization.memory", None)),
                    "utilization_encoder": conv.to_int(i.get("utilization.encoder", None)),
                    "utilization_decoder": conv.to_int(i.get("utilization.decoder", None)),
                    "utilization_jpeg": conv.to_int(i.get("utilization.jpeg", None)),
                    "utilization_ofa": conv.to_int(i.get("utilization.ofa", None)),
                    "memory_total": conv.oround(conv.aripti(conv.to_int(i.get("memory.total", None)), "*1048576")),
                    "memory_used": conv.oround(conv.aripti(conv.to_int(i.get("memory.used", None)), "*1048576")),
                    "memory_free": conv.oround(conv.aripti(conv.to_int(i.get("memory.free", None)), "*1048576")),
                    "temperature": conv.to_int(i.get("temperature.gpu", None)),
                    "fan_speed": conv.to_int(i.get("fan.speed", None)),
                    "power_currect": conv.to_int(i.get("power.draw", None)),
                    "power_maximum": conv.to_int(i.get("power.max_limit", None)),
                    "clocks_currect_graphics": conv.to_int(i.get("clocks.graphics", None)),
                    "clocks_currect_memory": conv.to_int(i.get("clocks.memory", None)),
                    "clocks_currect_sm": conv.to_int(i.get("clocks.sm", None)),
                    "clocks_max_graphics": conv.to_int(i.get("clocks.max.graphics", None)),
                    "clocks_max_memory": conv.to_int(i.get("clocks.max.memory", None)),
                    "clocks_max_sm": conv.to_int(i.get("clocks.max.sm", None))
                }
            }
        )
    return out

def get_nvidia_videocards(priority: Literal['nvml', 'nsmi']='nsmi') -> List[Dict[str, Any]]:
    if priority == 'nvml':
        f1, f2 = get_nvidia_videocards_pynvml, get_nvidia_videocards_nsmi
    elif priority == 'nsmi':
        f1, f2 = get_nvidia_videocards_nsmi, get_nvidia_videocards_pynvml
    else:
        raise ValueError("The 'priority' argument can be: 'nvml' or 'nsmi'")
    
    if len(data:=f1()) == 0:
        data = f2()
    
    return data

def get_videocards() -> List[Dict[str, Any]]:
    d, out = conv.from_values(wmic("path", "win32_VideoController", "GET", "Name,VideoProcessor,AdapterRAM,Availability,AdapterCompatibility,VideoArchitecture,VideoMemoryType,DriverDate,DriverVersion", FORMAT="VALUE")), []
    for i in d:
        out.append(
            {
                "name": i.get("Name", None),
                "model": i.get("VideoProcessor", None),
                "company": i.get("AdapterCompatibility", None),
                "driver_version": i.get("DriverVersion", None),
                "driver_date": conv.windate_to_datetime(i.get("DriverDate", None)),
                "memory_capacity": conv.to_int(i.get("AdapterRAM", None)),
                "memory_type": get_vmtype(conv.to_int(i.get("VideoMemoryType", None))),
                "architecture": get_varch(conv.to_int(i.get("VideoArchitecture", None))),
                "availability": get_vaval(conv.to_int(i.get("Availability", None)))
            }
        )
    return out

def get_motherboard() -> Dict[str, Any]:
    info = conv.from_values(wmic("BASEBOARD", "GET", "Name,PoweredOn,Product,Removable,Replaceable,RequiresDaughterBoard,SerialNumber,Tag,Version,HostingBoard,HotSwappable,Manufacturer", FORMAT="VALUE"))[0]
    return {
        "name": info.get("Name", None),
        "tag": info.get("Tag", None),
        "version": info.get("Version", None),
        "product": info.get("Product", None),
        "serial_number": conv.sn(tnvv(info.get("SerialNumber", None))),
        "manufacturer": info.get("Manufacturer", None),
        "power_on": conv.to_bool(info.get("PoweredOn", None)),
        "removable": conv.to_bool(info.get("Removable", None)),
        "replaceable": conv.to_bool(info.get("Replaceable", None)),
        "rdb": conv.to_bool(info.get("RequiresDaughterBoard", None)),
        "hosting_board": conv.to_bool(info.get("HostingBoard", None)),
        "hot_swappable": conv.to_bool(info.get("HotSwappable", None))
    }

def get_bios() -> Dict[str, Any]:
    info = conv.from_values(wmic("BIOS", "LIST", FORMAT="VALUE"))[0]
    try: langs = conv.winlang_to_tuple(conv.removes(conv.replaces(info.get("ListOfLanguages", ""), {";": ",", "{": "", "}": "", "\"": ""}).split(","), [""]))
    except: langs = []
    try: clang = conv.winlang_to_tuple(info.get("CurrentLanguage", ""))
    except: clang = None
    try: characteristics = [chrct(int(i)) for i in eval(info.get("BiosCharacteristics", "{}").replace(";", ","))]
    except: characteristics = []
    return {
        "name": info.get("Name", None),
        "manufacturer": info.get("Manufacturer", None),
        "release_date": conv.windate_to_datetime(info.get("ReleaseDate", None)),
        "languages": langs,
        "current_language": clang,
        "is_primary": conv.to_bool(info.get("PrimaryBIOS", None)),
        "serial_number": conv.sn(tnvv(info.get("SerialNumber", None))),
        "version": info.get("Version", None),
        "smbios_version": info.get("SMBIOSBIOSVersion", None),
        "smbios_major_version": info.get("SMBIOSMajorVersion", None),
        "smbios_minor_version": info.get("SMBIOSMinorVersion", None),
        "smbios_present": conv.to_bool(info.get("SMBIOSPresent", None)),
        "characteristics": characteristics
    }
