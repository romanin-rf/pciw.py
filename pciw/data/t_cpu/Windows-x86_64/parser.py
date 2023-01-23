import os
import elevate
import subprocess


elevate.elevate(False, False)
LOCALDIR_PATH = os.path.dirname(__file__)
with open(os.path.join(LOCALDIR_PATH, "req.log"), "wb") as file:
    file.write(subprocess.check_output(os.path.join(LOCALDIR_PATH, "t_cpu.exe")))
