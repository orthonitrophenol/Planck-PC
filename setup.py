import sys
from cx_Freeze import setup, Executable

base = None
if (sys.platform == "win32"):
    base = "Win32GUI"   

setup(
    name='Planck',
    version='0.1',
    description='Connecting the world faster than ever.',
    executables = [Executable("Planck.py", base=base)],
)



