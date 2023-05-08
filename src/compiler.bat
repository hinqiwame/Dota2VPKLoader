@echo off
echo [~] Compiling Dota2VPKLoader...
pyinstaller -F --onefile --icon=NONE main.py
echo [+] Done.
pause
