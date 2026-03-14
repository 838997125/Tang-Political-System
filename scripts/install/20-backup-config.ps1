# Step 20: Backup Configuration

function Backup-Config {
    Info "Backing up configuration..."
    $bf = "$script:OC_CFG.bak.$(Get-Date -f 'yyyyMMdd-HHmmss')"
    Copy-Item $script:OC_CFG $bf
    Log "Backup: $bf"
}
