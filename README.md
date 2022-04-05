# pciw.py
This module can obtain __full information__ about the `CPU`, `RAM`, `GPU`, `BIOS`, `motherboard` and `monitors`.
So far, it __only works fully__ on a `Windows` system.
## Install
```
pip install py-cpuinfo screeninfo psutil
```
## Example
```python
from pciw import pciw

cpu, ram, bios, gpu, motherboard, monitors = pciw.CPU(), pciw.RAM(), pciw.BIOS(), pciw.GPU(), pciw.Motherboard(), pciw.Monitors()
```
## Author
- Roman Slabicky
    - [Vkontakte](https://vk.com/romanin2)
    - [GitHub](https://github.com/romanin-rf)