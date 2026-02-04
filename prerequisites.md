# Prerequisites - Chemical Equipment Parameter Visualizer

## System Requirements

Before starting the project implementation, ensure the following software is installed on your PC.

---

## Required Software

### 1. Python (Version 3.9 or higher)

| | |
|---|---|
| **Download** | https://www.python.org/downloads/ |
| **Version** | 3.9+ (Recommended: 3.11 or 3.12) |
| **Important** | ✅ Check **"Add Python to PATH"** during installation |

**Verify Installation:**
```powershell
python --version
```

---

### 2. pip (Python Package Manager)

| | |
|---|---|
| **Included** | Comes with Python installation |
| **Update** | `python -m pip install --upgrade pip` |

**Verify Installation:**
```powershell
pip --version
```

---

### 3. Node.js (Version 18 LTS or higher)

| | |
|---|---|
| **Download** | https://nodejs.org/ |
| **Version** | 18 LTS or higher (Recommended: 20 LTS) |
| **Includes** | npm (Node Package Manager) |

**Verify Installation:**
```powershell
node --version
npm --version
```

---

### 4. Git

| | |
|---|---|
| **Download** | https://git-scm.com/downloads |
| **Purpose** | Version control & GitHub submission |

**Verify Installation:**
```powershell
git --version
```

---

### 5. virtualenv (Python Virtual Environment)

| | |
|---|---|
| **Install** | `pip install virtualenv` |
| **Purpose** | Create isolated Python environments for backend & desktop app |

**Verify Installation:**
```powershell
pip show virtualenv
```

---

## Recommended Software

### 6. Visual Studio Code (Code Editor)

| | |
|---|---|
| **Download** | https://code.visualstudio.com/ |
| **Purpose** | Code editing for Python, JavaScript, and more |

**Recommended VS Code Extensions:**
| Extension | Purpose |
|-----------|---------|
| Python | Python language support |
| Pylance | Python IntelliSense |
| ES7+ React/Redux/React-Native snippets | React code snippets |
| Prettier - Code formatter | Code formatting |
| GitLens | Git integration |
| REST Client | API testing within VS Code |

---

### 7. Postman (API Testing Tool)

| | |
|---|---|
| **Download** | https://www.postman.com/downloads/ |
| **Purpose** | Test Django REST API endpoints |
| **Alternative** | Thunder Client (VS Code extension) |

---

### 8. Web Browser with Developer Tools

| | |
|---|---|
| **Recommended** | Google Chrome or Mozilla Firefox |
| **Purpose** | Testing React frontend, debugging |
| **Access DevTools** | Press `F12` or `Ctrl + Shift + I` |

---

### 9. Screen Recording Software (For Demo Video)

| Option | Download |
|--------|----------|
| **OBS Studio** (Free) | https://obsproject.com/ |
| **Windows Game Bar** | Built-in, press `Win + G` |
| **Loom** (Free tier) | https://www.loom.com/ |

---

## Quick Verification Script

Run this in PowerShell to verify all required software:

```powershell
Write-Host "=== Checking Prerequisites ===" -ForegroundColor Cyan

Write-Host "`n1. Python:" -ForegroundColor Yellow
python --version

Write-Host "`n2. pip:" -ForegroundColor Yellow
pip --version

Write-Host "`n3. Node.js:" -ForegroundColor Yellow
node --version

Write-Host "`n4. npm:" -ForegroundColor Yellow
npm --version

Write-Host "`n5. Git:" -ForegroundColor Yellow
git --version

Write-Host "`n=== Verification Complete ===" -ForegroundColor Cyan
```

---

## Summary Checklist

| # | Software | Required | Status |
|---|----------|----------|--------|
| 1 | Python 3.9+ | ✅ Yes | ⬜ |
| 2 | pip | ✅ Yes | ⬜ |
| 3 | Node.js 18+ | ✅ Yes | ⬜ |
| 4 | npm | ✅ Yes | ⬜ |
| 5 | Git | ✅ Yes | ⬜ |
| 6 | virtualenv | ✅ Yes | ⬜ |
| 7 | VS Code | 📌 Recommended | ⬜ |
| 8 | Postman | 📌 Optional | ⬜ |
| 9 | Screen Recorder | 📌 For Demo | ⬜ |

---

## Installation Order

1. **Python** → Enables pip and backend development
2. **Node.js** → Enables npm and React development
3. **Git** → Enables version control
4. **virtualenv** → `pip install virtualenv`
5. **VS Code** → Code editor with extensions
6. **Postman** → API testing (optional)

---

## Troubleshooting

### Python not recognized in terminal
- Reinstall Python with **"Add to PATH"** checked
- Or manually add Python to System Environment Variables

### npm commands fail
- Run PowerShell as Administrator
- Or use: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

### Git not recognized
- Restart terminal after Git installation
- Or reinstall with **"Add to PATH"** option

---

## Next Steps

Once all prerequisites are installed and verified, proceed to:

📄 **[Implementation Plan](implementation_plan.md)** → Phase 1, Step 1.1

---

*Last Updated: February 2026*
