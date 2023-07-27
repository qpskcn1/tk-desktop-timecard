UI_PYTHON_PATH=../python/tk_desktop_timecard/ui

# if the pyside-uic and pyside-rcc commands are not on the path then print an error and exit
if ! which pyside2-uic > /dev/null 2>&1; then
    echo "ERROR: pyside-uic command was not found. Please ensure that the pyside package is installed."
    exit 1
fi

if ! which pyside2-rcc > /dev/null 2>&1; then
    echo "ERROR: pyside-rcc command was not found. Please ensure that the pyside package is installed."
    exit 1
fi

echo 'Compiling UI files...'
for ui_file in `ls *.ui`; do
    echo " > Compiling $ui_file"
    pyside2-uic --from-imports $ui_file > $UI_PYTHON_PATH/${ui_file%.*}.py
done

echo 'Compiling resource files...'
pyside2-rcc resources.qrc > $UI_PYTHON_PATH/resources_rc.py

echo 'Done!'



# function build_qt {
#     echo " > Building " $2

#     # compile ui to python
#     $1 $2 > $UI_PYTHON_PATH/$3.py

#     # replace PySide imports with sgtk.platform.qt and remove line containing Created by date
#     sed -i "" -e "s/from PySide import/from sgtk.platform.qt import/g" -e "/# Created:/d" $UI_PYTHON_PATH/$3.py
# }

# function build_ui {
#     build_qt "${PYTHON_BASE}/bin/python ${PYTHON_BASE}/bin/pyside-uic --from-imports" "$1.ui" "$1"
# }

# function build_res {
#     build_qt "${PYTHON_BASE}/bin/pyside-rcc" "$1.qrc" "$1_rc"
# }

# # build UI's:
# echo "building user interfaces..."
# build_ui dialog
# # add any additional .ui files you want converted here!
# build_ui my_time_form

# # build resources
# echo "building resources..."
# build_res resources
