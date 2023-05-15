@echo off
echo [~] Компиляция Dota2VPKLoader...
pyinstaller -F --onefile --icon=NONE Dota2VPKLoader.py
rd /s /q build
del /q Dota2VPKLoader.spec
if not exist Compiled mkdir Compiled
move /y dist\*.* Compiled
rd /s /q dist
echo [+] Готово.
pause
