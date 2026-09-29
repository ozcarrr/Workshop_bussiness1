"""Build the reduced C1 inputs in data/ from the original DEIS downloads.

Usage:
    python analysis/extract_c1_inputs.py RAW_DIR [rem20|a06|sadu ...]

RAW_DIR must contain:
    AtencionesUrgencia/AtencionesUrgencia2024.csv
    indicadores_rem20_20260825.csv
    REMS/SERIE_REM_2024/Datos/SerieA2024.csv

Lines are filtered on one field and copied unchanged (re-encoded to UTF-8).
Without step names, all three extracts are built.
"""

import gzip
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data"

# SADU cause IDs (DICCIONARIO_ATENCIONES_DE_URGENCIA.xlsx, Anexo 1).
# 1 = all emergency visits; 35-41 = mental-health visit causes;
# 25 = hospitalisations from the ED, split by cause into 7, 8, 22, 23, 32,
# 33 and 42 (mental disorders); 27/28 = patients waiting for a bed.
SADU_CAUSES = {"1", "7", "8", "22", "23", "25", "27", "28", "32", "33",
               "35", "36", "37", "38", "39", "40", "41", "42"}

# REM A06 section A.1: mental-health follow-up visits ("controles"),
# one code per professional (DICCIONARIO CODIGOS SA_24_V1.1.xlsm, sheet A06).
REM_A06_A1_CODES = {
    "06020201", "06020208", "06020202", "06020602", "06020206",
    "06200400", "06904900", "06200500", "06200501", "06905912",
}


def filter_lines(src, dest, field_index, keep, encoding, opener=open):
    """Copy the header and every line whose field `field_index` is in `keep`."""
    rows_in = rows_out = 0
    with open(src, encoding=encoding, newline="") as fin, \
            opener(dest, "wt", encoding="utf-8", newline="") as fout:
        fout.write(fin.readline())
        for line in fin:
            rows_in += 1
            if line.split(";", field_index + 1)[field_index] in keep:
                fout.write(line)
                rows_out += 1
    print(f"{src.name}: {rows_in:,} rows read, {rows_out:,} kept "
          f"-> {dest.name}", flush=True)


def extract_rem20(raw_dir):
    dest = OUT_DIR / "rem20_2024_psychiatry_extract.csv"
    filter_lines(raw_dir / "indicadores_rem20_20260825.csv", dest,
                 field_index=0, keep={"2024"}, encoding="utf-8")
    lines = dest.read_text(encoding="utf-8").splitlines(keepends=True)
    kept = [lines[0]] + [ln for ln in lines[1:]
                         if "psiquiatr" in ln.split(";")[7].lower()]
    dest.write_text("".join(kept), encoding="utf-8")
    print(f"  psychiatry functional areas: {len(kept) - 1:,} rows kept",
          flush=True)


def extract_a06(raw_dir):
    filter_lines(raw_dir / "REMS" / "SERIE_REM_2024" / "Datos" /
                 "SerieA2024.csv",
                 OUT_DIR / "rem_a06_2024_mh_controls_extract.csv",
                 field_index=4, keep=REM_A06_A1_CODES, encoding="latin1")


def extract_sadu(raw_dir):
    filter_lines(raw_dir / "AtencionesUrgencia" / "AtencionesUrgencia2024.csv",
                 OUT_DIR / "sadu_2024_mental_health_extract.csv.gz",
                 field_index=2, keep=SADU_CAUSES, encoding="latin1",
                 opener=gzip.open)


STEPS = {"rem20": extract_rem20, "a06": extract_a06, "sadu": extract_sadu}

if __name__ == "__main__":
    raw = Path(sys.argv[1])
    for name in sys.argv[2:] or STEPS:
        t0 = time.time()
        STEPS[name](raw)
        print(f"  {name} done in {time.time() - t0:.0f}s", flush=True)
