@echo off
color a
echo Where do you want to go?
echo.
echo Login Data [1]
echo.

set /p first=

if %first% == 1 goto login_data

pause
exit

:login_data
cls
echo From here, what do you want to do?
echo.
echo Retrieve Data (1)
echo Upload Data (2)
echo Delete Data (3)
echo.

set /p login=

if %login% == 1 goto login_data_retrieve
if %login% == 2 goto login_data_upload
if %login% == 3 goto login_data_delete


:login_data_retrieve
cls
echo See data in terminal (1)
echo Export data to excel file (2)
set /p method=

if %method% == 1 goto login_data_retrieve1
if %method% == 2 goto login_data_retrieve2

:login_data_retrieve1
cls
py Mysql_Login_Data.py -r
pause
exit

:login_data_retrieve2
cls
py Mysql_Login_Data.py -e
pause
exit

:login_data_upload
cls
echo Add data manually (1)
echo Add data from file (2)
set /p method=
if %method% == 1 goto login_data_upload1
if %method% == 2 goto login_data_upload2

:login_data_upload1
cls
py Mysql_Login_Data.py -a
pause
exit

:login_data_upload2
cls
py Mysql_Login_Data.py -u
pause
exit

:login_data_delete
cls
py Mysql_Login_Data.py -d
pause
exit