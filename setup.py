import sys

from cx_Freeze import setup, Executable

try:
    from cx_Freeze.hooks import get_qt_plugins_paths
except ImportError:
    get_qt_plugins_paths = None

include_files = ['main.qml','controls/', 'icons/']
if get_qt_plugins_paths:
    # Inclusion of extra plugins (since cx_Freeze 6.8b2)
    # cx_Freeze imports automatically the following plugins depending of the
    # use of some modules:
    # imageformats, platforms, platformthemes, styles - QtGui
    # mediaservice - QtMultimedia
    # printsupport - QtPrintSupport
    for plugin_name in (
        # "accessible",
        # "iconengines",
        # "platforminputcontexts",
        # "xcbglintegrations",
        # "egldeviceintegrations",
        "wayland-decoration-client",
        "wayland-graphics-integration-client",
        # "wayland-graphics-integration-server",
        "wayland-shell-integration",
    ):
        include_files += get_qt_plugins_paths("PySide2", plugin_name)

base = "Win32GUI" if sys.platform == "win32" else None

msi_data = {
    "ProgId": [
        ('Prog.Id', None, None, "FYP18-03 Automation App", 'IconId', None),
    ],
    "Icon": [
        ("IconId", "icons/mainIcon.ico"),
    ],
}
bdist_msi_options = {
    "data": msi_data,
    "target_name": "SHEMApp",
}

build_exe_options= {
    "include_files": include_files,
    "excludes": ['tkinter'],
    "zip_include_packages": ["PySide2"],
}
executables = (
    [
        Executable (
            "main.py",
            copyright="Copyright  (C) 2022 cx_freeze",
            base="Win32GUI",
            icon='icons/mainIcon.ico'
        )
    ]
)

setup(
    name = "FYP18-03 Aux Desktop",
    description="SHEM Embedded auxilliary desktop application",
    version="1.0.0",
    executables = executables,
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    }
)