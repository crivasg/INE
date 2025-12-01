@echo off 
setlocal

echo #............................................................#
echo #                                                            #
echo #                                                            #
echo #    INE                                                     #
echo #                                                            #
echo #                                                            #
echo #............................................................#
echo.

PUSHD %~dp0

if not exist "venv\Scripts\activate.bat" (
	echo.
	echo The virtal enviroment does not exist. 
	echo Will try to make the enviroment.
	echo.
	
	python -m venv venv
	call venv\Scripts\activate.bat
	python -m pip install -r requirements.txt
	:: python -m pip install --upgrade --force-reinstall -r requirements.txt
	call venv\Scripts\deactivate.bat
)

call venv\Scripts\activate.bat
python -m ine
call venv\Scripts\deactivate.bat

POPD

EXIT /B 0

:END_POINT
ECHO.
ECHO.
ECHO ... ERROR FOUND %DATE% %TIME% ...
ECHO.
ECHO.
