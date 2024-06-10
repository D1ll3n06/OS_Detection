@ECHO OFF

setlocal enabledelayedexpansion



for /f "skip=4 tokens=*" %%a in ('net user') do (
    
    for %%b in (%%a) do (
    
        echo %%b
    )
)


Exit

