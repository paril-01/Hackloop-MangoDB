@echo off
REM Git setup and CI trigger script for REPLIKA (Windows)

echo 🚀 REPLIKA - Git Setup ^& CI Trigger
echo ==================================

REM Check if git is initialized
if not exist ".git" (
    echo 📁 Initializing Git repository...
    git init
    echo ✅ Git initialized
)

REM Add .gitignore if it doesn't exist
if not exist ".gitignore" (
    echo 📝 Creating .gitignore...
    (
    echo # Python
    echo __pycache__/
    echo *.py[cod]
    echo *$py.class
    echo .Python
    echo build/
    echo dist/
    echo *.egg-info/
    echo.
    echo # Virtual environments
    echo .env
    echo .venv
    echo env/
    echo venv/
    echo.
    echo # Database
    echo *.db
    echo *.sqlite3
    echo.
    echo # Node.js
    echo node_modules/
    echo package-lock.json
    echo npm-debug.log*
    echo.
    echo # Build outputs
    echo dist/
    echo build/
    echo.
    echo # IDE
    echo .vscode/
    echo .idea/
    echo.
    echo # Test outputs
    echo test-results/
    echo playwright-report/
    echo.
    echo # Logs
    echo *.log
    ) > .gitignore
    echo ✅ .gitignore created
)

REM Stage all files
echo 📦 Staging files...
git add .

REM Commit changes
echo 💾 Committing changes...
git commit -m "Complete REPLIKA implementation - Ready for production"

REM Check if remote exists
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo 🌐 Remote origin configured
    echo 🚀 Pushing to trigger CI...
    git push
    echo ✅ Pushed to GitHub - CI will run shortly
) else (
    echo ⚠️  No remote origin configured
    echo.
    echo 📋 To push to GitHub:
    echo 1. Create repository on GitHub
    echo 2. Run: git remote add origin https://github.com/USERNAME/REPO.git
    echo 3. Run: git push -u origin main
)

echo.
echo 🎉 Setup complete! Project ready for CI validation.
pause
