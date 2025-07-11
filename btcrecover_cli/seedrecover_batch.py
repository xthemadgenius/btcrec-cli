#!/usr/bin/env python3
"""
Direct seedrecover_batch.py entry point for CLI compatibility
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Main entry point that mirrors the original seedrecover_batch.py"""
    script_path = Path(__file__).parent.parent / "seedrecover_batch.py"
    
    if not script_path.exists():
        print(f"Error: seedrecover_batch.py not found at {script_path}", file=sys.stderr)
        return 1
    
    # Pass all arguments directly to the original script
    cmd = [sys.executable, str(script_path)] + sys.argv[1:]
    
    try:
        result = subprocess.run(cmd, cwd=script_path.parent)
        return result.returncode
    except KeyboardInterrupt:
        return 130
    except Exception as e:
        print(f"Error running seedrecover_batch: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())