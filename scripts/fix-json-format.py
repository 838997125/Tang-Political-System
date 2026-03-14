#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix JSON formatting - reformat with proper indentation"""

import json
import sys
from pathlib import Path

def fix_json_file(filepath):
    """Reformat JSON file with proper indentation"""
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        
        print(f"Fixed: {filepath}")
        return True
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fix_json_file(sys.argv[1])
    else:
        # Fix openclaw.json
        openclaw_json = Path.home() / '.openclaw' / 'openclaw.json'
        if openclaw_json.exists():
            fix_json_file(str(openclaw_json))
        else:
            print(f"File not found: {openclaw_json}")
