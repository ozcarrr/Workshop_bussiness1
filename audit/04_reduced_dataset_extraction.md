# Reduced Dataset Extraction Specifications & Pipeline

## 1. Context & Architectural Rationale
In accordance with Course Assessment Protocol 04 (Packaging & Reproducibility) and Task 1.4 of `.instructions.md`, raw data files exceeding hundreds of megabytes (such as the 1.2 GB `AtencionesUrgencia2024.csv` and multi-year discharge repositories) must not be bundled directly into university evaluation archives.

Instead, a deterministic, fully reproducible Python pipeline (`audit/extract_reduced_datasets.py`) was developed and executed to extract three reduced, focused test datasets directly into `data/`. These subsets preserve all necessary clinical, temporal, and spatial variables required to explore both candidate lines (Respiratory Strain vs. Mental Health Crisis).

---

## 2. Reduced Datasets Inventory

| Generated File Name | Path in Repository | Source Raw Dataset | Filtering Logic & Inclusion Criteria | Extracted Rows | Extracted Size |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`reduced_urgencias_2024_sample.csv`** | `data/reduced_urgencias_2024_sample.csv` | `data/AtencionesUrgencia/AtencionesUrgencia2024.csv` | Filtered for 13 target causes:<br>- Respiratory: `IdCausa` in `[2, 3, 4, 5, 10, 11]`<br>- Mental Health: `IdCausa` in `[35, 36, 37, 38, 39, 40]`<br>- Hospital Admissions: `IdCausa == 25`<br>- Sanitized facility identifiers (`.str.strip()`). | **2,916,297 rows** (32.50% of 8.97M raw rows) | **543.03 MB** (UTF-8 encoded) |
| **`reduced_rem20_critical_psych.csv`** | `data/reduced_rem20_critical_psych.csv` | `data/indicadores_rem20_20260825.csv` | Filtered for calendar year `PERIODO == 2024` and functional areas matching Critical Care (`Intensiv`, `Intermed`) or Psychiatry (`Psiquiatr`). Codes: 405, 406, 411, 412, 414, 415, 418-426, 428-429. | **4,322 rows** | **0.70 MB** (UTF-8 encoded) |
| **`reduced_establecimientos.csv`** | `data/reduced_establecimientos.csv` | `data/establecimientos_20260910.csv` | Facilities satisfying at least one criterion:<br>1. Emergency services: `TieneServicioUrgencia == 'SI'`<br>2. General hospitals: `TipoEstablecimientoGlosa == 'Hospital'`<br>3. Reporting beds in REM20. | **838 facilities** (out of 5,743) | **0.37 MB** (UTF-8 encoded) |

---

## 3. Extracted Distributions in Reduced Data

### 3.1. SADU 2024 Cause Breakdown
In `data/reduced_urgencias_2024_sample.csv`, consultations are distributed across the 13 clinical categories as follows:

| IdCausa | Clinical Cause Description | Target Line | Total Consultations 2024 | Row Count |
| :--- | :--- | :--- | :--- | :--- |
| **2** | TOTAL CAUSAS SISTEMA RESPIRATORIO | Line A (Respiratory) | 5,541,628 | 224,330 |
| **3** | Bronquitis/bronquiolitis aguda (J20-J21) | Line A (Pediatric Respiratory) | 840,273 | 224,330 |
| **4** | Influenza (J09-J11) | Line A (Viral Epidemic) | 125,153 | 224,330 |
| **5** | Neumonía (J12-J18) | Line A (Severe Respiratory) | 266,049 | 224,330 |
| **10** | IRA Alta (J00-J06) | Line A (Upper Respiratory) | 3,753,066 | 224,330 |
| **11** | Crisis obstructiva bronquial (J40-J46) | Line A (Obstructive Respiratory) | 199,959 | 224,330 |
| **25** | SECCIÓN 2. TOTAL DE HOSPITALIZACIONES | Benchmark Capacity | 633,303 | 224,331 |
| **35** | Lesiones autoinfligidas intencionalmente (X60-X84) | Line B (Mental Health / Crisis) | 9,753 | 224,331 |
| **36** | TOTAL CAUSAS DE TRASTORNOS MENTALES (F00-F99) | Line B (Mental Health Aggregate) | 305,432 | 224,331 |
| **37** | Ideación Suicida (R45.8) | Line B (Suicide Risk) | 12,433 | 224,331 |
| **38** | Trastornos por sustancias psicoactivas (F10-F19) | Line B (Substance Abuse) | 28,633 | 224,331 |
| **39** | Trastornos del Humor (Afectivos) (F30-F39) | Line B (Affective Disorders) | 30,634 | 224,331 |
| **40** | Trastornos neuróticos y estrés (F40-F48) | Line B (Anxiety / Stress / Panic) | 173,931 | 224,331 |

### 3.2. REM20 2024 Functional Ward Distribution
In `data/reduced_rem20_critical_psych.csv`, records are categorized into 16 distinct high-acuity functional wards:
- **Cuidados Intermedios Adultos (UTI)**: 881 facility-months
- **Cuidados Intensivos Adultos (UCI)**: 752 facility-months
- **Cuidados Intermedios Pediátricos (UTI)**: 504 facility-months
- **Neonatología Intermedia**: 480 facility-months
- **Neonatología Intensiva**: 422 facility-months
- **Cuidados Intensivos Pediátricos (UCI)**: 349 facility-months
- **Psiquiatría Adulto Corta estadía**: 330 facility-months
- **Psiquiatría Infanto-adolescente corta estadía**: 248 facility-months
- **Cuidados Intensivos en Psiquiatría Adulto**: 108 facility-months
- **Cuidados Intensivos en Psiquiatría Infanto Adolescente**: 59 facility-months
- **Psiquiatría Forense Adulto (Evaluación / Tratamiento)**: 81 facility-months
- **Psiquiatría Adulto (Mediana / Larga estadía)**: 72 facility-months
- **Psiquiatría Forense Infanto Adolescente**: 24 facility-months
- **Psiquiatría Infanto-adolescente mediana estadía**: 12 facility-months

### 3.3. Establecimientos Facility Typology
In `data/reduced_establecimientos.csv`, the 838 facilities comprise:
- **SAPU**: 259 facilities
- **Hospitals**: 234 facilities
- **SUR**: 175 facilities
- **SAR**: 104 facilities
- **Clínicas Privadas**: 46 facilities
- **Otros / Centros Especializados / Dispositivos**: 20 facilities

---

## 4. Extraction Script Source Code
The script below is located at `audit/extract_reduced_datasets.py` and can be re-run at any time using `.venv/bin/python audit/extract_reduced_datasets.py`:

```python
#!/usr/bin/env python3
"""
Data Architecture & Extraction Pipeline: Phase 1 Reduced Datasets
Script: audit/extract_reduced_datasets.py

Extracts reduced test datasets from raw repositories in accordance with:
- Task 1.4 (.instructions.md)
- Protocol 01 (Grain & Five Cs)
- Protocol 04 (Relative Paths & Reproducibility)

Generated Files in data/:
1. reduced_urgencias_2024_sample.csv (Respiratory, Mental Health, Hospitalizations)
2. reduced_rem20_critical_psych.csv (2024 Critical Care and Psychiatric Bed Occupancy)
3. reduced_establecimientos.csv (Emergency facilities and inpatient bed-reporting hospitals)
"""

import os
import sys
import time
import pandas as pd

def extract_reduced_urgencias():
    src_path = os.path.join("data", "AtencionesUrgencia", "AtencionesUrgencia2024.csv")
    dest_path = os.path.join("data", "reduced_urgencias_2024_sample.csv")
    
    print(f"[1/3] Processing SADU 2024: {src_path} -> {dest_path}")
    t0 = time.time()
    
    # Target clinical causes per Task 1.4:
    # Respiratory: 2, 3, 4, 5, 10, 11
    # Mental Health: 35, 36, 37, 38, 39, 40
    # Hospitalizations: 25
    target_causes = {2, 3, 4, 5, 10, 11, 25, 35, 36, 37, 38, 39, 40}
    
    chunksize = 250000
    chunks = []
    total_in = 0
    total_out = 0
    
    for chunk in pd.read_csv(src_path, sep=';', encoding='latin1', chunksize=chunksize, low_memory=False):
        total_in += len(chunk)
        # Standardize key whitespace
        chunk['IdEstablecimiento'] = chunk['IdEstablecimiento'].astype(str).str.strip()
        filtered = chunk[chunk['IdCausa'].isin(target_causes)]
        total_out += len(filtered)
        chunks.append(filtered)
        
    df_out = pd.concat(chunks, ignore_index=True)
    df_out.to_csv(dest_path, sep=';', index=False, encoding='utf-8')
    
    size_mb = os.path.getsize(dest_path) / (1024 * 1024)
    print(f"      Rows read: {total_in:,} | Rows extracted: {total_out:,} ({total_out/total_in*100:.2f}%)")
    print(f"      File size: {size_mb:.2f} MB | Elapsed: {time.time()-t0:.2f}s")


def extract_reduced_rem20():
    src_path = os.path.join("data", "indicadores_rem20_20260825.csv")
    dest_path = os.path.join("data", "reduced_rem20_critical_psych.csv")
    
    print(f"[2/3] Processing REM20: {src_path} -> {dest_path}")
    t0 = time.time()
    
    df_rem = pd.read_csv(src_path, sep=';', encoding='utf-8', low_memory=False)
    
    # Filter 2024
    rem24 = df_rem[df_rem['PERIODO'] == 2024].copy()
    
    # Target areas: Critical Care & Psychiatry
    # Codes: 405, 406, 411, 412, 414, 415, 418, 419, 420, 421, 422, 423, 424, 425, 426, 428, 429
    target_areas_mask = rem24['AREA_FUNCIONAL'].str.contains('Intensiv|Intermed|Psiquiatr', case=False, na=False)
    filtered = rem24[target_areas_mask].copy()
    
    # Strip string fields
    for col in ['COD_SSS', 'GLOSA_SSS', 'ESTABLECIMIENTO', 'AREA_FUNCIONAL']:
        if col in filtered.columns:
            filtered[col] = filtered[col].astype(str).str.strip()
            
    filtered.to_csv(dest_path, sep=';', index=False, encoding='utf-8')
    size_mb = os.path.getsize(dest_path) / (1024 * 1024)
    print(f"      Rows read: {len(df_rem):,} | 2024 critical/psych rows: {len(filtered):,}")
    print(f"      File size: {size_mb:.2f} MB | Elapsed: {time.time()-t0:.2f}s")


def extract_reduced_establecimientos():
    src_path = os.path.join("data", "establecimientos_20260910.csv")
    dest_path = os.path.join("data", "reduced_establecimientos.csv")
    
    print(f"[3/3] Processing Establecimientos Master: {src_path} -> {dest_path}")
    t0 = time.time()
    
    df_estab = pd.read_csv(src_path, sep=';', encoding='utf-8', low_memory=False)
    
    # Load REM20 hospital codes to ensure all bed-reporting hospitals are included
    rem_path = os.path.join("data", "indicadores_rem20_20260825.csv")
    rem_codes = set(pd.read_csv(rem_path, sep=';', usecols=['CODIGO_ESTABLECIMIENTO'], low_memory=False)['CODIGO_ESTABLECIMIENTO'].unique())
    
    # Clean whitespace in keys
    df_estab['EstablecimientoCodigoAntiguo'] = df_estab['EstablecimientoCodigoAntiguo'].astype(str).str.strip().replace('nan', '')
    df_estab['EstablecimientoCodigo'] = df_estab['EstablecimientoCodigo'].astype(int)
    
    # Inclusion criteria:
    # 1. Has emergency room: TieneServicioUrgencia == 'SI'
    # 2. Or is a hospital: TipoEstablecimientoGlosa == 'Hospital'
    # 3. Or reports hospital beds in REM20
    mask = (
        (df_estab['TieneServicioUrgencia'] == 'SI') |
        (df_estab['TipoEstablecimientoGlosa'] == 'Hospital') |
        (df_estab['EstablecimientoCodigo'].isin(rem_codes))
    )
    
    filtered = df_estab[mask].copy()
    filtered.to_csv(dest_path, sep=';', index=False, encoding='utf-8')
    
    size_mb = os.path.getsize(dest_path) / (1024 * 1024)
    print(f"      Total catalog: {len(df_estab):,} | Filtered facilities: {len(filtered):,}")
    print(f"      File size: {size_mb:.2f} MB | Elapsed: {time.time()-t0:.2f}s")


if __name__ == '__main__':
    print("=== STARTING REDUCED DATASET EXTRACTION PIPELINE ===")
    extract_reduced_urgencias()
    extract_reduced_rem20()
    extract_reduced_establecimientos()
    print("=== EXTRACTION COMPLETE ===")
```
