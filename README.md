# Phase 1 Technical Audit Report: Data Architecture, Schema Inspection & Reduced Datasets

**Role**: Senior Health Data Engineer & Schema Auditor  
**Course**: Business Intelligence (IIB423T-1) — Universidad del Desarrollo  
**Context**: Chilean Public Health Data Observatory (MINSAL / DEIS)  
**Deliverable Scope**: Phase 1 Technical Audit (`.instructions.md` & Rubric Criterion W1-B)

---

## 1. Executive Summary & Audit Overview
This technical audit establishes the empirical foundation for Workshop 1 (W1) and Checkpoint 1 (C1). Using Python scripts executed against the complete raw data repository (`data/` and `Diccionario/`), we conducted an exhaustive schema audit, relational join verification, Five Cs quality profiling, and reduced dataset extraction pipeline.

All findings reported below reflect computed empirical results rather than catalog assumptions.

### Directory Organization of Audit Discoveries
The deliverables and discoveries of this audit are organized within the `audit/` directory:
- [`audit/01_schema_inventory_and_grains.md`](audit/01_schema_inventory_and_grains.md): Comprehensive inventory of schemas, atomic observational units (grains), temporal coverage, administrative levels, identifying keys, and official DEIS dictionary concordances across all 7 workspace datasets.
- [`audit/02_relational_linkage_matrix.md`](audit/02_relational_linkage_matrix.md): Empirical join feasibility tests, master facility bridge evaluation, primary care emergency unit mismatch analysis, DEIS mortality diagnostic architecture discovery (`DIAG1` vs. `DIAG2`), and hospital discharge code redaction findings.
- [`audit/03_five_cs_quality_profiling.md`](audit/03_five_cs_quality_profiling.md): Quantitative data quality evaluation across Completeness, Correctness, Consistency, Currency, and Conformity, including cross-sum formula proofs across 8.97M rows and hospital bed saturation analyses.
- [`audit/04_reduced_dataset_extraction.md`](audit/04_reduced_dataset_extraction.md): Extraction specifications, clinical filtering logic, row distributions, and reproducibility instructions for generated reduced test files.
- [`audit/extract_reduced_datasets.py`](audit/extract_reduced_datasets.py): Production Python script for deterministic, chunked extraction of reduced datasets into `data/`.

---

## 2. Observational Units & Schema Inventory

In accordance with Course Protocol 01 (The Observation Unit Rule), every dataset must have an explicitly defined atomic row grain, temporal window, and administrative coverage before performing analytical aggregations.

| Dataset Name | Observational Unit (Row Grain) | Temporal Granularity & Coverage | Geographic / Administrative Scope | Key Identifying Columns | Verified File Attributes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Atenciones de Urgencia (SADU)** | Daily consultation volume aggregated by clinical cause category and age bracket per reporting emergency facility. | **Daily** (`fecha`, `semana`).<br>Coverage: 2021-01-01 to 2024-12-31 (1,461 calendar days). | National public urgent network (640 facilities in 2024: 182 Hospital EDs, 228 SAPU, 132 SUR, 95 SAR, 3 CEAR). | `IdEstablecimiento`, `fecha`, `semana`, `IdCausa`, `GLOSATIPOESTABLECIMIENTO`. | CSV (`sep=';'`, Latin-1). 8,973,229 rows in 2024 (1.2 GB). |
| **Indicadores Hospitalarios REM20** | Monthly aggregate of operational bed capacity, patient-days, discharges, and occupancy metrics per functional care area in inpatient facilities. | **Monthly** (`MES`, `PERIODO`).<br>Coverage: 2014-01 to 2026-07 (151 operational months). | National hospital network reporting beds to DEIS (208 facilities across 29 Health Services). | `CODIGO_ESTABLECIMIENTO`, `COD_AREA_FUNCIONAL`, `PERIODO`, `MES`. | CSV (`sep=';'`, UTF-8). 167,405 rows across 13 years. |
| **Catálogo Maestro de Establecimientos** | Master registry entry for one authorized physical healthcare establishment in Chile. | **Static snapshot** (as of 2026-09-10). | National census of all public, municipal, and private facilities (5,743 establishments). | `EstablecimientoCodigo` (Primary Key, unique), `EstablecimientoCodigoAntiguo`, `ComunaCodigo`. | CSV (`sep=';'`, UTF-8). 5,743 rows, 33 columns. |
| **Defunciones DEIS (Mortalidad General)** | Event-level microdata: one registered human death occurring within the national territory. | **Event-level** (exact date `FECHA_DEF`, annual consolidation `AÑO`).<br>Coverage: 2024-01-01 to 2026-09-22. | National vital statistics registry (all recorded deaths in Chile). | `AÑO`, `FECHA_DEF`, `COD_COMUNA`, `DIAG1`, `DIAG2`, `SEXO_NOMBRE`, `EDAD_CANT`. | CSV (`sep=';'`, Latin-1). 344,469 records (104.2 MB). |
| **Egresos Hospitalarios DEIS** | Event-level microdata: one completed inpatient hospital discharge episode (anonymized patient). | **Event-level** (annual closure `ANO_EGRESO`, duration `DIAS_ESTADA`).<br>Coverage: 2022 to 2025. | National public and private inpatient hospital discharges. | `ANO_EGRESO`, `COMUNA_RESIDENCIA`, `REGION_RESIDENCIA`, `DIAG1`, `DIAS_ESTADA`, `PERTENENCIA_ESTABLECIMIENTO_SALUD`. | CSV (`sep=';'`, Latin-1). 6,582,248 records across 4 years. |
| **Estadísticas Trimestrales GES** | Quarterly consolidated volume of Explicit Health Guarantees (AUGE/GES) cases by health condition and insurer subsystem. | **Quarterly** (Q1–Q4) & historical series 2005–2026. | National health system, stratified by public (FONASA) and private (ISAPRE) coverage regimes. | `Año`, `Trimestre`, `ProblemaSalud`, `SubtipoGarantia`. | Excel (`.xlsx`, multi-sheet). |
| **Series REM (A, BM, BS, D, P)** | Monthly aggregate of clinical prestations, consultations, or procedures per facility and prestation code. | **Monthly** (`Mes`, `Ano`).<br>Coverage: 2022 to 2026. | National public health network (primary care, specialty centers, hospitals). | `IdEstablecimiento`, `IdServicio`, `Ano`, `Mes`, `CodigoPrestacion`. | CSV (`sep=';'`, UTF-8 / Latin-1). 57 columns (`Col01` to `Col50`). |

---

## 3. Tested Relational Join Matrix

In compliance with Protocol 01 (Join Discipline), no shared-code assumptions were accepted without testing. The matrix below documents all proposed joins, their empirically verified status, key drop rates, and architectural aggregation rules:

| Join Description | Source Key | Target Key | Tested Status | Cardinality | Match Rate & Dropoff | Required Aggregation Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SADU -> Master Catalog** | `SADU.IdEstablecimiento` (trimmed) | `Establecimientos.EstablecimientoCodigoAntiguo` / `EstablecimientoCodigo` | **VERIFIED** | N : 1 | **100.00% match** (640 / 640 facilities). 0% drop. | Trailing whitespace removal mandatory. 609 match legacy code (95.16%); 31 match new 6-digit code (4.84%). |
| **REM20 -> Master Catalog** | `REM20.CODIGO_ESTABLECIMIENTO` | `Establecimientos.EstablecimientoCodigo` | **VERIFIED** | N : 1 | **100.00% match** (208 / 208 hospitals). 0% drop. | Clean numeric primary key join. Full integrity. |
| **SADU -> REM20 (Facility Level)** | `SADU.CodigoNuevo` (via Master Bridge) | `REM20.CODIGO_ESTABLECIMIENTO` | **PARTIALLY VERIFIED (Hospitals only)** | N : M | **28.28% match** (181 / 640 facilities). **71.72% drop**. | **1:1 join valid only for Hospital Emergency Units (179 / 182 matched in 2024, 98.35%).** Zero primary care centers (SAPU/SAR/SUR) exist in REM20. |
| **SADU -> REM20 (Health Service Level)** | `SADU.CodigoDependencia` | `REM20.COD_SSS` | **VERIFIED** | N : M | **100.00% match** (29 / 29 Health Services). 0% drop. | Primary care and hospital emergency demand must be aggregated to the Health Service (`Servicio de Salud`) to evaluate hospital bed strain. |
| **SADU -> REM20 (Commune Level)** | `SADU.CodigoComuna` | `Establecimientos.ComunaCodigo` -> `REM20.CODIGO_ESTABLECIMIENTO` | **VERIFIED** | N : M | **100.00% match for hospital communes**. | Aggregates community emergency presentations to territorial hospital beds located within the commune. |
| **Defunciones -> Commune** | `Defunciones.COD_COMUNA` | `Establecimientos.ComunaCodigo` | **VERIFIED** | N : M | **99.71% match** (343 / 344 communes). 58 unassigned rows. | Enables territorial mortality correlation with emergency volumes. |
| **Esgresos -> SADU / REM20** | `Esgresos.CODIGO_ESTABLECIMIENTO` | `Establecimientos.EstablecimientoCodigo` | **DOCUMENTED INFEASIBLE** | N/A | **100% drop** (Key missing in public files). | Hospital codes are redacted in public DEIS discharge data. Facility-level linkage impossible; analysis bounded to regional/communal aggregates. |

### Critical Empirical Linkage Discoveries
1. **The Primary Care Emergency Gap**:
   Primary care urgent centers (SAPU: 228, SAR: 95, SUR: 132) represent 71.1% of physical emergency centers and handle 61.5% of total emergency demand in Chile (43,032,407 consultations in 2024). However, REM20 tracks inpatient hospital beds and contains exactly 0 primary care facilities. Therefore, analyzing primary care emergency pressure against hospital bed capacity cannot be done at the facility level; it requires spatial rollup to the Health Service (`Servicio de Salud`) or Commune (`Comuna`).
2. **The DEIS Mortality Diagnostic Architecture (`DIAG1` vs. `DIAG2`)**:
   Querying ICD-10 intentional self-harm / suicide codes (`X60-X84`) in `DIAG1` returned exactly **0 cases** across 344,469 deaths. Under DEIS coding rules, `DIAG1` records the anatomical trauma/pathology (e.g., asphyxiation, intracranial trauma, poisoning), whereas the external cause/intent (`X60-X84`) is coded exclusively in `DIAG2` (`CAPITULO_DIAG2: V01-Y98`). Querying `DIAG2` uncovered **5,172 confirmed intentional self-harm deaths** across 2024–2026.
3. **Esgresos Facility Anonymization Barrier**:
   In `Esgresos` (6.58M records), psychiatric hospitalizations (`DIAG1` starting with `F`) account for ~43,000 annual discharges with a median length of stay of 8.0 days (mean 22.3 days). However, hospital identifiers (`CODIGO_ESTABLECIMIENTO`) are omitted from public open data to safeguard patient confidentiality. Direct facility linkage to REM20 beds is structurally infeasible.

---

## 4. The Five Cs Data Quality Summary

Quality profiling was conducted across `AtencionesUrgencia2024.csv`, `indicadores_rem20_20260825.csv`, and `establecimientos_20260910.csv`:

### 4.1. Completeness
- `AtencionesUrgencia2024.csv`: Core analytical fields (`Total`, age groups, `IdCausa`, `fecha`, `semana`, `GLOSATIPOESTABLECIMIENTO`) exhibit **0.0000% missing values** across 8,973,229 rows. Minor missingness occurs only in non-essential names (`NEstablecimiento`: 0.58%; `CodigoComuna`: 0.09%), fully recoverable via the master catalog.
- `indicadores_rem20_20260825.csv`: **100.00% complete** across all 20 attributes and 167,405 rows. Zero nulls.
- `establecimientos_20260910.csv`: Primary key `EstablecimientoCodigo` is 100% complete. Legacy key `EstablecimientoCodigoAntiguo` has 1,395 nulls (24.29%) corresponding to facilities established after the transition to 6-digit codes. Geographic coordinates have 217 nulls (3.78%).

### 4.2. Correctness
- **SADU Age Cross-Sum Validation**:
  Empirical formula test: `Total == Menores_1 + De_1_a_4 + De_5_a_14 + De_15_a_64 + De_65_y_mas`.
  Verified across all 8,973,229 rows: **0 discrepancies (100.0000% mathematical accuracy)**.
- **REM20 Occupancy Formula Validation**:
  Empirical formula test: `INDICE_OCUPACIONAL == (DIAS_CAMAS_OCUPADAS / DIAS_CAMAS_DISPONIBLES) * 100`.
  Verified across all 164,241 valid rows: **0 discrepancies within rounding tolerance (100.00% formula integrity)**.
  Operational overcapacity (`INDICE_OCUPACIONAL > 100.0%`) was observed in 1,894 records (1.13%), reflecting surge bed reconversions during peak winter strains and psychiatric crises.

### 4.3. Consistency
- `AtencionesUrgencia2024.csv` contains exactly 42 distinct `IdCausa` values, which map 100% to official clinical categories in `Diccionario/DICCIONARIO_ATENCIONES_DE_URGENCIA.xlsx` (`Anexo 1`).
- All 208 hospital codes in REM20 map to valid establishments in the master catalog.
- Legacy codes in `establecimientos` exhibit zero duplication collisions among non-null values.

### 4.4. Currency
- `AtencionesUrgencia2024.csv`: Fully consolidated annual closure covering 2024-01-01 to 2024-12-31 (weeks 1 to 52).
- `indicadores_rem20_20260825.csv`: Multi-year longitudinal series (2014 to 2026), updated through July 2026 (Month 7), representing a standard 45-day operational reporting lag.
- `establecimientos_20260910.csv`: Official DEIS master snapshot dated September 10, 2026.
- `DEFUNCIONES_FUENTE_DEIS`: Official DEIS vital statistics extract updated through September 22, 2026.

### 4.5. Conformity
- Delimiters: Standard semicolon `;` across all tabular files.
- Encodings:
  - `AtencionesUrgencia` and `Defunciones`: **Latin-1 (ISO-8859-1)**. Loading with UTF-8 triggers character corruption or decode failures.
  - `indicadores_rem20` and `establecimientos`: **UTF-8**.
- Date Formats: `AtencionesUrgencia` utilizes localized `DD/MM/YYYY`, requiring explicit string-to-datetime parsing. `Defunciones` uses ISO-8601 `YYYY-MM-DD`. `REM20` isolates `PERIODO` and `MES`.
- Trailing Whitespaces: 28 facility identifiers in SADU 2024 contained trailing spaces (e.g. `'07-802 '`), requiring `.str.strip()` prior to relational merging.

---

## 5. Reduced Test Datasets Execution Summary

Pursuant to Task 1.4, three reduced datasets were extracted and saved directly into `data/` using `audit/extract_reduced_datasets.py`:

```
data/
├── reduced_urgencias_2024_sample.csv    (543.03 MB | 2,916,297 rows | UTF-8)
├── reduced_rem20_critical_psych.csv     (0.70 MB   | 4,322 rows     | UTF-8)
└── reduced_establecimientos.csv         (0.37 MB   | 838 facilities | UTF-8)
```

### Reproducibility Command
To reproduce the extraction pipeline from raw source files:
```bash
.venv/bin/python audit/extract_reduced_datasets.py
```

### Target Causes Captured in `reduced_urgencias_2024_sample.csv`:
- **Respiratory Stream (Line A)**:
  - `IdCausa 2`: Total Causas Sistema Respiratorio (5,541,628 consultations)
  - `IdCausa 3`: Bronquitis / bronquiolitis aguda (840,273 consultations)
  - `IdCausa 4`: Influenza (125,153 consultations)
  - `IdCausa 5`: Neumonía (266,049 consultations)
  - `IdCausa 10`: IRA Alta (3,753,066 consultations)
  - `IdCausa 11`: Crisis obstructiva bronquial (199,959 consultations)
- **Mental Health Stream (Line B)**:
  - `IdCausa 35`: Lesiones autoinfligidas intencionalmente (9,753 consultations)
  - `IdCausa 36`: Total Causas Trastornos Mentales (305,432 consultations)
  - `IdCausa 37`: Ideación Suicida (12,433 consultations)
  - `IdCausa 38`: Trastornos por sustancias psicoactivas (28,633 consultations)
  - `IdCausa 39`: Trastornos del Humor / Afectivos (30,634 consultations)
  - `IdCausa 40`: Trastornos neuróticos y estrés (173,931 consultations)
- **Hospital Capacity Triage**:
  - `IdCausa 25`: Total de Hospitalizaciones derivadas desde Urgencia (633,303 hospitalizations)

---

## 6. Audit Conclusion & Phase 2 Transition
The data architecture audit confirms:
1. Both candidate lines (Respiratory Strain vs. Mental Health Crisis) possess high-integrity empirical data within the workspace.
2. Direct hospital emergency linkage to REM20 inpatient beds is verified for 179 public hospitals (98.35%).
3. Primary care emergency analysis (SAPU/SAR/SUR) is empirically feasible and representative (61.5% of consultations), but requires spatial aggregation to the Health Service (`Servicio de Salud`) or Commune (`Comuna`).
4. Mortality analysis for suicidal crises requires querying `DIAG2` in DEIS mortality data, avoiding the false-negative trap of `DIAG1`.
5. The reduced test datasets in `data/` are verified, consistent, and ready for exploratory data analysis (EDA) and narrative reporting in Phase 2.
