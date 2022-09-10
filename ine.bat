@echo off 
setlocal

cd /d %~dp0

echo #............................................................#
echo #                                                            #
echo #                                                            #
echo #    INE                                                     #
echo #                                                            #
echo #                                                            #
echo #............................................................#
echo.

call venv\Scripts\activate.bat
python -m ine
call venv\Scripts\deactivate.bat

echo.
