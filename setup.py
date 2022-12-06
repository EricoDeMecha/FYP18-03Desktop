import sys

from cx_Freeze import setup, Executable

base = "Win32GUI" if sys.platform == "win32" else None

build_exe_options= {
    "include_files": ['main.qml','controls/', 'icons/']
}

executables = [
        Executable (
            "main.py",
            copyright="Copyright  (C) 2022 cx_freeze",
            base=base,
            icon='icons/mainIcon.ico'
        )
]

setup(
    name = "FYP18-03 Aux Desktop",
    description="SHEM Embedded auxilliary desktop application",
    version="1.0.0",
    executables = executables,
    options= {
        "build_exe": build_exe_options,
    }
)