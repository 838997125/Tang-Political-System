# JSON Helper - Use Python for proper JSON formatting

function Save-JsonWithPython($data, $filepath) {
    # Create temporary JSON file
    $tempFile = [System.IO.Path]::GetTempFileName() + ".json"
    $data | ConvertTo-Json -Depth 10 | Set-Content $tempFile -Encoding UTF8
    
    # Use Python to reformat
    $pythonScript = @"
import json
import sys
with open('$tempFile', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
with open('$filepath', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')
"@
    $pythonScript | py -
    
    # Clean up temp file
    Remove-Item $tempFile -ErrorAction SilentlyContinue
}
