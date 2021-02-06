from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ['os', 'sys'], 'excludes': []}


base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('app.py', base=base)
]


setup(name='Connect6',
      version = '1.0',
      description = 'Bleum',
      options = {'build_exe': build_options},
      executables = executables)
