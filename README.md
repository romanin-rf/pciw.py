# pciw.py
This module can obtain __full information__ about the `CPU`, `RAM`, `GPU`, `BIOS`, `motherboard` and `monitors`.
So far, it __only works fully__ on a `Windows` system.
## Install
```
pip install py-cpuinfo screeninfo psutil pciw.py
```
## Example
```python
from pciw import pciw

cpu, ram, bios, gpu, motherboard, monitors = pciw.CPU(), pciw.RAM(), pciw.BIOS(), pciw.GPU(), pciw.Motherboard(), pciw.Monitors()

"""CPU INFO"""
cpu.name
cpu.model
cpu.family
cpu.stepping
cpu.architecture
cpu.bits
cpu.frequency
cpu.cores_count
cpu.cache
cpu.flags

cpu.get_load_all() # -> cpu_load_all(standard, percent)
cpu.get_load()     # -> cpu_load(standard, percent)

"""GPU INFO"""
gpu.videocard      # -> [videocard(name, processor, memory, company, availability, driver_date, driver_version), ...]

"""RAM INFO"""
ram.memory_cards   # -> [memory_card(model, type, form_factor, capacity, frequency, serial_number, data_width, location), ...]

ram.get_status()   # -> psutil.virtual_memory()

"""Monitors INFO"""
monitors.displays  # -> [monitor(name, primary, size, size_mm, position), ...]

"""Motherboard INFO"""
motherboard.info   # -> motherboard(name, product, manufacturer, serial_number, version, tag, status, features)

"""BIOS INFO"""
bios.info          # -> bios(name, manufacturer, primary, version, release_date, serial_number, language_current, language_supported, characteristics, smbios)

```
## Author
- Roman Slabicky
    - [Vkontakte](https://vk.com/romanin2)
    - [GitHub](https://github.com/romanin-rf)