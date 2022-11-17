import datetime
from dateutil import parser
from typing import Union, Any, List, Optional, Tuple, Dict
# ! Локальные импорты
try:
    from . import units as units
except:
    import units as units

# ! Константы
LINUX_BYTES_NAMES: Dict[str, int] = {
    "KiB": 1024,
    "MiB": 1048576,
    "GiB": 1073741824
}

# ! Главные функции
def exists_key(
    key: Union[str, int],
    data: Union[dict, list, tuple]
) -> Tuple[bool, Optional[Any]]:
    try:
        return True, data[key]
    except:
        return False, None

def eks(
    data: Union[dict, list, tuple],
    keys: Union[str, Union[list, str]]
) -> Tuple[bool, Optional[Any]]:
    ks = ""
    if isinstance(keys, str):
        for i in keys.split("."):
            try:
                it = eval(i)
                ks += f"[{it}]"
            except:
                it = str(i)
                ks += f"[\"{it}\"]"
    elif isinstance(keys, list):
        for i in keys:
            if isinstance(i, str):
                ks += f"[\"{i}\"]"
            else:
                ks += f"[{i}]"
    try:
        return True, eval(f"data{ks}")
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

def startswiths(string: str, sl: List[str]) -> bool:
    for i in sl:
        if string.startswith(i):
            return True
    return False

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
    for idx, item in enumerate(do):
        for key in item.keys():
            if item[key].replace(" ", "") == "":
                do[idx][key] = None
    return do

def str_to_bool(string: str) -> Optional[bool]:
    string = string.lower().replace(" ", "")
    if string == "true":
        return True
    elif string == "false":
        return False

def str_to_int(string: Optional[Union[str, int]]) -> Optional[int]:
    if string is not None:
        if not isinstance(string, int):
            string = string.lower().replace(" ", "")
            try:
                return int(string)
            except:
                pass
        return string

def str_to_float(string: Optional[str]) -> Optional[float]:
    if string is not None:
        string = replaces(string.lower(), {" ": "", ",": "."})
        try:
            return float(string)
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

def winlang_to_tuple(string: Union[List[str], str]) -> Optional[Union[List[Tuple[str, str, str]], Tuple[str, str, str]]]:
    try:
        if isinstance(string, list):
            return [tuple(i.split("|")) for i in string]
        elif isinstance(string, str):
            return tuple(string.split("|"))
    except:
        pass

def sn(string: Optional[str]) -> Optional[str]:
    if string is not None:
        if not startswiths(string, units.SERIAL_NUMBER_EXCEPTIONS):
            return string

def from_csv(data: str, dvalue: str, dline: str) -> List[List[str]]:
    data_values = []
    lines = removes(data.split(dline), [""])
    for i in lines:
        data_values.append(
            i.split(dvalue)
        )
    return data_values

def t_cpu_data_to_dict(s: str) -> Dict[str, Dict[str, Dict[Any, Any]]]:
    data = {}
    for i in removes(s.split("\r\n"), [""]):
        i: str
        d = [i.lower() for i in i.split(":")]
        # ! ДОЛПИСАТЬ ПАРСИНГ
        if d[0] not in data:
            data[d[0]] = {}
        if d[2] not in data[d[0]]:
            data[d[0]][d[2]] = {}
        
        d[3] = d[3] if (d[3] not in [""]) else None

        if d[0] == "cpu":
            try:
                if d[2] == "temperature":
                    data[d[0]][d[2]][int(d[1][-1:])] = str_to_int(d[3])
                else:
                    data[d[0]][d[2]][int(d[1][-1:])] = str_to_float(d[3])
            except:
                if d[2] == "temperature":
                    data[d[0]][d[2]][replaces(d[1], {"cpu ": ""})] = str_to_int(d[3])
                else:
                    data[d[0]][d[2]][replaces(d[1], {"cpu ": ""})] = str_to_float(d[3])
    return data

def linux_bytes(string: Optional[Union[str, int]]) -> Optional[int]:
    if not isinstance(string, int):
        if string is not None:
            ls = string.split(' ')
            try:
                return int(ls[0]) * LINUX_BYTES_NAMES[ls[1]]
            except:
                pass
    return string