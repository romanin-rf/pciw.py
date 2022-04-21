import psutil
import cpuinfo
import platform
import datetime
import subprocess
import screeninfo
from typing import Union, Any
from collections import namedtuple
from dateutil import parser

class __info__:
	name = "pciw"
	version = ["0.1", 0.1]
	authors = ["ProgrammerFromParlament"]

class __data__:
	nt_memory_type = [None, "Other", "DRAM", "Synchronous DRAM", "Cache DRAM", "EDO", "EDRAM", "VRAM", "SRAM", "RAM", "ROM", "Flash", "EEPROM", "FEPROM", "EPROM", "CDRAM", "3DRAM", "SDRAM", "SGRAM", "RDRAM", "DDR", "DDR2", "DDR2 FB-DIMM", None, "DDR3", "FBD2", "DDR4"]
	nt_memory_form_factor = [None, "Other", "SIP", "DIP", "ZIP", "SOJ", "Proprietary", "SIMM", "DIMM", "TSOP", "PGA", "RIMM", "SODIMM", "SRIMM", "SMD", "SSMP", "QFP", "TQFP", "SOIC", "LCC", "PLCC", "BGA", "FPBGA", "LGA", "FB-DIMM"]
	nt_video_memory_type = {1: "Other", 2: None, 3: "VRAM", 4: "DRAM", 5: "SRAM", 6: "WRAM", 7: "EDO RAM", 8: "Burst Synchronous DRAM", 9: "Pipelined Burst SRAM", 10: "CDRAM", 11: "3DRAM", 12: "SDRAM", 13: "SGRAM"}
	nt_video_architecture = {1: "Other", 2: None, 3: "CGA", 4: "EGA", 5: "VGA", 6: "SVGA", 7: "MDA", 8: "HGC", 9: "MCGA", 10: "8514A", 11: "XGA", 12: "Linear Frame Buffer", 160: "PC-98"}
	nt_video_availability = {1: "other", 2: None, 3: "works", 4: "warning", 5: "tested", 6: "not_applicable", 7: "power_off", 8: "stand-alone_operation", 9: "not_serve", 10: "degradation", 11: "not_established", 12: "installation_error", 13: "energy_saving_not_data", 14: "energy_saving_low_consumption_mode", 15: "energy_saving_standby_mode", 16: "power_cycle", 17: "energy_saving_warning"}
	nt_comparison_bool = {"false": False, "true": True}
	nt_bios_characteristic = {0: 'reserved', 1: 'reserved', 2: None, 3: 'not_characteristics', 4: 'ISA', 5: 'MCA', 6: 'EISA', 7: 'PCI', 8: 'PCMCIA', 9: 'plug_and_play', 10: 'APM', 11: 'updated', 12: 'shading_available', 13: 'VL-VESA', 14: 'ESCD', 15: 'loading_from_cd', 16: 'boot_choice', 17: 'bios_rom_socketed', 18: 'loading_from_pcmcia', 19: 'EDD', 20: 'floppy_nec9800', 21: 'floppy_toshiba', 22: 'floppy_525', 23: 'floppy_525', 24: 'floppy_35', 25: 'floppy_35', 26: 'print_screen', 27: 'keyboard_8042', 28: 'serial', 29: 'printer', 30: 'cga_mono_video', 31: 'nec_pc98', 32: 'ACPI', 33: 'obsolete_usb', 34: 'AGP', 35: 'i2o_loading', 36: 'ls120_loadings', 37: 'atapi_zip_driver_loading', 38: '1394_loading', 39: 'smart_battery', 40: 'bios_other', 41: 'bios_other', 42: 'bios_other', 43: 'bios_other', 44: 'bios_other', 45: 'bios_other', 46: 'bios_other', 47: 'bios_other', 48: 'os_other', 49: 'os_other', 50: 'os_other', 51: 'os_other', 52: 'os_other', 53: 'os_other', 54: 'os_other', 55: 'os_other', 56: 'os_other', 57: 'os_other', 58: 'os_other', 59: 'os_other', 60: 'os_other', 61: 'os_other', 62: 'os_other', 63: 'os_other'}

class __types_nt__:
	cpu_cache = namedtuple("cpu_cache", ["size", "line_size", "associativity"])
	cpu_cache_size = namedtuple("cpu_cache_size", ["L2", "L3"])
	cpu_cache_line_size = namedtuple("cpu_cache_line_size", ["L2"])
	cpu_cache_associativity = namedtuple("cpu_cache_line_size", ["L2"])
	cpu_load = namedtuple("cpu_load", ["standard", "percent"])
	cpu_load_all = namedtuple("cpu_load_all", ["standard", "percent"])
	memory_card = namedtuple("memory_card", ["model", "type", "form_factor", "capacity", "frequency", "serial_number", "data_width", "location"])
	monitor = namedtuple("monitor", ["name", "primary", "size", "size_mm", "position"])
	videocard = namedtuple("videocard", ["name", "processor", "memory", "company", "availability", "driver_date", "driver_version"])
	videocard_memory = namedtuple("videocard_memory", ["type", "size"])
	videocard_processor = namedtuple("videocard_processor", ["name", "architecture"])
	motherboard = namedtuple("motherboard", ["name", "product", "manufacturer", "serial_number", "version", "tag", "status", "features"])
	motherboard_status = namedtuple("motherboard_status", ["powered_on", "hosting_board"])
	motherboard_features = namedtuple("motherboard_features", ["removable", "replaceable", "requires_daughter_board", "hot_swappable"])
	bios = namedtuple("bios", ["name", "manufacturer", "primary", "version", "release_date", "serial_number", "language_current", "language_supported", "characteristics", "smbios"])
	smbios = namedtuple("smbios", ["version", "major_version", "minor_version", "present"])

class __func__:
	def exists_key(key: Union[str, int], data: Union[dict, list, tuple]) -> tuple[bool, Union[None, Any]]:
		try:
			return True, data[key]
		except:
			return False, None
	
	def delect_values_list(l: list[Any], ldv: list[Any]) -> list:
		for value in ldv:
			for i in range(0, l.count(value)):
				l.remove(value)
		return l
	
	def str_to_bool(string: str) -> bool:
		return __data__.nt_comparison_bool[string.lower().replace(" ", "")]
	
	def values_str_to_dict(string: str) -> list[dict[str, Union[str, None]]]:
		data: list[list[str]] = [i.split("\r\r\n") for i in __func__.delect_values_list(string.replace("\r\r\n\r\r\n\r\r\n\r\r\n", "").split("\r\r\n\r\r\n"), [""])]
		do = []
		for table in data:
			d = {}
			for line in table:
				rd = line.split("=")
				if rd[0].replace(" ", "") != "":
					d[rd[0]] = rd[1] if (rd[0].replace(" ", "") != "") else None
			do.append(d)
		return do
	
	def windate_to_datetime(string: str) -> datetime.datetime:
		return parser.parse("{year}.{month}.{day} {hour}:{min}.{sec}".format(year=string[0:4], month=string[4:6], day=string[6:8], hour=string[8:10], min=string[10:12], sec=string[12:14]))

	def get_memory_info_nt() -> list[__types_nt__.memory_card]:
		data = __func__.values_str_to_dict(subprocess.check_output("wmic memorychip get devicelocator,partnumber,serialnumber,capacity,speed,datawidth,formfactor,memorytype /FORMAT:value").decode(errors="ignore"))
		do = []
		for i in data:
			do.append(
				__types_nt__.memory_card(
					i["PartNumber"],
					__data__.nt_memory_type[int(i["MemoryType"])],
					__data__.nt_memory_form_factor[int(i["FormFactor"])],
					int(i["Capacity"]),
					int(i["Speed"]),
					str(i["SerialNumber"]),
					int(i["DataWidth"]),
					str(i["DeviceLocator"])
				)
			)
		return do
	
	def get_monitors_info_nt() -> list[__types_nt__.monitor]:
		displays = []
		for monotor_data in screeninfo.get_monitors():
			displays.append(__types_nt__.monitor(monotor_data.name.replace("\\", "").replace(".", ""), monotor_data.is_primary, [monotor_data.width, monotor_data.height], [monotor_data.width_mm, monotor_data.height_mm], [monotor_data.x, monotor_data.y]))
		return displays
	
	def get_videocards_info_nt() -> list[__types_nt__.videocard]:
		data = __func__.values_str_to_dict(subprocess.check_output("wmic path win32_VideoController get Name,VideoProcessor,AdapterRAM,Availability,AdapterCompatibility,VideoArchitecture,VideoMemoryType,DriverDate,DriverVersion /FORMAT:value").decode(errors="ignore"))
		do = []
		for i in data:
			do.append(
				__types_nt__.videocard(
					str(i["VideoProcessor"]),
					__types_nt__.videocard_processor(
						str(i["Name"]),
						__data__.nt_video_architecture[int(i["VideoArchitecture"])]
					),
					__types_nt__.videocard_memory(
						__data__.nt_video_memory_type[int(i["VideoMemoryType"])],
						int(i["AdapterRAM"])
					),
					str(i["AdapterCompatibility"]),
					__data__.nt_video_availability[int(i["Availability"])],
					__func__.windate_to_datetime(str(i["DriverDate"])),
					str(i["DriverVersion"])
				)
			)
		return do
	
	def get_motherboard_info_nt() -> list:
		i = __func__.values_str_to_dict(subprocess.check_output("wmic BASEBOARD get Name,PoweredOn,Product,Removable,Replaceable,RequiresDaughterBoard,SerialNumber,Tag,Version,HostingBoard,HotSwappable,Manufacturer /FORMAT:VALUE").decode(errors="ignore"))[0]
		return __types_nt__.motherboard(
			str(i["Name"]),
			str(i["Product"]),
			str(i["Manufacturer"]),
			str(i["SerialNumber"]),
			str(i["Version"]),
			str(i["Tag"]),
			__types_nt__.motherboard_status(
				__func__.str_to_bool(str(i["PoweredOn"])),
				__func__.str_to_bool(str(i["HostingBoard"]))
			),
			__types_nt__.motherboard_features(
				__func__.str_to_bool(str(i["Removable"])),
				__func__.str_to_bool(str(i["Replaceable"])),
				__func__.str_to_bool(str(i["RequiresDaughterBoard"])),
				__func__.str_to_bool(str(i["HotSwappable"]))
			)
		)
	
	def get_bios_info_nt() -> __types_nt__.bios:
		i = __func__.values_str_to_dict(subprocess.check_output("wmic bios list full").decode(errors="ignore"))[0]
		characteristics_ids, characteristics = list(eval(str(i["BiosCharacteristics"]))), []
		for cid in characteristics_ids:
			characteristics.append(__data__.nt_bios_characteristic[cid])
		return __types_nt__.bios(
			str(i["Name"]),
			str(i["Manufacturer"]),
			__func__.str_to_bool(str(i["PrimaryBIOS"])),
			str(i["Version"]),
			__func__.windate_to_datetime(str(i["ReleaseDate"])),
			str(i["SerialNumber"]),
			str(i["CurrentLanguage"]).split("|"),
			[i.split("|") for i in list(eval(i["ListOfLanguages"]))],
			list(set(characteristics)),
			__types_nt__.smbios(
				str(i["SMBIOSBIOSVersion"]),
				str(i["SMBIOSMajorVersion"]),
				str(i["SMBIOSMinorVersion"]),
				__func__.str_to_bool(str(i["SMBIOSPresent"]))
			)
		)

class CPU():
	def __init__(self) -> None:
		info = cpuinfo.get_cpu_info()
		self.name: str = info["brand_raw"]
		self.model: str = info["model"]
		self.family: str = info["family"]
		self.stepping: str = info["stepping"]
		self.architecture: str = info["arch"]
		self.bits: Any = info["bits"]
		self.frequency: float = info["hz_actual"][0] / 1000000000
		self.cores_count: float = info["count"]
		self.cache: __types_nt__.cpu_cache = __types_nt__.cpu_cache(
			__types_nt__.cpu_cache_size(
				__func__.exists_key("l2_cache_size", info)[1],
				__func__.exists_key("l3_cache_size", info)[1]
			),
			__types_nt__.cpu_cache_line_size(
				__func__.exists_key("l2_cache_line_size", info)[1]
			),
			__types_nt__.cpu_cache_associativity(
				__func__.exists_key("l2_cache_associativity", info)[1]
			)
		)
		self.flags = []
		for i in info["flags"]:
			self.flags.append(i.upper())
	
	def get_load_all(self) -> __types_nt__.cpu_load_all:
		return __types_nt__.cpu_load_all(psutil.cpu_times_percent(), psutil.cpu_times())

	def get_load(self) -> __types_nt__.cpu_load:
		timesp, times = psutil.cpu_times_percent(), psutil.cpu_times()
		return __types_nt__.cpu_load(round((times.user + times.system + times.interrupt + times.dpc), 4), round(100 - timesp.idle, 1))

class RAM():
	def __init__(self) -> None:
		if platform.system() == 'Windows':
			self.memory_cards = __func__.get_memory_info_nt()
		else:
			self.memory_cards = None

	def get_status(self) -> psutil.virtual_memory():
		return psutil.virtual_memory()

class GPU():
	def __init__(self) -> None:
		if platform.system() == 'Windows':
			self.videocards = __func__.get_videocards_info_nt()
		else:
			self.videocards = None

class Motherboard():
	def __init__(self) -> None:
		if platform.system() == 'Windows':
			self.info = __func__.get_motherboard_info_nt()
		else:
			self.info = None

class Monitors():
	def __init__(self) -> None:
		self.displays = __func__.get_monitors_info_nt()

class BIOS():
	def __init__(self) -> None:
		if platform.system() == 'Windows':
			self.info = __func__.get_bios_info_nt()
		else:
			self.info = None