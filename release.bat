@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   OCR App - Build and Release
echo ========================================
echo.

:: ── 1. 從 pyproject.toml 讀取目前版本 ──
set "CURRENT_VERSION="
for /f "tokens=2 delims=^= " %%a in ('findstr /r "^version" pyproject.toml') do (
    set "CURRENT_VERSION=%%~a"
)

if "%CURRENT_VERSION%"=="" (
    echo ERROR: Cannot read version from pyproject.toml
    exit /b 1
)

echo Current version: %CURRENT_VERSION%

:: ── 2. 拆解版本號並遞增 patch ──
for /f "tokens=1,2,3 delims=." %%a in ("%CURRENT_VERSION%") do (
    set "MAJOR=%%a"
    set "MINOR=%%b"
    set "PATCH=%%c"
)

set /a PATCH=%PATCH%+1
set "NEW_VERSION=%MAJOR%.%MINOR%.%PATCH%"

echo New version:     %NEW_VERSION%
echo.

:: ── 3. 更新 pyproject.toml 中的版本號 ──
echo Updating pyproject.toml...
powershell -Command "(Get-Content pyproject.toml) -replace 'version = \"%CURRENT_VERSION%\"', 'version = \"%NEW_VERSION%\"' | Set-Content pyproject.toml"
if errorlevel 1 (
    echo ERROR: Failed to update pyproject.toml
    exit /b 1
)
echo Done.
echo.

:: ── 4. 打包 exe ──
echo Building exe with PyInstaller...
echo.
python -m PyInstaller ocr_app.spec --clean --noconfirm
if errorlevel 1 (
    echo.
    echo ERROR: PyInstaller build failed
    exit /b 1
)
echo.
echo Build successful: dist\OCR-App.exe
echo.

:: ── 5. Git commit, tag, push ──
echo Committing version bump...
git add pyproject.toml
git commit -m "release: v%NEW_VERSION%"
if errorlevel 1 (
    echo ERROR: Git commit failed
    exit /b 1
)

echo Creating tag v%NEW_VERSION%...
git tag "v%NEW_VERSION%"
if errorlevel 1 (
    echo ERROR: Git tag failed
    exit /b 1
)

echo Pushing to remote...
git push origin main --tags
if errorlevel 1 (
    echo ERROR: Git push failed
    exit /b 1
)

echo.
echo ========================================
echo   Release v%NEW_VERSION% complete!
echo   GitHub Actions will build and publish
echo   the release automatically.
echo ========================================
