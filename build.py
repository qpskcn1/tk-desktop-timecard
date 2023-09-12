#!/usr/bin/env python3

"""
build ui files, and resources for the app
"""
import os
import sys
import shutil
import glob
import subprocess

uic_bin = shutil.which("pyside2-uic")
rcc_bin = shutil.which("pyside2-rcc")

if not uic_bin:
    print("pyside2-uic not found.  Please install PySide2")
    sys.exit(1)

if not rcc_bin:
    print("pyside2-rcc not found.  Please install PySide2")
    sys.exit(1)


script_directory = os.path.dirname(os.path.realpath(__file__))
resources_directory = os.path.join(script_directory, "resources")
output_directory = os.path.join(script_directory, "python", "tk_desktop_timecard", "ui")
os.makedirs(output_directory, exist_ok=True)
open(os.path.join(output_directory, "__init__.py"), "w").close()

for ui_file in glob.glob(os.path.join(resources_directory, "*.ui")):
    print(f"Building UI file: {os.path.basename(ui_file)}")
    output_file = os.path.join(
        output_directory, os.path.basename(ui_file).replace(".ui", ".py")
    )
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    subprocess.check_call([uic_bin, ui_file, "--from-imports", "-o", output_file])

source_resources_file = os.path.join(resources_directory, "resources.qrc")
target_resources_file = os.path.join(output_directory, "resources_rc.py")
print(f"Building resources file: {os.path.basename(source_resources_file)}")
subprocess.check_call([rcc_bin, source_resources_file, "-o", target_resources_file])

print("Done")
