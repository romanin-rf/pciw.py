from . import pciw
from rich.console import Console

console = Console()

console.print(f"[yellow]Location of this file[/] [red]->[/] [green]{__file__}[/]")
console.rule("CPU INFO")
console.print(pciw.get_cpu_info())

console.rule("RAM INFO")
console.print(pciw.get_ram_info())

console.rule("GPU INFO")
console.print(pciw.get_video_info())

console.rule("MONITORS INFO")
console.print(pciw.get_monitors_info())

console.rule("MOTHERBOARD INFO")
console.print(pciw.get_motherboard_info())

console.rule("BIOS INFO")
console.print(pciw.get_bios_info())