import platform
from typing import Any, Dict, List

# ! Константы
SYSTEM: str = platform.system()

# ! Исключения
class MethodIsNotSupported(Exception):
    def __init__(self, *args, **kwargs) -> None:
        """Called if the method is not supported by the OS"""
        if args.__len__() != 0:
            self.msg = " ".join([str(i) for i in args])
        else:
            if len(kwargs) == 0:
                self.msg = "This method is not supported on your system"
            else:
                if "method" in kwargs.keys():
                    self.msg = "The '%s' method is not supported by your operating system" % kwargs["method"].__name__
                else:
                    self.msg = "This method is not supported on your system"
    
    def __str__(self) -> str:
        return self.msg
    
    def __repr__(self) -> str:
        return "MethodIsNotSupported: {}".format(
            self.__str__()
        )

# ! Главный класс
class Supported:
    def __init__(self) -> None:
        self.methods: Dict[Any, bool] = {}

    def __add_method(self, method: Any, supported: List[str]) -> None:
        if method not in self.methods.keys():
            self.methods[method] = (SYSTEM in supported)
    
    def __by_supported(self, method: Any) -> bool:
        if method in self.methods.keys():
            if not self.methods[method]:
                return False
        return True

    def add_support(self, supported: List[str]):
        def adder(method):
            self.__add_method(method, supported)
            def wrapper(*args):
                if self.__by_supported(method):
                    if len(args) != 0:
                        return method(*args)
                    else:
                        return method()
                else:
                    raise MethodIsNotSupported(method=method)
            return wrapper
        return adder
