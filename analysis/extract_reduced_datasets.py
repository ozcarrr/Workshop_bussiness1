"""
Data Architecture & Extraction Pipeline: Phase 1 Reduced Datasets
Script: analysis/extract_reduced_datasets.py

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

DATA_DIR = "data" if os.path.exists("data") else os.path.join("..", "data")

def extract_reduced_urgencias():
    src_path = os.path.join(DATA_DIR, "AtencionesUrgencia", "AtencionesUrgencia2024.csv")
    dest_path = os.path.join(DATA_DIR, "reduced_urgencias_2024_sample.csv")
    
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
    src_path = os.path.join(DATA_DIR, "indicadores_rem20_20260825.csv")
    dest_path = os.path.join(DATA_DIR, "reduced_rem20_critical_psych.csv")
    
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
    src_path = os.path.join(DATA_DIR, "establecimientos_20260910.csv")
    dest_path = os.path.join(DATA_DIR, "reduced_establecimientos.csv")
    
    print(f"[3/3] Processing Establecimientos Master: {src_path} -> {dest_path}")
    t0 = time.time()
    
    df_estab = pd.read_csv(src_path, sep=';', encoding='utf-8', low_memory=False)
    
    # Load REM20 hospital codes to ensure all bed-reporting hospitals are included
    rem_path = os.path.join(DATA_DIR, "indicadores_rem20_20260825.csv")
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
