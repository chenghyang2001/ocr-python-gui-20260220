"""本機打包腳本 — 使用 PyInstaller 建立 exe"""

import subprocess
import sys


def main():
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "ocr_app.spec",
        "--clean",
        "--noconfirm",
    ]
    print(f"執行: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print("\nDone! exe at dist/OCR-App.exe")
    else:
        print("\nBuild failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
