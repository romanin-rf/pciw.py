from .Base import BaseParser
from .Linux import LinuxParser
from .Windows import WindowsParser
from typing import List, Type

__parsers__: List[Type[BaseParser]] = [LinuxParser, WindowsParser]