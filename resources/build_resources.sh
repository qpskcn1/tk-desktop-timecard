UI_PYTHON_PATH=../python/tk_desktop_timecard/ui

if [[-d $UI_PYTHON_PATH]]; then
    rm -rf $UI_PYTHON_PATH
fi

mkdir -p $UI_PYTHON_PATH
touch $UI_PYTHON_PATH/__init__.py

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
    py_file=$UI_PYTHON_PATH/${ui_file%.*}.py
    echo " > Compiling $ui_file -> $py_file"
    pyside2-uic --from-imports $ui_file > $py_file
    
done

echo 'Compiling resource files...'
pyside2-rcc resources.qrc > $UI_PYTHON_PATH/resources_rc.py

echo 'Done!'

