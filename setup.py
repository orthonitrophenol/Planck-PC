import sys
from cx_Freeze import setup, Executable


base = None
if (sys.platform == "win32"):
    base = "Win32GUI"   

build_exe_options = {
    "build_exe": "downloads/PlanckWindows",
    "zip_include_packages": ["PyQt5", "asyncio", "qasync"],
}

setup(
    name='Planck',
    version='0.1',
    description='Connecting the world faster than ever.',
    executables = [Executable("Planck.py", base=base)],
    options = {"build_exe": build_exe_options}
)



