@echo off
REM ========================================
REM Build Completo do Unipulso
REM Cria executavel + instalador em 1 passo
REM ========================================

echo.
echo ========================================
echo   UNIPULSO - BUILD COMPLETO
echo   Executavel + Instalador
echo ========================================
echo.

REM Verificar se esta na pasta correta
if not exist "app.py" (
    echo [ERRO] app.py nao encontrado!
    echo Execute este script na raiz do projeto.
    pause
    exit /b 1
)

REM Ativar ambiente virtual se existir
if exist ".venv\Scripts\activate.bat" (
    echo [1/4] Ativando ambiente virtual...
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    echo [1/4] Ativando ambiente virtual...
    call venv\Scripts\activate.bat
) else (
    echo [AVISO] Ambiente virtual nao encontrado
    echo Continuando com Python global...
)

echo.
echo ========================================
echo [2/4] Construindo executavel...
echo ========================================
echo.

REM Executar build do executavel
python build_exe.py
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao criar executavel!
    pause
    exit /b 1
)

echo.
echo ========================================
echo [3/4] Criando instalador...
echo ========================================
echo.

REM Executar build do instalador
python build_installer.py
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao criar instalador!
    pause
    exit /b 1
)

echo.
echo ========================================
echo [4/4] Build concluido com sucesso!
echo ========================================
echo.
echo Executavel: dist\Unipulso.exe
echo Instalador: installer_output\Unipulso_Setup_v1.0.0.exe
echo.
echo Pronto para distribuicao!
echo.

pause
