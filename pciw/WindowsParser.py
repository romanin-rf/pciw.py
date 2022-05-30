import cpuinfo
import screeninfo
import subprocess
import datetime
from dateutil import parser
from typing import Union, Any, List, Optional, Literal, Tuple, Dict
# ! Локальные импорты
try:
    from . import units
except:
    import units

# ! Функции
def exists_key(
    key: Union[str, int],
    data: Union[dict, list, tuple]
) -> Tuple[bool, Optional[Any]]:
    try:
        return True, data[key]
    except:
        return False, None

def removes(l: list, ldv: list) -> list:
    for value in ldv:
        for i in range(0, l.count(value)):
            l.remove(value)
    return l

def replaces(s: str, d: Dict[str, str]) -> str:
    for i in d.items():
        s = s.replace(i[0], i[1])
    return s

# ! Класс конвертации данных
class Converter:
    def value_to_dict(string: str) -> List[Dict[str, Optional[str]]]:
        data: List[List[str]] = [
            i.split("\r\r\n") for i in removes(
                string\
                    .replace("\r\r\n\r\r\n\r\r\n\r\r\n", "")\
                    .split("\r\r\n\r\r\n"),
                [""]
            )
        ]
        do = []
        for table in data:
            d = {}
            for line in table:
                rd = line.split("=")
                if rd[0].replace(" ", "") != "":
                    d[rd[0]] = rd[1]\
                        if (
                            rd[0].replace(" ", "") != ""
                        ) else None
            do.append(d)
        return do
    
    def str_to_bool(string: str) -> Optional[bool]:
        string = string.lower().replace(" ", "")
        if string == "true":
            return True
        elif string == "false":
            return False
    
    def str_to_int(string: str) -> Optional[int]:
        string = string.lower().replace(" ", "")
        try:
            return int(string)
        except:
            pass
    
    def windate_to_datetime(string: str) -> Optional[datetime.datetime]:
        try:
            return parser.parse(
                "{year}.{month}.{day} {hour}:{min}.{sec}"\
                .format(
                    year=string[0:4],
                    month=string[4:6],
                    day=string[6:8],
                    hour=string[8:10],
                    min=string[10:12],
                    sec=string[12:14]
                )
            )
        except:
            pass

# ! Функция запросов к WMIC
def request(
    method: str,
    treq: Optional[Literal["GET", "LIST"]]=None,
    data: Optional[Union[List[str], str]]=None,
    form: Optional[Literal["VALUE", "CSV"]]=None
) -> str:
    form = form or "VALUE"
    treq = treq or "LIST"
    if data is not None:
        req = subprocess.check_output(
            "wmic {0} {2} {1} /format:{3}"\
                .format(
                    method,
                    (",".join(data) if isinstance(data, list) else data),
                    treq,
                    form
                )
        )
    else:
        req = subprocess.check_output(f"wmic {method} {treq} /format:{form}")
    return req.decode(errors="ignore")

# ! Функции определения
def get_mff(code: int) -> str:
    return units.NT_TYPES.MEMORY_FORM_FACTOR[code]

def get_mtype(code: int) -> str:
    return units.NT_TYPES.MEMORY_TYPE[code]

def get_vmtype(code: int) -> str:
    return units.NT_TYPES.VIDEO_MEMORY_TYPE[code]

def get_varch(code: int) -> str:
    return units.NT_TYPES.VIDEO_ARCHITECTURE[code]

# ! Get-функции
def get_cpu() -> Dict[str, Any]:
    info = cpuinfo.get_cpu_info()
    return {
        "name": info["brand_raw"],
        "model": info["model"],
        "family": info["family"],
        "stepping": info["stepping"],
        "architecture": info["arch"],
        "bits": int(info["bits"]),
        "frequency": info["hz_actual"][0] / 1000000000,
        "cores_count": info["count"],
        "cache": {
            "l2_size": exists_key("l2_cache_size", info)[1],
            "l3_size": exists_key("l3_cache_size", info)[1]
        },
        "flags": [i.upper() for i in info["flags"]]
    }

def get_ram() -> List[Dict[str, Any]]:
    ld, uld = Converter.value_to_dict(request("MEMORYCHIP")), []
    for i in ld:
        uld.append(
            {
                "device_location": i["DeviceLocator"],
                "form_factor": get_mff(Converter.str_to_int(i["FormFactor"])),
                "type": get_mtype(Converter.str_to_int(i["MemoryType"])),
                "serial_number": i["SerialNumber"].replace(" ", ""),
                "part_number": i["PartNumber"].replace(" ", ""),
                "capacity": Converter.str_to_int(i["Capacity"]),
                "frequency": Converter.str_to_int(i["Speed"]),
                "data_width": Converter.str_to_int(i["DataWidth"])
            }
        )
    return uld

def get_monitors() -> List[Dict[str, Any]]:
    return [
        {
            "name": replaces(i.name, {"\\": "", ".": ""}),
            "size": (i.width, i.height),
            "size_mm": (i.width_mm, i.height),
            "is_primary": i.is_primary
        } for i in screeninfo.get_monitors()
    ]

def get_videocards() -> List[Dict[str, Any]]:
    ld, uld = Converter.value_to_dict(
        request(
            "path win32_VideoController", "GET", "Name,VideoProcessor,AdapterRAM,Availability,AdapterCompatibility,VideoArchitecture,VideoMemoryType,DriverDate,DriverVersion"
        )
    ), []
    for i in ld:
        uld.append(
            {
                "name": i["Name"],
                "model": i["VideoProcessor"],
                "company": i["AdapterCompatibility"],
                "driver_version": i["DriverVersion"],
                "driver_date": Converter.windate_to_datetime(i["DriverDate"]),
                "memory_capacity": Converter.str_to_int(i["AdapterRAM"]),
                "memory_type": get_vmtype(Converter.str_to_int(i["VideoMemoryType"])),
                "architecture": get_varch(Converter.str_to_int(i["VideoArchitecture"]))
            }
        )
    return uld