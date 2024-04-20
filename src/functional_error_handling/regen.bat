echo OFF
del *_modified.py
del *_temp.py
cls
echo --- Remove all 'console ==' outputs, regenerate them, and test everything ---
python .\update_output.py * --clear
: rye test
python .\update_output.py *
rye test
