from cx_Freeze import setup, Executable
import sys

buildOptions = dict(packages      = ["qtmodern.windows", "qtmodern.styles", "os", "sys",], 
                    excludes      = [],
                    includes      = ["guiWindow"],
                    include_files = ["images"]
                    )

base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = [Executable("main.py", base=base)]

setup(
    name        = 'Connect6',
    version     = '1.0',
    author      = "Bleum",
    description = "Connect6",
    options     = dict(build_exe = buildOptions),
    executables = exe
)