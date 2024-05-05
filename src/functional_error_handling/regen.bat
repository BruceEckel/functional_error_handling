echo OFF
del *_modified.py
cls
echo --- Remove all 'console ==' outputs, regenerate them, and test everything ---
python .\update_output.py * --clear
@REM rye test
python .\update_output.py *
rye test
