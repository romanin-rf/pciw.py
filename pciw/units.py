import os
import glob
import platform

# ! Функции получения тега системы
def systag() -> str:
    return f"{platform.system()}-{platform.machine()}"

# ! Для функций
NONE_TYPE_EXCEPTIONS = [
    "tobefilled", "default", "n/a",
    "[notsupported]", "[n/a]",
    "tobefilledbyo.e.m."
]

# ! Поиск nvidia-smi (WINDOWS ONLY)
WINDOWS_NVIDIA_SMI_PATH = "nvidia-smi"
WINDOWS_NVIDIA_SMI_POSSIBLE_PATHS = [
    "{sd}\\Windows\\System32\\DriverStore\\FileRepository\\*\\nvidia-smi.exe",
    "{sd}\\Program Files\\NVIDIA Corporation\\NVSMI\\*\\nvidia-smi.exe"
]

if platform.system() == "Windows":
    system_drive = os.getenv("SystemDrive")
    for possible_path in WINDOWS_NVIDIA_SMI_POSSIBLE_PATHS:
        gwnsmi = glob.glob(possible_path.format(sd=system_drive), recursive=True)
        if len(gwnsmi) != 0:
            WINDOWS_NVIDIA_SMI_PATH = gwnsmi[0]
            break
    del system_drive

# ! Определение путей
NVIDIA_SMI_PATH_SUPPORTED = {
    "Windows-AMD64": WINDOWS_NVIDIA_SMI_PATH,
    "Windows-x86_64": WINDOWS_NVIDIA_SMI_PATH,
    "Linux-x86_64": "nvidia-smi"
}
T_CPU_PATH_SUPPORTED = {
    "Windows-AMD64": os.path.join(os.path.dirname(__file__), "data\\t_cpu\\Windows-x86_64\\parser.py"),
    "Windows-x86_64": os.path.join(os.path.dirname(__file__), "data\\t_cpu\\Windows-x86_64\\parser.py")
}
T_CPU_PATH_ADMIN_SUPPORTED = {
    "Windows-AMD64": os.path.join(os.path.dirname(__file__), "data\\t_cpu\\Windows-x86_64\\t_cpu.exe"),
    "Windows-x86_64": os.path.join(os.path.dirname(__file__), "data\\t_cpu\\Windows-x86_64\\t_cpu.exe")
}

NVIDIA_SMI_PATH: str = NVIDIA_SMI_PATH_SUPPORTED.get(systag(), None)
T_CPU_PATH: str = T_CPU_PATH_SUPPORTED.get(systag(), None)
T_CPU_PATH_ADMIN: str = T_CPU_PATH_ADMIN_SUPPORTED.get(systag(), None)

# ! Для определения значений
class NT:
    MEMORY_TYPE = {
        0: None,
        1: '<UNKNOWN>',
        2: 'DRAM',
        3: 'SYNCHRONOUS_DRAM',
        4: 'CACHE_DRAM',
        5: 'EDO',
        6: 'EDRAM',
        7: 'VRAM',
        8: 'SRAM',
        9: 'RAM',
        10: 'ROM',
        11: 'Flash',
        12: 'EEPROM',
        13: 'FEPROM',
        14: 'EPROM',
        15: 'CDRAM',
        16: '3DRAM',
        17: 'SDRAM',
        18: 'SGRAM',
        19: 'RDRAM',
        20: 'DDR',
        21: 'DDR2',
        22: 'DDR2_FB-DIMM',
        23: None,
        24: 'DDR3',
        25: 'FBD2',
        26: 'DDR4',
        27: 'LPDDR',
        28: 'LPDDR2',
        29: 'LPDDR3',
        30: 'LPDDR4',
        31: 'LOGICAL_NON-VOLATILE_DEVICE',
        32: 'HBM',
        33: 'HBM2',
        34: 'DDR5',
        35: 'LPDDR5'
    }
    MEMORY_FORM_FACTOR = {
        0: None,
        1: '<UNKNOWN>',
        2: 'SIP',
        3: 'DIP',
        4: 'ZIP',
        5: 'SOJ',
        6: 'PROPRIETARY',
        7: 'SIMM',
        8: 'DIMM',
        9: 'TSOP',
        10: 'PGA',
        11: 'RIMM',
        12: 'SODIMM',
        13: 'SRIMM',
        14: 'SMD',
        15: 'SSMP',
        16: 'QFP',
        17: 'TQFP',
        18: 'SOIC',
        19: 'LCC',
        20: 'PLCC',
        21: 'BGA',
        22: 'FPBGA',
        23: 'LGA',
        24: 'FB-DIMM'
    }
    VIDEO_MEMORY_TYPE = {
        1: "<UNKNOWN>",
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
        1: "<UNKNOWN>",
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
        1: '<UNKNOWN>',
        2: None,
        3: 'WORK',
        4: 'WARNING',
        5: 'TESTED',
        6: 'NOT_APPLICABLE',
        7: 'POWER_OFF',
        8: 'STAND-ALONE_OPERATION',
        9: 'NOT_SERVE',
        10: 'DEGRADATION',
        11: 'NOT_ESTABLISHED',
        12: 'INSTALLATION_ERROR',
        13: 'ENERGY_SAVING_NOT_DATA',
        14: 'ENERGY_SAVING_LOW_CONSUMPTION_MODE',
        15: 'ENERGY_SAVING_STANDBY_MODE',
        16: 'POWER_CYCLE',
        17: 'ENERGY_SAVING_WARNING'
    }
    BIOS_CHARACTERISTICS = {
        0: 'RESERVED',
        1: 'RESERVED',
        2: None,
        3: 'NOT_CHARACTERISTICS',
        4: 'ISA',
        5: 'MCA',
        6: 'EISA',
        7: 'PCI',
        8: 'PCMCIA',
        9: 'PLUG_AND_PLAY',
        10: 'APM',
        11: 'UPDATED',
        12: 'SHADING_AVAILABLE',
        13: 'VL-VESA',
        14: 'ESCD',
        15: 'LOADING_FROM_CD',
        16: 'BOOT_CHOICE',
        17: 'BIOS_ROM_SOCKETED',
        18: 'LOADING_FROM_PCMCIA',
        19: 'EDD',
        20: 'FLOPPY_NEC9800',
        21: 'FLOPPY_TOSHIBA',
        22: 'FLOPPY_525',
        23: 'FLOPPY_525',
        24: 'FLOPPY_35',
        25: 'FLOPPY_35',
        26: 'PRINT_SCREEN',
        27: 'KEYBOARD_8042',
        28: 'SERIAL',
        29: 'PRINTER',
        30: 'CGA_MONO_VIDEO',
        31: 'NEC_PC98',
        32: 'ACPI',
        33: 'OBSOLETE_USB',
        34: 'AGP',
        35: 'I2O_LOADING',
        36: 'LS120_LOADINGS',
        37: 'ATAPI_ZIP_DRIVER_LOADING',
        38: '1394_LOADING',
        39: 'SMART_BATTERY',
        40: '<BIOS{code}>',
        41: '<BIOS{code}>',
        42: '<BIOS{code}>',
        43: '<BIOS{code}>',
        44: '<BIOS{code}>',
        45: '<BIOS{code}>',
        46: '<BIOS{code}>',
        47: '<BIOS{code}>',
        48: '<OS{code}>',
        49: '<OS{code}>',
        50: '<OS{code}>',
        51: '<OS{code}>',
        52: '<OS{code}>',
        53: '<OS{code}>',
        54: '<OS{code}>',
        55: '<OS{code}>',
        56: '<OS{code}>',
        57: '<OS{code}>',
        58: '<OS{code}>',
        59: '<OS{code}>',
        60: '<OS{code}>',
        61: '<OS{code}>',
        62: '<OS{code}>',
        63: '<OS{code}>'
    }