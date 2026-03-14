# Step 60: Copy Cheatsheet

function Copy-Cheatsheet {
    Info "Copying CHEATSHEET.md to user workspace..."
    $src = "$REPO_DIR\CHEATSHEET.md"
    $dst = "$script:DefWorkspace\CHEATSHEET.md"
    if (Test-Path $src) {
        Copy-Item $src $dst -Force
        Log "CHEATSHEET.md copied"
    }
}
