import os
import platform

# ! Для функций
SERIAL_NUMBER_EXCEPTIONS = [
    "To be filled",
    "Default",
    "N/A"
]
NVIDIA_VALUES_EXCEPTIONS = [
    "[Not Supported]"
]
# ! Для проверки поддержки
NVIDIA_SMI_PATH_SUPPORTED = {
    "Windows": "nsmi.exe"
}
try:
    NVIDIA_SMI_PATH = os.path.join(os.path.dirname(__file__), "data", NVIDIA_SMI_PATH_SUPPORTED[platform.system()])
except:
    NVIDIA_SMI_PATH = None
# ! Для определения типа
class NT_TYPES:
    MEMORY_TYPE = [
        None, "Other", "DRAM", "Synchronous DRAM", "Cache DRAM",
        "EDO", "EDRAM", "VRAM", "SRAM", "RAM", "ROM", "Flash",
        "EEPROM", "FEPROM", "EPROM", "CDRAM", "3DRAM", "SDRAM",
        "SGRAM", "RDRAM", "DDR", "DDR2", "DDR2 FB-DIMM", None,
        "DDR3", "FBD2", "DDR4"
    ]
    MEMORY_FORM_FACTOR = [
        None, "Other", "SIP", "DIP", "ZIP", "SOJ", "Proprietary",
        "SIMM", "DIMM", "TSOP", "PGA","RIMM", "SODIMM", "SRIMM",
        "SMD", "SSMP", "QFP", "TQFP", "SOIC", "LCC", "PLCC", "BGA",
        "FPBGA", "LGA", "FB-DIMM"
    ]
    VIDEO_MEMORY_TYPE = {
        1: "Other",
        2: None,
        3: "VRAM",
        4: "DRAM",
        5: "SRAM",
        6: "WRAM",
        7: "EDO RAM",
        8: "Burst Synchronous DRAM",
        9: "Pipelined Burst SRAM",
        10: "CDRAM",
        11: "3DRAM",
        12: "SDRAM",
        13: "SGRAM"
    }
    VIDEO_ARCHITECTURE = {
        1: "Other",
        2: None,
        3: "CGA",
        4: "EGA",
        5: "VGA",
        6: "SVGA",
        7: "MDA",
        8: "HGC",
        9: "MCGA",
        10: "8514A",
        11: "XGA",
        12: "Linear Frame Buffer",
        160: "PC-98"
    }
    VIDEO_ALAILABILITY = {
        1: "other",
        2: None,
        3: "work",
        4: "warning",
        5: "tested",
        6: "not_applicable",
        7: "power_off",
        8: "stand-alone_operation",
        9: "not_serve",
        10: "degradation",
        11: "not_established",
        12: "installation_error",
        13: "energy_saving_not_data",
        14: "energy_saving_low_consumption_mode",
        15: "energy_saving_standby_mode",
        16: "power_cycle",
        17: "energy_saving_warning"
    }
    BIOS_CHARACTERISTICS = {
        0: 'reserved',
        1: 'reserved',
        2: None,
        3: 'not_characteristics',
        4: 'ISA',
        5: 'MCA',
        6: 'EISA',
        7: 'PCI',
        8: 'PCMCIA',
        9: 'plug_and_play',
        10: 'APM',
        11: 'updated',
        12: 'shading_available',
        13: 'VL-VESA',
        14: 'ESCD',
        15: 'loading_from_cd',
        16: 'boot_choice',
        17: 'bios_rom_socketed',
        18: 'loading_from_pcmcia',
        19: 'EDD',
        20: 'floppy_nec9800',
        21: 'floppy_toshiba',
        22: 'floppy_525',
        23: 'floppy_525',
        24: 'floppy_35',
        25: 'floppy_35',
        26: 'print_screen',
        27: 'keyboard_8042',
        28: 'serial',
        29: 'printer',
        30: 'cga_mono_video', 
        31: 'nec_pc98',
        32: 'ACPI',
        33: 'obsolete_usb',
        34: 'AGP',
        35: 'i2o_loading',
        36: 'ls120_loadings',
        37: 'atapi_zip_driver_loading',
        38: '1394_loading',
        39: 'smart_battery',
        40: 'bios_other',
        41: 'bios_other',
        42: 'bios_other',
        43: 'bios_other',
        44: 'bios_other',
        45: 'bios_other',
        46: 'bios_other',
        47: 'bios_other',
        48: 'os_other',
        49: 'os_other',
        50: 'os_other',
        51: 'os_other',
        52: 'os_other',
        53: 'os_other',
        54: 'os_other',
        55: 'os_other',
        56: 'os_other',
        57: 'os_other',
        58: 'os_other',
        59: 'os_other',
        60: 'os_other',
        61: 'os_other',
        62: 'os_other',
        63: 'os_other'
    }