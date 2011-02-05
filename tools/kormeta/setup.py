from distutils.core import setup
import py2exe

dll_excludes = ['w9xpopen.exe']

setup(
    #console=['kormeta.py'],
    windows=['kormeta.py'],
    options = {"py2exe": {"compressed": 3,
                          "optimize": 2,
                          "dll_excludes": dll_excludes,
                          "ascii": False,
                         }
              }
    )
