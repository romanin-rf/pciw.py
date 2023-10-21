from typing import Generator, Any

# ! Base Classes
class BaseError(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.args = tuple(self.__error__(*args, **kwargs))
    
    def __error__(self, *args, **kwargs) -> Generator[str, Any, None]:
        pass

# ! Errors
class NotSupportedError(BaseError):
    def __error__(self, *args, **kwargs):
        yield "This is not supported on your platform."

class NSMINotFoundError(BaseError):
    def __error__(self, *args, **kwargs):
        yield "No nvidia-smi was detected, maybe we don't have NVIDIA driver."