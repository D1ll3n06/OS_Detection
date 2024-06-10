@ECHO OFF
setlocal enabledelayedexpansion

set "LogName=Security"
set "Event1=4624"
set "Event2=4625"


powershell.exe -Command "get-localuser "





endlocal
exit /b 0