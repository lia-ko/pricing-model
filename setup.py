from cx_Freeze import setup, Executable
import sys
import os

includes = []
include_files = [r"C:\Python36-32\DLLs\tcl86t.dll",
                 r"C:\Python36-32\DLLs\tk86t.dll"]

base = 'Win32GUI'

executables = [Executable("dialog.py", base=base)]

packages = ["idna", "numpy", "scipy", "tkinter", "tkinter.ttk", "_tkinter", "sys"]
options = {
    'build_exe': {
        'includes': includes, 'include_files': include_files,
        'packages':packages,
    },
}

os.environ['TCL_LIBRARY'] = r'C:\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python36-32\tcl\tk8.6'

setup(
    name = "PricingApp",
    options = options,
    version = "1.0.0",
    description = 'Option pricing app',
    executables = executables
)