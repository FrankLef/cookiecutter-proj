@rem ==========================================================================
@rem Create PYTHONPATH and add the current directory to it.
@rem ==========================================================================
@rem This batch file will create the PYTHONPATH environment variable and
@rem add the folder in which it is located to PYTHONPATH
@rem If PYTHONPATH exists and the dir is already in it it will says so.
@rem If PYTHONPATH exists and the dir is NOT already in it it will says so.
cls
@rem next line is used to test, result should give ErrorLevel 1
@rem @set newdir=%~dp0Wrong
@set newdir=%~dp0
@if Not Defined PYTHONPATH (
	@echo [1;31mPYTHONPATH did not exist but is now set to this directory[0m
	@echo [1;93m%newdir%[0m
	set PYTHONPATH=%newdir%
	exit /b 0
)
@rem IMPORTANT, use %windir%\system32\FIND.exe to avoid conflict issues with cygwin, git, etc.
@rem That problem made me lose an entire day!
@echo ";%PYTHONPATH%;" | %windir%\system32\FIND.exe /i ";%newdir%;" > nul
@set FINDERROR=%ErrorLevel%
@if %FINDERROR%==0 (
	@echo [1;32mThis path is in PYTHONPATH[0m
	) else (
	@echo [1;31mThis path is NOT in PYTHONPATH[0m
	)
@echo [1;93m%newdir%[0m
