import datetime
from dateutil import parser
from typing import Union, List, Optional, Tuple, Dict
# > Локальные импорты
from . import tree
from . import units

# ! Vars
LINUX_BYTES_NAMES: Dict[str, int] = {
    "KiB": 1024,
    "MiB": 1024**2,
    "GiB": 1024**3,
    "TiB": 1024**4,
}

# ! Функции редактирования
def removes(l: list, ldv: list) -> list:
    for value in ldv:
        for i in range(0, l.count(value)):
            l.remove(value)
    return l

def replaces(s: str, d: Dict[str, str]) -> str:
    for i in d.items():
        try: s = s.replace(i[0], i[1])
        except: pass
    return s

def startswiths(string: str, sl: List[str]) -> bool:
    for i in sl:
        if string.startswith(i):
            return True
    return False

# ! Convert Functions
def to_bool(string: str) -> Optional[bool]:
    try: return bool(str(string).replace(" ", "").title())
    except: pass

def to_int(string: Optional[str]) -> Optional[int]:
    try:
        return int(str(string).lower().replace(" ", ""))
    except:
        try:
            return round(float(replaces(str(string).lower(), {" ": "", ",": "."})))
        except:
            pass

def to_float(string: Optional[str]) -> Optional[float]:
    try:
        return float(replaces(str(string).lower(), {" ": "", ",": "."}))
    except:
        try:
            return float(int(str(string).lower().replace(" ", "")))
        except:
            pass

def from_values(string: str) -> List[Dict[str, Optional[str]]]:
    data: List[List[str]] = [
        i.split("\r\r\n") for i in removes(
            string.replace("\r\r\n\r\r\n\r\r\n\r\r\n", "").split("\r\r\n\r\r\n"),
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

def from_csv(data: str, *, header: Optional[List[str]]=None, sep=",", end="\r\r\n") -> List[Dict[str, str]]:
    dt: List[List[str]] = [i.split(sep) for i in removes(data.split(end), [""])]
    head, out = header or dt[0], []
    if header is None: dt = dt[1:]
    for d in dt:
        l = {}
        for idx, i in enumerate(head):
            l[i] = d[idx]
        out.append(l)
    return out

def from_tcpu_data(s: str) -> tree.Tree:
    t, slines = tree.Tree(), removes(s.split("\r\n"), [""])
    for sline in slines:
        *keys, value = str(sline).replace(" ", "_").lower().split(":")
        if (data:=to_float(value)) is not None: value = data
        elif (data:=to_int(value)) is not None: value = data
        elif value.replace("_","") == "": value = None
        t.set(".".join(keys), value)
    return t

# ! Windows Convertion Functions
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
    except: pass

def winlang_to_tuple(string: Union[List[str], str], *, string_sep=";") -> Optional[Union[List[Tuple[str, str, str]], Tuple[str, str, str]]]:
    try:
        if isinstance(string, list):
            return [tuple(i.split("|")) for i in string]
        elif isinstance(string, str):
            return tuple(string.split("|"))
    except: pass

# ! Linux Convertion Functions
def linux_bytes(string: Optional[Union[str, int]]) -> Optional[int]:
    if not isinstance(string, int):
        if string is not None:
            ls = string.split(' ')
            try: return int(ls[0]) * LINUX_BYTES_NAMES[ls[1]]
            except: pass
    return string

# ! Функции проверки
def sn(string: Optional[str]) -> Optional[str]:
    if string is not None:
        if not startswiths(string, units.NONE_TYPE_EXCEPTIONS):
            return string

# ! Optional Functions
def aripti(value, operation: str="+0"):
    if value is not None:
        return eval(f'{value}{operation}')

def oround(value):
    if value is not None:
        return round(value)