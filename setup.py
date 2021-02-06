# from cx_Freeze import setup, Executable
# import sys

# # Dependencies are automatically detected, but it might need
# # fine tuning.
# build_options = {'packages': ['os', 'sys'], 'excludes': []}


# base = 'Win32GUI' if sys.platform=='win32' else None

# executables = [
#     Executable('app.py', base=base)
# ]


# setup(name='Connect6',
#       version = '1.0',
#       description = 'Bleum',
#       options = {'build_exe': build_options},
#       executables = executables)


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
    name        = 'Sillock',
    version     = '1.0',
    author      = "XENIA & CATNAP",
    description = "Sillock Verifier Client",
    options     = dict(build_exe = buildOptions),
    executables = exe
)