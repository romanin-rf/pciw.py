import platform
from typing import Any, Dict, List, Literal, Optional

# ! Константы
SYSTEM: str = platform.system()

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

    def add_support(
        self,
        supported: List[str],
        default_return: Optional[Any]=None,
        errors: Optional[Literal["ignore", "view"]]=None
    ) -> Any:
        errors = errors or "view"
        def adder(method):
            self.__add_method(method, supported)
            def wrapper(*args, **kwargs):
                if self.__by_supported(method):
                    if errors == "ignore":
                        try:
                            if len(args) != 0:
                                return method(*args, **kwargs)
                            else:
                                return method()
                        except:
                            return default_return
                    elif errors == "view":
                        if len(args) != 0:
                            return method(*args, **kwargs)
                        else:
                            return method()
                else:
                    return default_return
            return wrapper
        return adder
