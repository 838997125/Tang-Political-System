# Fix Encoding - Convert all text files to UTF-8 with BOM
param(
    [switch]$DryRun
)

$ErrorActionPreference = "Continue"

# File extensions to process
$extensions = @('.ps1', '.py', '.md', '.html', '.json', '.txt', '.js', '.css')

# Directories to skip
$skipDirs = @('node_modules', '.git', '__pycache__', '.obsidian', '.vite', 'dist')

function Add-Utf8Bom {
    param($filePath)
    
    try {
        # Read file content
        $content = [System.IO.File]::ReadAllText($filePath)
        
        # Check if already has BOM
        $bytes = [System.IO.File]::ReadAllBytes($filePath)
        $hasBom = ($bytes.Length -ge 3 -and 
                   $bytes[0] -eq 0xEF -and 
                   $bytes[1] -eq 0xBB -and 
                   $bytes[2] -eq 0xBF)
        
        if ($hasBom) {
            return "SKIP (already has BOM)"
        }
        
        if ($DryRun) {
            return "WOULD FIX"
        }
        
        # Write with BOM
        $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
        $bom = [System.Text.Encoding]::UTF8.GetPreamble()
        $fullBytes = $bom + $utf8Bytes
        [System.IO.File]::WriteAllBytes($filePath, $fullBytes)
        
        return "FIXED"
    }
    catch {
        return "ERROR: $_"
    }
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  UTF-8 BOM Encoding Fix Tool" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
    Write-Host ""
}

$repoDir = "D:\tools\Tang-Political-System"
$files = Get-ChildItem -Path $repoDir -Recurse -File | Where-Object {
    # Check extension
    $ext = $_.Extension.ToLower()
    $hasTargetExt = $extensions -contains $ext
    
    # Check if in skip directory
    $inSkipDir = $false
    foreach ($skip in $skipDirs) {
        if ($_.FullName -like "*\$skip\*") {
            $inSkipDir = $true
            break
        }
    }
    
    $hasTargetExt -and -not $inSkipDir
}

Write-Host "Found $($files.Count) files to check" -ForegroundColor Green
Write-Host ""

$fixed = 0
$skipped = 0
$errors = 0

foreach ($file in $files) {
    $result = Add-Utf8Bom -filePath $file.FullName
    
    switch -Regex ($result) {
        "^FIXED" { 
            $fixed++
            Write-Host "[FIXED] $($file.FullName.Replace($repoDir, '.'))" -ForegroundColor Green
        }
        "^SKIP" { 
            $skipped++
            # Don't show skipped files to reduce output
        }
        "^WOULD" { 
            Write-Host "[WOULD FIX] $($file.FullName.Replace($repoDir, '.'))" -ForegroundColor Yellow
        }
        default { 
            $errors++
            Write-Host "[ERROR] $($file.FullName.Replace($repoDir, '.')) - $result" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Summary" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Fixed:   $fixed" -ForegroundColor Green
Write-Host "Skipped: $skipped (already has BOM)" -ForegroundColor Gray
Write-Host "Errors:  $errors" -ForegroundColor Red
Write-Host ""

if (-not $DryRun -and $fixed -gt 0) {
    Write-Host "All files have been converted to UTF-8 with BOM encoding." -ForegroundColor Green
}
