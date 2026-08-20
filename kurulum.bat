@echo off
chcp 65001 > nul
echo ===================================================
echo Yerel RAG Projesi Otomatik Kurulum Araci
echo ===================================================
echo.

echo [1/3] Gerekli klasorler hazirlaniyor...
if not exist "data" (
    mkdir data
    echo - 'data' klasoru olusturuldu. PDF'leri buraya atacaksiniz.
) else (
    echo - 'data' klasoru zaten mevcut.
)

if not exist "db" (
    mkdir db
    echo - 'db' klasoru olusturuldu.
) else (
    echo - 'db' klasoru zaten mevcut.
)
echo.

echo [2/3] Python kontrol ediliyor...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo HATA: Bilgisayarda Python bulunamadi! Lutfen Python yukleyin.
    pause
    exit /b
)
echo - Python basariyla algilandi.
echo.

echo [3/3] Kutuphaneler kuruluyor...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo HATA: requirements.txt bulunamadi!
    pause
    exit /b
)
echo.

echo ===================================================
echo KURULUM TAMAMLANDI!
echo ===================================================
echo Simdi 'data' klasorune PDF'lerinizi atip 'start_rag.bat' ile baslatabilirsiniz.
pause