# Relational Linkage & Cross-Dataset Join Audit

## 1. Executive Summary & Audit Scope
This technical audit evaluates the feasibility, structural integrity, and cardinalities of relational links across Chilean health datasets (`SADU`, `REM20`, `Establecimientos`, `Defunciones`, and `Esgresos`). In accordance with Course Assessment Protocol 01 (Join Discipline) and Rubric Criterion W1-B, every proposed join was empirically tested using Python scripts against actual raw data. All linkages are classified as either `VERIFIED` or `DOCUMENTED INFEASIBLE AT ROW GRAIN`.

---

## 2. Tested Join Matrix

| Linkage Identifier | Source Dataset & Key | Target Dataset & Key | Proposed Status | Tested Status | Tested Cardinality | Drop Rate / Match Integrity | Aggregation Rule & Resolution |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **J1: SADU to Master Catalog** | `SADU.IdEstablecimiento` (stripped) | `Establecimientos.EstablecimientoCodigoAntiguo` / `EstablecimientoCodigo` | Proposed | **VERIFIED** | N : 1 | **0.00% drop** (640 / 640 facilities matched 100.00%). | 609 facilities match `EstablecimientoCodigoAntiguo` (95.16%); 31 match `EstablecimientoCodigo` (4.84%). Whitespace trimming mandatory. |
| **J2: REM20 to Master Catalog** | `REM20.CODIGO_ESTABLECIMIENTO` | `Establecimientos.EstablecimientoCodigo` | Proposed | **VERIFIED** | N : 1 | **0.00% drop** (208 / 208 hospitals matched 100.00%). | Clean numeric-to-numeric join. Full compatibility across all 151 operational months. |
| **J3: SADU to REM20 (Facility Level)** | `SADU.CodigoNuevo` (via Master Bridge) | `REM20.CODIGO_ESTABLECIMIENTO` | Proposed | **PARTIALLY VERIFIED (Hospitals only)** | N : M | **71.72% drop at facility level** (458 / 640 facilities have no REM20 records). | **1:1 join valid only for Hospital EDs (179 / 182 matched, 98.35%).** Zero SAPU, SAR, or SUR exist in REM20. Cross-level analysis requires spatial/administrative aggregation. |
| **J4: SADU to REM20 (Health Service Level)** | `SADU.CodigoDependencia` / `NombreDependencia` | `REM20.COD_SSS` / `GLOSA_SSS` | Proposed | **VERIFIED** | N : M | **0.00% drop** (29 / 29 Health Services matched 100.00%). | Roll up daily emergency consultations and monthly bed occupancy to Health Service (`Servicio de Salud`). |
| **J5: SADU to REM20 (Commune Level)** | `SADU.CodigoComuna` | `Establecimientos.ComunaCodigo` -> `REM20.CODIGO_ESTABLECIMIENTO` | Proposed | **VERIFIED** | N : M | **0.00% drop for hospital communes** (communes without hospitals lack bed data). | Roll up primary care emergency demand to commune level; compare against territorial hospital beds. |
| **J6: SADU / Defunciones Link** | `Defunciones.COD_COMUNA` | `Establecimientos.ComunaCodigo` / `SADU.CodigoComuna` | Proposed | **VERIFIED** | N : M | **0.29% drop** (343 / 344 communes matched; 58 unassigned commune records in mortality). | Territory-level linkage feasible. Direct patient-level linkage impossible due to anonymization. |
| **J7: Esgresos to SADU / REM20** | `Esgresos.CODIGO_ESTABLECIMIENTO` | `Establecimientos.EstablecimientoCodigo` | Proposed | **DOCUMENTED INFEASIBLE** | N/A | **100% drop** (Variable absent from public data). | Open DEIS discharge files redact hospital identifiers. Linkage restricted to `COMUNA_RESIDENCIA` or `REGION_RESIDENCIA`. |

---

## 3. Detailed Empirical Verification Findings

### 3.1. Master Facility Bridge: Old vs. New Identifiers
- **Source**: `data/establecimientos_20260910.csv`
- **Audit Findings**:
  - `EstablecimientoCodigo` is the authoritative 6-digit primary key: 5,743 rows, 5,743 distinct values, 0 nulls.
  - `EstablecimientoCodigoAntiguo` contains 4,348 unique values and 1,395 nulls. Among non-null values, it is strictly 1:1 with `EstablecimientoCodigo`.
  - In `AtencionesUrgencia2024.csv`, raw values of `IdEstablecimiento` exhibited trailing whitespaces across 28 facilities (e.g., `'07-802 '`, `'26-100 '`). Without sanitization, 28 facilities fail to join.
  - Post `.str.strip()` sanitization:
    - 609 facilities (95.16%) match `EstablecimientoCodigoAntiguo`.
    - 31 facilities (4.84%) match `EstablecimientoCodigo` directly (already migrated to 6-digit format).
    - Unmatched facilities: **0 (100.00% resolution)**.

### 3.2. Primary Care Emergency Units vs. Hospital Inpatient Capacity Gap
- **Empirical Disparity**:
  - `AtencionesUrgencia2024.csv` comprises 640 urgent care facilities:
    - **Hospital Emergency Departments (UEH)**: 182 facilities (28.4% of centers; 26,958,924 consultations).
    - **Primary Care Urgent Centers (SAPU)**: 228 facilities (35.6% of centers; 22,369,076 consultations).
    - **High-Resolutivity Primary Centers (SAR)**: 95 facilities (14.8% of centers; 16,154,694 consultations).
    - **Rural Urgent Services (SUR)**: 132 facilities (20.6% of centers; 4,508,637 consultations).
    - **Respiratory Care Centers (CEAR)**: 3 facilities (0.5% of centers; 701 consultations).
  - Primary care centers (SAPU + SAR + SUR) represent **71.1% of all physical emergency facilities** and account for **43,032,407 consultations** (61.5% of total emergency demand).
  - `indicadores_rem20_20260825.csv` contains **208 inpatient facilities** (196 hospitals and 12 specialized clinics). It contains **exactly 0 records for SAPU, SAR, or SUR**.
- **Architectural Consequence**:
  - A facility-level join (`SADU.IdEstablecimiento` to `REM20.CODIGO_ESTABLECIMIENTO`) succeeds for 179 public hospitals (98.35% coverage of hospital emergency rooms), but drops 100% of primary care urgent centers.
  - To study the impact of community emergency surges (such as adolescent mental health crises or pediatric respiratory infections presenting at SAPU/SAR) on hospital inpatient capacity (UCI/UTI or Psychiatric beds), analysts **must aggregate demand to the Health Service (`GLOSA_SSS`) or Comuna (`CodigoComuna`) level**.

### 3.3. DEFUNCIONES Linkage & The ICD-10 DIAG2 Discovery
- **Source**: `data/DEFUNCIONES_FUENTE_DEIS_2024_2026_22092026/DEFUNCIONES_FUENTE_DEIS_2024_2026_22092026.csv` (344,469 deaths).
- **Audit Findings**:
  - The DEIS mortality registry contains two primary diagnostic columns: `DIAG1` (immediate/pathological cause) and `DIAG2` (external cause / mechanism).
  - An empirical query for suicide / intentional self-harm codes (`ICD-10: X60-X84`) in `DIAG1` yielded **0 records** across all 344,469 deaths.
  - In DEIS coding methodology, violent deaths or injuries record the physical pathology in `DIAG1` (e.g., `T71` Asphyxiation, `S06` Intracranial injury, `T39-T50` Poisoning) while the intentionality and external mechanism (`X60-X84`) is coded exclusively in `DIAG2` (`CAPITULO_DIAG2: V01-Y98`).
  - An empirical query on `DIAG2` identified **5,172 confirmed intentional self-harm deaths** across 2024–2026:
    - 2024: 1,986 deaths (1,602 males, 384 females).
    - 2025: 1,928 deaths (1,532 males, 396 females).
    - 2026 (provisional through Sep 22): 1,258 deaths (991 males, 267 females).
    - Demographic distribution: Mean age 43.6 ± 17.6 years; Range: 9 to 101 years; Male-to-female ratio: 4.1 to 1.
  - Commune match rate: `COD_COMUNA` in Defunciones matches `ComunaCodigo` in `establecimientos` in 343 out of 344 Chilean communes (99.71%).

### 3.4. Egresos Hospitalarios & Documented Infeasibility Finding
- **Source**: `data/Esgresos/EGRESOS_2022/` to `EGRESOS_2025/` (6,582,248 discharges).
- **Audit Findings**:
  - `DIAG1` starting with prefix `F` (`F00-F99`) captures inpatient psychiatric hospitalizations:
    - 2022: 34,798 discharges (2.18% of total).
    - 2023: 39,874 discharges (2.47% of total).
    - 2024: 43,005 discharges (2.58% of total).
    - 2025: 45,372 discharges (2.66% of total).
  - Length of stay (`DIAS_ESTADA`) for psychiatric admissions in 2024:
    - Median: 8.0 days.
    - Mean: 22.3 days.
    - Extreme positive skew: Max observed stay of 15,162 days (representing chronic institutionalized patients).
- **Documented Infeasibility Finding**:
  - *Inspected Files*: `data/Esgresos/EGRESOS_2022/EGRE_DATOS_ABIERTOS_2022.csv` through `EGRESOS_2025/EGR_DATOS_ABIERTO_2025.csv` and dictionaries `Diccionario BD egresos hospitalario.xlsx`.
  - *Missing Variable*: Neither `CODIGO_ESTABLECIMIENTO`, `IdEstablecimiento`, nor establishment name is present in public microdata files. The only facility-related variable is `PERTENENCIA_ESTABLECIMIENTO_SALUD` (binary indicator for SNSS vs. Non-SNSS).
  - *Structural Barrier*: It is structurally impossible to link individual patient discharge durations or bed-days directly to specific hospital identifiers in REM20 or SADU. Egresos data can only be utilized for national, regional (`REGION_RESIDENCIA`), or communal (`COMUNA_RESIDENCIA`) aggregate profiling.
