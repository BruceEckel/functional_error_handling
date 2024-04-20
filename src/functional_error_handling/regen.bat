echo OFF
cls
del *modified.py
del *temp.py
echo --- Remove all 'console ==' outputs, regenerate them, and test everything ---
python .\update_output.py * --clear
: rye test
python .\update_output.py *
rye test
