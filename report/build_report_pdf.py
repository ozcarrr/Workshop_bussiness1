"""Render report/GROUP_01_C1_Report.md to PDF.

Requires pandoc and a Chromium-based browser (Chrome, Edge or Chromium).
Set CHROME to the browser executable if it is not on PATH as `chromium`.

    python report/build_report_pdf.py
"""

import os
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "GROUP_01_C1_Report.md"
HTML = HERE / "GROUP_01_C1_Report.html"
PDF = HERE / "GROUP_01_C1_Report.pdf"
CSS = HERE / "report.css"

chrome = os.environ.get("CHROME") or shutil.which("chromium") or shutil.which("google-chrome")
if chrome is None:
    raise SystemExit("Set CHROME to a Chromium-based browser executable.")

subprocess.run(["pandoc", str(SRC), "--standalone", "--embed-resources",
                "--css", str(CSS), "--resource-path", str(HERE),
                "--metadata", "lang=en", "-o", str(HTML)], check=True)
subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", f"--print-to-pdf={PDF}",
                HTML.as_uri()], check=True)
HTML.unlink()
print(f"written {PDF.relative_to(HERE.parent)}")
