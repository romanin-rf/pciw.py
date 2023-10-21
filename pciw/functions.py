from typing import List, Dict, Optional, Union, TypeVar
# > Local Imports
from .units import NONE_VALUES

# ! Types
TP = TypeVar('TP')
T0 = TypeVar('T0')
T1 = TypeVar('T1')

# ! Standard Functions
def removes(l: List[Union[T0, T1]], ldv: List[T1]) -> List[T0]:
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

# ! Parsing Functions
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

# ! Spetific Functions
def sn(string: Optional[str]) -> Optional[str]:
    if string is not None:
        if not startswiths(string, NONE_VALUES):
            return string

# ! Optional Function
def aripti(value, operation: str="+0"):
    if value is not None:
        return eval(f'{value}{operation}')

def oround(value):
    if value is not None:
        return round(value)
