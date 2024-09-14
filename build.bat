@echo off

pyinstaller --noconfirm hterm.spec

xcopy /y /q /S /E /I ".\hterm\images" ".\dist\hterm\images"
xcopy /y /q /S /E /I ".\hterm\profile" ".\dist\hterm\profile"
xcopy /y /q /S /E /I ".\hterm\schemes" ".\dist\hterm\schemes"

pause