# Schema Inventory & Observational Units Audit

## 1. Systemic Scope & Regulatory Framework
This document provides the formal data architecture audit across all Chilean public health datasets located within the workspace repository (`data/` and `Diccionario/`). In accordance with Course Assessment Protocol 01 and Rubric Criterion W1-B, each dataset is evaluated by explicitly defining its atomic unit of observation (grain), verified temporal coverage, administrative scope, and identifying keys.

---

## 2. Observational Units & Coverage Matrix

| Source / Dataset | Observational Unit (Row Grain) | Temporal Granularity & Range | Geographic / Administrative Scope | Key Identifying Columns | File Format & Encoding |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Atenciones de Urgencia (SADU)** (`data/AtencionesUrgencia/`) | Daily aggregate count of emergency consultations by clinical cause category and age bracket per healthcare facility. | **Daily** (`fecha`, `semana`).<br>Verified: 2021-01-01 to 2024-12-31 (1,461 calendar days). | National coverage across primary care emergency centers (SAPU, SAR, SUR) and hospital emergency units (UEH). 640 reporting facilities in 2024. | `IdEstablecimiento`, `fecha`, `semana`, `IdCausa`, `GLOSATIPOESTABLECIMIENTO`. | CSV (`sep=';'`, Latin-1). |
| **Indicadores REM20** (`data/indicadores_rem20_20260825.csv`) | Monthly aggregate of hospital bed capacity and operational productivity metrics per functional care area in inpatient facilities. | **Monthly** (`MES`, `PERIODO`).<br>Verified: 2014-01 to 2026-07 (151 operational months). | National hospital network reporting inpatient beds to DEIS (SNSS public hospitals and delegadas). 208 unique facilities across 29 Health Services. | `CODIGO_ESTABLECIMIENTO`, `COD_AREA_FUNCIONAL`, `PERIODO`, `MES`. | CSV (`sep=';'`, UTF-8). |
| **Catálogo Maestro de Establecimientos** (`data/establecimientos_20260910.csv`) | Master registry entry for one authorized physical healthcare establishment in Chile. | **Static snapshot** (as of 2026-09-10). | National census of all public, municipal, and private healthcare facilities (5,743 total establishments). | `EstablecimientoCodigo` (Primary Key, unique), `EstablecimientoCodigoAntiguo`, `ComunaCodigo`, `RegionCodigo`. | CSV (`sep=';'`, UTF-8). |
| **Defunciones DEIS** (`data/DEFUNCIONES_FUENTE_DEIS_2024_2026_22092026/`) | Event-level microdata: one registered human death occurring within the national territory. | **Event-level** (exact date `FECHA_DEF`, annual consolidation `AÑO`).<br>Verified: 2024-01-01 to 2026-09-22. | National vital statistics registry (all deaths registered in civil registry and codified by DEIS). 344,469 total records. | `AÑO`, `FECHA_DEF`, `COD_COMUNA`, `DIAG1`, `DIAG2` (External cause), `SEXO_NOMBRE`, `EDAD_CANT`. | CSV (`sep=';'`, Latin-1). |
| **Egresos Hospitalarios** (`data/Esgresos/`) | Event-level microdata: one completed inpatient hospital discharge episode (anonymized patient). | **Event-level** (annual closure `ANO_EGRESO`, duration `DIAS_ESTADA`).<br>Verified: 2022 to 2025. | National public and private inpatient hospital discharges. 6,582,248 total discharge records across 4 years. | `ANO_EGRESO`, `COMUNA_RESIDENCIA`, `REGION_RESIDENCIA`, `DIAG1`, `DIAS_ESTADA`, `PERTENENCIA_ESTABLECIMIENTO_SALUD`. | CSV (`sep=';'`, Latin-1). |
| **Estadísticas Casos GES** (`data/EstadisticasTrimestralesCasosGES/`) | Quarterly consolidated volume of Explicit Health Guarantees (AUGE/GES) cases by health condition and insurer subsystem. | **Quarterly** (Q1, Q2, Q3, Q4) & historical series 2005-2026. | National health system, stratified by public (FONASA) and private (ISAPRE) coverage regimes. | `Año`, `Trimestre`, `ProblemaSalud`, `SubtipoGarantia`. | Excel workbook (`.xlsx`, multi-sheet). |
| **Series REM (A, BM, BS, D, P)** (`data/REMS/`) | Monthly aggregate of clinical prestations, consultations, or procedures per facility and prestation code. | **Monthly** (`Mes`, `Ano`).<br>Verified: 2022 to 2026. | National public health network (primary care, specialty centers, hospitals). | `IdEstablecimiento`, `IdServicio`, `Ano`, `Mes`, `CodigoPrestacion`. | CSV (`sep=';'`, UTF-8 / Latin-1). |

---

## 3. Detailed Dataset Schemas

### 3.1. Sistema de Atención de Urgencia (SADU)
- **Primary Source File**: `data/AtencionesUrgencia/AtencionesUrgencia2024.csv`
- **Total Rows Audited**: 8,973,229
- **Columns (21 total)**:
  1. `IdEstablecimiento` (string): Facility identifier, primarily matching `EstablecimientoCodigoAntiguo` (e.g., `01-100`, `14-900`).
  2. `NEstablecimiento` (string): Nominal establishment name.
  3. `IdCausa` (integer): Official DEIS cause identifier (values 1 to 42, matching `Anexo 1`).
  4. `GlosaCausa` (string): Clinical descriptive glosa.
  5. `Total` (integer): Total consultation volume for the specific facility-day-cause.
  6. `Menores_1` (integer): Consultations for patients aged < 1 year.
  7. `De_1_a_4` (integer): Consultations for patients aged 1 to 4 years.
  8. `De_5_a_14` (integer): Consultations for patients aged 5 to 14 years.
  9. `De_15_a_64` (integer): Consultations for patients aged 15 to 64 years.
  10. `De_65_y_mas` (integer): Consultations for patients aged 65 years and older.
  11. `fecha` (string): Date in `DD/MM/YYYY` format.
  12. `semana` (integer): Epidemiological week (1 to 52).
  13. `GLOSATIPOESTABLECIMIENTO` (string): Facility type (`Hospital`, `SAPU`, `SAR`, `SUR`, `CEAR`).
  14. `GLOSATIPOATENCION` (string): Attention modality (e.g., `Indiferenciado`).
  15. `GlosaTipoCampana` (string): Seasonal health campaign descriptor.
  16. `CodigoRegion` (integer): Territorial administrative region code (1 to 16).
  17. `NombreRegion` (string): Nominal region name.
  18. `CodigoDependencia` (integer): Health service administrative code.
  19. `NombreDependencia` (string): Nominal health service dependency.
  20. `CodigoComuna` (float/integer): Official SUBDERE commune code.
  21. `NombreComuna` (string): Nominal commune name.

### 3.2. Indicadores Hospitalarios REM20
- **Primary Source File**: `data/indicadores_rem20_20260825.csv`
- **Total Rows Audited**: 167,405
- **Columns (20 total)**:
  1. `PERIODO` (integer): Calendar year (2014 to 2026).
  2. `TIPO_PERTENENCIA` (integer): Administrative ownership code (1 = SNSS).
  3. `COD_SSS` (string/integer): Health Service identifier (01 to 33).
  4. `GLOSA_SSS` (string): Nominal Health Service name (e.g., `Metropolitano Central`).
  5. `CODIGO_ESTABLECIMIENTO` (integer): Official 6-digit DEIS establishment code (matches `EstablecimientoCodigo`).
  6. `ESTABLECIMIENTO` (string): Official hospital name.
  7. `COD_AREA_FUNCIONAL` (integer): Standardized hospital clinical ward area code.
  8. `AREA_FUNCIONAL` (string): Ward functional area description (e.g., `Área Cuidados Intensivos Adultos`, `Área Psiquiatría Adulto Corta estadía`).
  9. `MES` (integer): Calendar month of record (1 to 12).
  10. `DIAS_CAMAS_OCUPADAS` (integer): Bed days utilized by inpatients during the month.
  11. `DIAS_CAMAS_DISPONIBLES` (integer): Bed days operational and available during the month.
  12. `DIAS_ESTADA` (integer): Cumulative days of stay of patients discharged during the month.
  13. `NUMERO_EGRESOS` (integer): Total inpatient discharges (live discharges + deaths).
  14. `EGRESOS_FALLECIDOS` (integer): In-hospital inpatient deaths.
  15. `TRASLADOS` (integer): Inpatient inter-service or inter-hospital transfers.
  16. `INDICE_OCUPACIONAL` (float): Occupancy rate percentage: `(DIAS_CAMAS_OCUPADAS / DIAS_CAMAS_DISPONIBLES) * 100`.
  17. `PROMEDIO_CAMAS_DISPONIBLE` (float): Mean daily available beds during the month: `DIAS_CAMAS_DISPONIBLES / days_in_month`.
  18. `PROMEDIO_DIAS_ESTADA` (float): Mean length of stay: `DIAS_ESTADA / NUMERO_EGRESOS`.
  19. `LETALIDAD` (float): Hospital mortality rate percentage: `(EGRESOS_FALLECIDOS / NUMERO_EGRESOS) * 100`.
  20. `INDICE_ROTACION` (float): Bed turnover rate: `NUMERO_EGRESOS / PROMEDIO_CAMAS_DISPONIBLE`.

### 3.3. Catálogo Maestro de Establecimientos
- **Primary Source File**: `data/establecimientos_20260910.csv`
- **Total Facilities Audited**: 5,743
- **Primary Identifier**: `EstablecimientoCodigo` (0 nulls, 5,743 distinct values, verified 100% unique primary key).
- **Secondary Identifier**: `EstablecimientoCodigoAntiguo` (1,395 nulls for newer facilities; 4,348 distinct values, verified 100% unique among non-null values).
- **Core Structural Metadata**:
  - `TieneServicioUrgencia`: Binary flag (`SI`: 768, `NO`: 4,975).
  - `TipoEstablecimientoGlosa`: Facility classification (Hospitals: 234, SAPU: 259, SUR: 175, SAR: 104, Clinics: 46).
  - `NivelAtencionEstabglosa`: Level of care (`Primer Nivel`: 4,374; `Segundo Nivel`: 237; `Tercer Nivel`: 189; `No Aplica`: 943).
  - Geographic bindings: `RegionCodigo`, `RegionGlosa`, `ComunaCodigo`, `ComunaGlosa`, `Latitud`, `Longitud`.

### 3.4. Defunciones DEIS (Mortalidad General)
- **Primary Source File**: `data/DEFUNCIONES_FUENTE_DEIS_2024_2026_22092026/DEFUNCIONES_FUENTE_DEIS_2024_2026_22092026.csv`
- **Total Records Audited**: 344,469 (2024: 126,928; 2025: 126,466; 2026: 91,075 through 22-09-2026).
- **Diagnostic Architecture**:
  - `DIAG1`: Nature of injury, terminal physiological mechanism, or immediate pathological cause (e.g., asphyxiation, intracranial trauma, cardiogenic shock).
  - `DIAG2`: External cause of morbidity and mortality (`CAPITULO_DIAG2: V01-Y98`). Contains intentional self-harm codes (`X60-X84`) and accidental trauma.
  - Geographic variable: `COD_COMUNA` (344 distinct communes, 58 null values).

### 3.5. Egresos Hospitalarios DEIS
- **Primary Source Files**: `data/Esgresos/EGRESOS_2022` to `EGRESOS_2025`
- **Total Discharges Audited**: 6,582,248
- **Core Clinical & Operational Fields**:
  - `ANO_EGRESO`: Calendar year of hospital discharge.
  - `DIAG1`: Primary underlying diagnosis that caused hospital admission (ICD-10).
  - `DIAS_ESTADA`: Total calendar days of inpatient hospitalization.
  - `CONDICION_EGRESO`: Discharge status (1 = Alive, 2 = Deceased).
  - `COMUNA_RESIDENCIA` & `REGION_RESIDENCIA`: Patient territorial residence.
  - `PERTENENCIA_ESTABLECIMIENTO_SALUD`: Sector code (1 = SNSS Public, 2 = Non-SNSS Private).

---

## 4. Clinical Classifications & Codebook Reference

### 4.1. SADU Clinical Causes (Anexo 1 Concordance)
The table below specifies the official mapping between `IdCausa` in SADU and corresponding ICD-10 codes:

| IdCausa | Official Glosa (`Anexo 1`) | ICD-10 Classification | Clinical Stream |
| :--- | :--- | :--- | :--- |
| **1** | SECCIÓN 1. TOTAL ATENCIONES DE URGENCIA | All clinical causes | Benchmark |
| **2** | TOTAL CAUSAS SISTEMA RESPIRATORIO | J00-J98 | Respiratory Aggregate |
| **3** | Bronquitis/bronquiolitis aguda (J20-J21) | J20-J21 | Pediatric Respiratory |
| **4** | Influenza (J09-J11) | J09-J11 | Viral Epidemic |
| **5** | Neumonía (J12-J18) | J12-J18 | Severe Respiratory |
| **10** | IRA Alta (J00-J06) | J00-J06 | Acute Upper Respiratory |
| **11** | Crisis obstructiva bronquial (J40-J46) | J40-J46 | Obstructive Chronic/Acute |
| **25** | SECCIÓN 2. TOTAL DE HOSPITALIZACIONES | Inpatient Admissions from ED | Capacity Triage |
| **35** | Lesiones autoinfligidas intencionalmente (X60-X84) | X60-X84 | Mental Health / Self-Harm |
| **36** | TOTAL CAUSAS DE TRASTORNOS MENTALES (F00-F99) | F00-F99 | Mental Health Aggregate |
| **37** | Ideación Suicida (R45.8) | R45.8 | Suicidal Ideation |
| **38** | Trastornos debidos al uso de sustancias psicoactivas (F10-F19) | F10-F19 | Addiction / Substance Abuse |
| **39** | Trastornos del Humor (Afectivos) (F30-F39) | F30-F39 | Depressive / Bipolar Disorders |
| **40** | Trastornos neuróticos y relacionados con el estrés (F40-F48) | F40-F48 | Anxiety / Panic / PTSD |

### 4.2. REM20 Functional Care Areas (Bed Typologies)
Hospital beds in `indicadores_rem20_20260825.csv` are tracked across the following functional wards:
- **Adult Critical Care**: Code `405` (Cuidados Intensivos Adultos - UCI), Code `406` (Cuidados Intermedios Adultos - UTI).
- **Pediatric Critical Care**: Code `411` (Cuidados Intensivos Pediátricos - UCI), Code `412` (Cuidados Intermedios Pediátricos - UTI).
- **Neonatal Critical Care**: Code `414` (Neonatología Intensiva - UCI), Code `415` (Neonatología Intermedia - UTI).
- **Adult Inpatient Psychiatry**: Code `418` (Corta estadía), Code `419` (Mediana estadía), Code `420` (Larga estadía), Code `428` (Cuidados Intensivos Psiquiatría Adulto).
- **Child & Adolescent Inpatient Psychiatry**: Code `421` (Corta estadía), Code `422` (Mediana estadía), Code `429` (Cuidados Intensivos Psiquiatría Infanto-Adolescente).
- **Forensic Psychiatry**: Code `423` (Evaluación adulto), Code `424` (Tratamiento adulto), Code `425` (Evaluación infanto-adolescente), Code `426` (Tratamiento infanto-adolescente).
