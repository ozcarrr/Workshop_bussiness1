# GROUP_01_C1 · Mental-health emergency visits, community follow-up and acute psychiatric beds by Health Service (Chile, 2024)

Business Intelligence (IIB423T-1), Universidad del Desarrollo.
Instructor: Carlos Elías Pérez Pizarro.

| Item | Value |
|---|---|
| Group ID | 01 |
| Members | Benjamín Buzeta, Oscar Pichuman Millape, Felipe Alfredo Tajan Gebauer |
| Submission | 30 September 2026, version C1-1.0 |
| Previous stage | W1, submitted 24 September 2026 |

## Package contents

| Path | Role | Type |
|---|---|---|
| `report/GROUP_01_C1_Report.pdf` | Self-contained report, including the Process record | Deliverable |
| `presentation/GROUP_01_C1_Slides.pdf` | Presentation slides | Deliverable |
| `analysis/extract_c1_inputs.py` | Builds the reduced inputs in `data/` from the DEIS downloads | Script |
| `analysis/c1_mental_health_services.ipynb` | C1 analysis, executed with saved outputs | Notebook |
| `analysis/workshop1.ipynb` | W1 notebook, kept as the W1 record; not re-run for C1 | Notebook (W1) |
| `report/GROUP_01_C1_Report.md` | Report source | Source |
| `report/build_report_pdf.py`, `report/report.css` | Render the report PDF | Script |
| `report/figures/fig1`–`fig4` | Figures written by the notebook | Output |
| `presentation/GROUP_01_C1_Slides.html` | Slides source | Source |

### `data/`

| File | Kind | Source and scope |
|---|---|---|
| `sadu_2024_mental_health_extract.csv.gz` | Extracted input (unchanged lines) | `AtencionesUrgencia2024.csv`; `IdCausa` in 1, 7, 8, 22, 23, 25, 27, 28, 32, 33, 35–42; 4,037,964 of 8,973,229 rows |
| `rem20_2024_psychiatry_extract.csv` | Extracted input (unchanged lines) | `indicadores_rem20_20260825.csv`; `PERIODO` = 2024 and psychiatric functional areas; 934 of 167,405 rows |
| `rem_a06_2024_mh_controls_extract.csv` | Extracted input (unchanged lines) | `REMS/SERIE_REM_2024/Datos/SerieA2024.csv`; 10 codes of sheet A06 section A.1; 72,522 of 6,559,080 rows |
| `establecimientos_20260910.csv` | Original input | DEIS facility registry, snapshot 2026-09-10 (full file) |
| `facility_join_check.csv` | Processed output | One row per SADU facility with the code system matched and the registry Health Service |
| `health_service_labels.csv` | Processed output | Health Service code with SADU and REM20 names |
| `health_service_profile_2024.csv` | Processed output | Indicators per Health Service (report Table A1) |
| `health_service_screen_2024.csv` | Processed output | Emergency, community and hospital flags per Health Service |

The original SADU (1.6 GB) and REM Serie A (675 MB) files are not included.
They are the DEIS open-data downloads distributed as course files. The
versions used are named above; REM20 was downloaded on 25 August 2026.
The W1 reduced files (`reduced_*.csv`) are not used in C1.

## Software

- Analysis notebook: Python 3.11.15, pinned in `requirements.txt`.
- Extraction script: standard library only; run with Python 3.10.12.
- Report PDF: pandoc 3.1.3 and a Chromium-based browser.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run order

All paths are relative to the package root.

1. Optional, only to rebuild `data/` from the original downloads:

   ```bash
   python analysis/extract_c1_inputs.py PATH/TO/RAW_DIR
   ```

   `RAW_DIR` must contain `AtencionesUrgencia/AtencionesUrgencia2024.csv`,
   `indicadores_rem20_20260825.csv` and
   `REMS/SERIE_REM_2024/Datos/SerieA2024.csv`. Each step can be run on its
   own by adding `rem20`, `a06` or `sadu`.
2. Open `analysis/c1_mental_health_services.ipynb` from the `analysis/`
   folder and run all cells. It reads `data/` and writes the processed
   tables and `report/figures/`.
3. Optional, to rebuild the report PDF:

   ```bash
   python report/build_report_pdf.py
   ```

   Set `CHROME` to the browser executable if `chromium` is not on `PATH`.

## Known issues

- The DEIS 2024 establishment list could not be downloaded from our
  environment, so network membership in 2024 was not cross-checked. The
  2026 registry was used; report section 4.3 describes the effect.
- `analysis/workshop1.ipynb` needs the W1 reduced files, which are not in
  this package. Its saved outputs are the W1 record.
