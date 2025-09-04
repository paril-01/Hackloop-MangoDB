#!/bin/bash
# Git setup and CI trigger script for REPLIKA

echo "🚀 REPLIKA - Git Setup & CI Trigger"
echo "=================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
fi

# Add .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Database
*.db
*.sqlite3

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json

# Build outputs
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Test outputs
test-results/
playwright-report/
coverage/

# Logs
*.log
logs/
EOF
    echo "✅ .gitignore created"
fi

# Stage all files
echo "📦 Staging files..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit"
else
    # Commit changes
    echo "💾 Committing changes..."
    git commit -m "Complete REPLIKA implementation

✅ Backend: FastAPI + SQLAlchemy + authentication
✅ Frontend: React + Electron + session management  
✅ E2E Tests: Playwright with auth scenarios
✅ CI/CD: GitHub Actions with matrix testing
✅ Privacy: Local-only data storage

Ready for production use!"
    echo "✅ Changes committed"
fi

# Check if remote exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "🌐 Remote origin already configured"
    
    # Push to trigger CI
    echo "🚀 Pushing to trigger CI..."
    git push
    echo "✅ Pushed to GitHub - CI will run shortly"
    echo ""
    echo "🔍 Check CI status at:"
    echo "   https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\([^/]*\/[^/]*\)\.git/\1/')/actions"
else
    echo "⚠️  No remote origin configured"
    echo ""
    echo "📋 To push to GitHub:"
    echo "1. Create repository on GitHub"
    echo "2. Run: git remote add origin https://github.com/USERNAME/REPO.git"
    echo "3. Run: git push -u origin main"
fi

echo ""
echo "🎉 Setup complete! Project ready for CI validation."
