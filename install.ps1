# install.ps1 — Installs all dependencies for render_mermaid_md.py
# Run with: powershell -ExecutionPolicy Bypass -File install.ps1

Write-Host "=== Installing dependencies for render_mermaid_md.py ===" -ForegroundColor Cyan

# Node.js (needed for mmdc)
Write-Host "`n[1/4] Installing Node.js..." -ForegroundColor Yellow
winget install OpenJS.NodeJS

# Pandoc
Write-Host "`n[2/4] Installing Pandoc..." -ForegroundColor Yellow
winget install JohnMacFarlane.Pandoc

# MiKTeX (provides xelatex)
Write-Host "`n[3/4] Installing MiKTeX (xelatex)..." -ForegroundColor Yellow
winget install MiKTeX.MiKTeX

# Mermaid CLI (mmdc) — installed via npm after Node.js
Write-Host "`n[4/4] Installing Mermaid CLI (mmdc)..." -ForegroundColor Yellow
Write-Host "NOTE: If Node.js was just installed in this session, close and reopen your terminal before running this step." -ForegroundColor Magenta
npm install -g @mermaid-js/mermaid-cli

Write-Host "`n=== Done! ===" -ForegroundColor Green
Write-Host "Run the script with: python render_mermaid_md.py"
