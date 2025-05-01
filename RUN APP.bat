@echo off
cd /d "%~dp0"\AIMS-Web\AIMS-Web
call env\Scripts\activate
python manage.py runserver 172.16.1.15:8000
pause
