@echo off
nasm -f win32 main.asm -o main.obj
if errorlevel 1 pause & exit /b
nasm -f win32 utils.asm -o utils.obj
if errorlevel 1 pause & exit /b
gcc main.obj utils.obj -o program.exe
if errorlevel 1 pause & exit /b
chcp 1251
echo Сборка успешно завершена!
program.exe
pause