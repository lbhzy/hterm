@echo off

pyinstaller -y ^
-i images/icon.png ^
-p hterm/terminal;hterm/ui ^
-n Hterm ^
hterm/main.py

del *.spec

xcopy /y /q /S /E /I ".\hterm\images" ".\dist\hterm\images"
xcopy /y /q /S /E /I ".\hterm\profiles" ".\dist\hterm\profiles"
xcopy /y /q /S /E /I ".\hterm\schemes" ".\dist\hterm\schemes"

pause