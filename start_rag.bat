@echo off
cd /d "%~dp0"

title LOCAL RAG

echo ========================================
echo        LOCAL RAG BASLATILIYOR
echo ========================================
echo.

echo Foundry Local baslatiliyor...
foundry server start

echo.
echo Foundry durumu kontrol ediliyor...
echo.

for /f "tokens=3" %%A in ('foundry server status ^| findstr "Web URLs"') do set FOUNDRY_URL=%%A

if "%FOUNDRY_URL%"=="" (
    echo.
    echo Foundry adresi bulunamadi!
    pause
    exit /b
)

echo Foundry adresi:
echo %FOUNDRY_URL%

echo.
echo Phi-4 modeli yukleniyor...
foundry model load Phi-4-mini-instruct-generic-cpu

echo.
echo Phi-4 hazir.
echo.

echo FOUNDRY_URL=%FOUNDRY_URL%/v1 > .env
echo FOUNDRY_API_KEY=foundry >> .env
echo CHAT_MODEL=Phi-4-mini-instruct-generic-cpu >> .env

echo Python ortami baslatiliyor...
echo.

call "%~dp0venv\Scripts\activate.bat"

python "%~dp0src\main.py"

echo.
echo ========================================
echo       PROGRAM SONLANDI
echo ========================================
echo.

pause