import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4a5568"))
        
        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Business Intelligence (IIB423T-1) — Workshop 1 (W1) Technical Report")
            self.drawRightString(558, 750, "Candidate Line Comparison & Strategy")
            self.setStrokeColor(colors.HexColor("#cbd5e0"))
            self.setLineWidth(0.5)
            self.line(54, 745, 558, 745)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 38, "Chilean Public Health Data Observatory | GROUP_01_W1")
        self.drawRightString(558, 38, page_text)
        self.setStrokeColor(colors.HexColor("#cbd5e0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()


def build_pdf(filename="report/GROUP_01_W1_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#4a5568'),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1a365d'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1a202c')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1 # Center
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#2d3748')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#4a5568'),
        alignment=1, # Center
        spaceAfter=8
    )

    story = []

    # Title & Header
    story.append(Paragraph("Chilean Public Health Data Observatory", title_style))
    story.append(Paragraph("Exploratory Data Analysis, Strategic Inquiry Framing & Architecture Report", ParagraphStyle('Sub', parent=title_style, fontSize=12, leading=15, textColor=colors.HexColor('#2b6cb0'))))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1a365d'), spaceBefore=4, spaceAfter=8))

    meta_text = "<b>Course:</b> Business Intelligence (IIB423T-1) — Workshop 1 (W1) | <b>Term:</b> Spring 2026<br/>" \
                "<b>Institution:</b> Universidad del Desarrollo, Facultad de Ingeniería | <b>Group:</b> GROUP_01_W1<br/>" \
                "<b>Instructor:</b> Carlos Elías Pérez Pizarro | <b>Submission Date:</b> September 24, 2026"
    story.append(Paragraph(meta_text, subtitle_style))
    story.append(Spacer(1, 4))

    # SECTION 1: EXECUTIVE SUMMARY
    story.append(Paragraph("1. Executive Summary & Project Context", h1_style))
    story.append(Paragraph(
        "The Chilean Public Health Data Observatory is an educational and strategic business intelligence initiative that transforms open public health repositories into rigorous analytical tools for systemic decision-making. Using authoritative data releases from the Ministry of Health (MINSAL) and the Department of Health Statistics and Information (DEIS), this report establishes the complete empirical baseline for Workshop 1 (W1) and Checkpoint 1 (C1).",
        body_style
    ))
    story.append(Paragraph(
        "We formulated and investigated two distinct candidate problems within the Chilean National Health System (SNSS):",
        body_style
    ))
    story.append(Paragraph("• <b>Candidate Line 1 (Seasonal Respiratory Surge & Critical Bed Saturation)</b>: Investigates how ambulatory emergency room visits for Acute Respiratory Infections (ARI) across pediatric (<1, 1-4 years) and elderly (65+ years) cohorts stress hospital ICU/IMU bed capacity during the annual winter campaign.", bullet_style))
    story.append(Paragraph("• <b>Candidate Line 2 (Mental Health Emergencies, Suicidal Ideation & Psychiatric Bed Tension)</b>: Evaluates the structural disparity between emergency room acute psychiatric presentations (ICD-10 R45.8, X60-X84, F30-F48) and specialized short-stay psychiatric bed capacity across Chile's 29 territorial Health Services.", bullet_style))
    story.append(Paragraph(
        "Following an exhaustive data audit of 8.97M raw emergency consultations (2.91M clinical target records), 167k longitudinal hospital bed records (REM20), and 5,743 registered healthcare facilities, we profile data quality via the <b>Five Cs Framework</b> and empirically verify foreign key linkages. We establish a <b>justified provisional preference for Candidate Line 2</b>, demonstrating that severe territorial bed deficits violate the mandate of Law 21.331 on Mental Health Protection.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # SECTION 2: CANDIDATE LINE 1
    story.append(Paragraph("2. Candidate Line 1 Brief: Seasonal Respiratory Strain & Bed Saturation", h1_style))
    story.append(Paragraph("<b>Problem Framing & Population:</b> Acute Respiratory Infections (ARI) constitute the primary operational stressor for Chilean emergency units during epidemiological winter (May to August). The clinical burden is strictly bimodal: infants (<1 and 1-4 years) are disproportionately affected by Respiratory Syncytial Virus (RSV) and acute bronchiolitis, while older adults (65+) experience severe viral/bacterial pneumonia. The scope encompasses 640 emergency facilities and 208 public inpatient hospitals across all 16 regions during 2024.", body_style))
    story.append(Paragraph("<b>Documentary Support & Health Policy:</b> Anchored in MINSAL's annual <i>Campaña de Invierno</i> operational decrees and the <i>National Health Strategy (ENS) 2030</i> (Axis on Communicable & Respiratory Diseases). While ENS 2030 targets a reduction in avoidable pneumonia mortality, public open data does not track clinical wait times in minutes; rather, strain is observable via the temporal correlation between weekly emergency volume and monthly hospital bed occupancy indices.", body_style))
    story.append(Paragraph("<b>Tentative BI Question & Proposed Use:</b> <i>'With how many weeks of lead time does an increase in primary care emergency consultations (SAPU/SAR) for upper ARI, bronchiolitis, and pneumonia anticipate critical bed saturation (occupancy > 85%) in pediatric and adult ICU/IMU units across each Health Service?'</i> Proposed User: Undersecretariat of Healthcare Networks & Centralized Bed Management Units (UGCC) to dynamically schedule bed reconversions 2-3 weeks ahead of peak viral circulation.", body_style))
    
    # Figure 1
    if os.path.exists('report/figures/fig1_respiratory_epidemiological_curve.png'):
        story.append(Spacer(1, 4))
        story.append(Image('report/figures/fig1_respiratory_epidemiological_curve.png', width=470, height=180))
        story.append(Paragraph("<b>Figure 1:</b> Weekly Epidemiological Curve of Respiratory Emergency Consultations (Chile, 2024). Shaded area denotes Winter Surge Window (Weeks 18-32).", caption_style))

    story.append(Paragraph("<b>Empirical Observations & Bed Saturation:</b> Across 2024, Upper ARI (`IdCausa 10`: 3.75M consultations) and Bronchiolitis (`IdCausa 3`: 840k consultations) dominated ambulatory presentations. In REM20, Adult ICU and IMU units operated continuously above the <b>85% safety threshold</b> (88.2% to 94.6% occupancy). Pediatric ICU occupancy surged from 62.1% in summer to 84.8% during winter.", body_style))

    # Figure 2
    if os.path.exists('report/figures/fig2_critical_bed_occupancy_85pct.png'):
        story.append(Spacer(1, 4))
        story.append(Image('report/figures/fig2_critical_bed_occupancy_85pct.png', width=470, height=180))
        story.append(Paragraph("<b>Figure 2:</b> Monthly Critical Bed Occupancy Index by Functional Care Area (REM20, 2024) with the 85% Operational Saturation Threshold Line.", caption_style))

    story.append(Spacer(1, 6))

    # SECTION 3: CANDIDATE LINE 2
    story.append(Paragraph("3. Candidate Line 2 Brief: Mental Health Emergencies & Psychiatric Bed Tension", h1_style))
    story.append(Paragraph("<b>Problem Framing & Systemic Crisis:</b> Emergency departments increasingly operate as acute stabilization points for severe psychiatric crises, suicidal ideation, and self-harm. Because primary care community mental health centers (COSAM) operate strictly on weekday ambulatory schedules, acute after-hours crises collapse into emergency rooms. Patients requiring admission face severe bottlenecks due to a chronic deficit in short-stay psychiatric hospital beds, leading to prolonged holding in emergency hallways.", body_style))
    story.append(Paragraph("<b>Policy Alignment & Legal Mandate:</b> <i>Law 21.331 (2021) on Mental Health Protection</i> legally mandates that psychiatric hospitalizations must be integrated into general secondary and tertiary hospitals under parity with physical illnesses, prohibiting segregated asylums. The <i>ENS 2030</i> targets a 15% reduction in youth suicide mortality, yet the <i>MINSAL Mental Health Plan</i> confirms mental health receives only ~2.4% of the public health budget versus the WHO >5% recommendation.", body_style))
    story.append(Paragraph("<b>Tentative BI Question & Proposed Use:</b> <i>'To what extent does the territorial disparity between acute mental health emergency demand (SADU: ICD-10 R45.8, X60-X84, F30-F48) and specialized short-stay psychiatric bed capacity (REM20: Functional Area Psiquiatría) create systemic bottlenecks across Chile's 29 Health Services?'</i> Proposed User: MINSAL Mental Health Department & Regional UGCC Bed Coordinators to allocate mobile crisis teams (COSAM) and convert hospital beds.", body_style))
    
    # KPI Callout
    kpi_table_data = [[
        Paragraph("<b>Core Key Performance Indicator (KPI):</b><br/>"
                  "<b>Mental Health Stress Ratio</b> = <i>[Acute Mental Health Emergency Visits (SADU)] / [Available Psychiatric Bed-Days (REM20)]</i><br/>"
                  "Quantifies territorial tension by measuring annual emergency presentations against local inpatient capacity.", callout_style)
    ]]
    kpi_table = Table(kpi_table_data, colWidths=[500])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#feebc8')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#dd6b20')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 6))

    # Figure 3
    if os.path.exists('report/figures/fig3_mental_health_age_distribution.png'):
        story.append(Image('report/figures/fig3_mental_health_age_distribution.png', width=470, height=180))
        story.append(Paragraph("<b>Figure 3:</b> Age Bracket Distribution in Critical Mental Health Emergency Presentations (Chile, 2024). Note the acute concentration of Intentional Self-Harm and Suicidal Ideation in youth (5-14) and young adults (15-64).", caption_style))

    story.append(Paragraph("<b>Empirical Findings & The Pediatric Bed Vacuum:</b> In 2024, mental health generated 305,432 emergency visits. In Intentional Self-Harm (`IdCausa 35`), <b>25.2% of presentations were children aged 5-14</b>, and 71.4% were aged 15-64. In REM20, only 33 hospitals report Adult Short-Stay Psychiatric beds (263k bed-days, 79.4% occupancy, 21.4 days mean stay). For Child/Adolescent Psychiatry, only 16 hospitals report active beds (81k bed-days), and <b>18 of Chile's 29 Health Services have ZERO dedicated pediatric psychiatric beds</b>.", body_style))

    # Figure 4
    if os.path.exists('report/figures/fig4_mental_health_stress_ratio_top12.png'):
        story.append(Spacer(1, 4))
        story.append(Image('report/figures/fig4_mental_health_stress_ratio_top12.png', width=470, height=190))
        story.append(Paragraph("<b>Figure 4:</b> Top 12 Chilean Health Services by Mental Health Stress Ratio (2024). Ratios above 1.0 denote acute systemic holding tension.", caption_style))

    # Table of Top Health Services
    story.append(Spacer(1, 4))
    ss_table_data = [
        [Paragraph("Health Service (Servicio de Salud)", table_header_style),
         Paragraph("Acute Emergencies", table_header_style),
         Paragraph("Psych Bed-Days", table_header_style),
         Paragraph("Stress Ratio", table_header_style),
         Paragraph("Operational Status", table_header_style)],
        [Paragraph("Servicio de Salud Del Maule", table_cell_bold), Paragraph("18,101", table_cell_style), Paragraph("9,865", table_cell_style), Paragraph("1.83", table_cell_bold), Paragraph("Severe Critical Bottleneck", table_cell_style)],
        [Paragraph("Servicio de Salud Talcahuano", table_cell_bold), Paragraph("7,096", table_cell_style), Paragraph("4,392", table_cell_style), Paragraph("1.62", table_cell_bold), Paragraph("Severe Critical Bottleneck", table_cell_style)],
        [Paragraph("Metropolitano Central", table_cell_bold), Paragraph("7,613", table_cell_style), Paragraph("5,776", table_cell_style), Paragraph("1.32", table_cell_bold), Paragraph("Critical Saturation", table_cell_style)],
        [Paragraph("Metropolitano Occidente", table_cell_bold), Paragraph("18,506", table_cell_style), Paragraph("14,138", table_cell_style), Paragraph("1.31", table_cell_bold), Paragraph("Critical Saturation", table_cell_style)],
        [Paragraph("Magallanes", table_cell_bold), Paragraph("3,417", table_cell_style), Paragraph("3,288", table_cell_style), Paragraph("1.04", table_cell_bold), Paragraph("High Systemic Tension", table_cell_style)],
        [Paragraph("Arauco", table_cell_bold), Paragraph("6,869", table_cell_style), Paragraph("6,707", table_cell_style), Paragraph("1.02", table_cell_bold), Paragraph("High Systemic Tension", table_cell_style)],
        [Paragraph("Concepción (Regional Referral Hub)", table_cell_bold), Paragraph("14,261", table_cell_style), Paragraph("18,770", table_cell_style), Paragraph("0.76", table_cell_bold), Paragraph("Regional Base Hospital", table_cell_style)],
    ]
    t_ss = Table(ss_table_data, colWidths=[150, 80, 80, 70, 120])
    t_ss.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f7fafc')]),
    ]))
    story.append(t_ss)
    story.append(Spacer(1, 6))

    # SECTION 4: DATA INSPECTION & FIVE CS
    story.append(Paragraph("4. Empirical Data Inspection & The Five Cs Quality Profiling", h1_style))
    story.append(Paragraph("<b>Observation Units (Grains) & Administrative Coverage:</b>", body_style))
    
    grains_table_data = [
        [Paragraph("Dataset Name", table_header_style),
         Paragraph("Observational Unit (Row Grain)", table_header_style),
         Paragraph("Temporal Window", table_header_style),
         Paragraph("Key Identifiers", table_header_style),
         Paragraph("Administrative Scope", table_header_style)],
        [Paragraph("Emergency Visits (SADU)", table_cell_bold), Paragraph("Daily volume by cause & age group per reporting facility", table_cell_style), Paragraph("Daily / Weekly (2024 annual closure)", table_cell_style), Paragraph("IdEstablecimiento, IdCausa, fecha", table_cell_style), Paragraph("National urgent network (640 centers: 182 Hospital EDs, 455 Primary Care)", table_cell_style)],
        [Paragraph("Hospital Beds (REM20)", table_cell_bold), Paragraph("Monthly aggregate of beds, patient-days & occupancy per functional area", table_cell_style), Paragraph("Monthly (2014 to 2026 series)", table_cell_style), Paragraph("CODIGO_ESTABLECIMIENTO, COD_AREA_FUNCIONAL", table_cell_style), Paragraph("National public hospital network (208 hospitals across 29 Health Services)", table_cell_style)],
        [Paragraph("Master Facility Registry", table_cell_bold), Paragraph("One authorized physical healthcare establishment", table_cell_style), Paragraph("Static snapshot (Sept 2026)", table_cell_style), Paragraph("EstablecimientoCodigo (PK), EstablecimientoCodigoAntiguo", table_cell_style), Paragraph("National census of 5,743 authorized public, municipal & private facilities", table_cell_style)],
    ]
    t_grains = Table(grains_table_data, colWidths=[100, 110, 80, 100, 110])
    t_grains.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f7fafc')]),
    ]))
    story.append(t_grains)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Relational Linkage Matrix & Verified Matches:</b>", body_style))
    story.append(Paragraph("• <b>SADU -> Master Registry</b>: `IdEstablecimiento` matches `EstablecimientoCodigoAntiguo`/`EstablecimientoCodigo` with <b>100.00% match rate</b> (640/640 facilities). Mandatory whitespace `.str.strip()` applied.", bullet_style))
    story.append(Paragraph("• <b>REM20 -> Master Registry</b>: `CODIGO_ESTABLECIMIENTO` matches `EstablecimientoCodigo` with <b>100.00% match rate</b> (208/208 hospitals).", bullet_style))
    story.append(Paragraph("• <b>Facility-Level Join (SADU -> REM20)</b>: Direct 1:1 join matches 179/182 hospital emergency departments (98.35%), but exhibits a <b>71.72% dropoff</b> across the entire network because primary care clinics (SAPU/SAR/SUR) have zero inpatient beds.", bullet_style))
    story.append(Paragraph("• <b>Spatial Rollup (Health Service Level)</b>: Linking `CodigoDependencia` to `COD_SSS` achieves <b>100.00% match across all 29 Health Services</b>, establishing the mathematically sound architecture for evaluating hospital bed strain.", bullet_style))
    story.append(Paragraph("• <b>Hospital Discharge Barrier (Esgresos)</b>: Public open data omits hospital codes to protect patient privacy, rendering direct facility linkage infeasible.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>The Five Cs Quality Framework Summary:</b>", body_style))
    story.append(Paragraph("• <b>Completeness</b>: 0.00% missing values in core SADU fields (`Total`, age groups, `IdCausa`, `semana`) across 8.97M rows. REM20 contains zero nulls across 167k records.", bullet_style))
    story.append(Paragraph("• <b>Correctness</b>: Mathematical formula `Total == Menores_1 + De_1_a_4 + De_5_a_14 + De_15_a_64 + De_65_y_mas` validated with 100.000% zero-discrepancy rate across all 8.97M rows. REM20 occupancy formula matches reported index within rounding tolerance.", bullet_style))
    story.append(Paragraph("• <b>Consistency</b>: All 42 distinct `IdCausa` values map 100% to DEIS ICD-10 groupings in `Anexo 1`.", bullet_style))
    story.append(Paragraph("• <b>Currency</b>: Reflects closed, audited 2024 annual series (weeks 1 to 52).", bullet_style))
    story.append(Paragraph("• <b>Conformity & DEIS Mortality Diagnostic Discovery</b>: Querying intentional self-harm codes (`X60-X84`) in `Defunciones.DIAG1` yields 0 records because DEIS codes the physical mechanism in `DIAG1` and external intent exclusively in `DIAG2`, where <b>5,172 confirmed self-harm deaths</b> were uncovered.", bullet_style))

    story.append(Spacer(1, 6))

    # SECTION 5: CRITICAL COMPARISON TABLE
    story.append(Paragraph("5. Critical Comparison Table & Evaluation (Rubric Criterion W1-C)", h1_style))
    
    comp_table_data = [
        [Paragraph("Evaluation Dimension", table_header_style),
         Paragraph("Candidate Line 1: Seasonal Respiratory Strain", table_header_style),
         Paragraph("Candidate Line 2: Mental Health & Psychiatric Bottlenecks", table_header_style)],
        [Paragraph("<b>Relevance Supported by Sources</b>", table_cell_style),
         Paragraph("Grounded in annual Winter Campaign protocols and ENS 2030 targets. Highly predictable operational challenge.", table_cell_style),
         Paragraph("Grounded in Law 21.331 (2021), ENS 2030 suicide prevention targets, and MINSAL Mental Health Plan (2.4% budget vs WHO >5%).", table_cell_style)],
        [Paragraph("<b>Question–Data Fit</b>", table_cell_style),
         Paragraph("Strong temporal fit across 52 weeks in SADU and monthly ICU/IMU bed indicators in REM20.", table_cell_style),
         Paragraph("Direct fit between acute crisis codes (R45.8, X60-X84) in SADU and psychiatric bed capacity in REM20 via Health Service rollup.", table_cell_style)],
        [Paragraph("<b>Analytical Opportunity for C1</b>", table_cell_style),
         Paragraph("Modeling seasonal lag between primary care ambulatory surge and tertiary ICU/IMU bed saturation across Health Services.", table_cell_style),
         Paragraph("Constructing territorial Stress KPIs, quantifying the pediatric bed vacuum, mapping regional bottlenecks, and testing Law 21.331 parity.", table_cell_style)],
        [Paragraph("<b>Main Limitation or Uncertainty</b>", table_cell_style),
         Paragraph("Highly sensitive to circulating viral strains (e.g. RSV vs Influenza) and dynamic temporary bed reconversions.", table_cell_style),
         Paragraph("Known stigma-related under-reporting; severe self-harm deaths captured only in `DIAG2` of vital statistics; discharge microdata redacted.", table_cell_style)],
        [Paragraph("<b>Feasible Scope & Future ML/UI</b>", table_cell_style),
         Paragraph("<b>ML</b>: Time-series forecasting of weekly respiratory surge.<br/><b>Dashboard</b>: Early warning bed alert semaphores.", table_cell_style),
         Paragraph("<b>ML</b>: Spatial clustering and risk classification of Health Services facing acute psychiatric bottlenecks.<br/><b>Dashboard</b>: Territorial Equity & Bed Stress Monitor.", table_cell_style)],
    ]
    t_comp = Table(comp_table_data, colWidths=[90, 205, 205])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f7fafc')]),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Justification of Provisional Preference for Candidate Line 2:</b><br/>"
                           "1. <b>Strategic Differentiation</b>: Avoids the conventional, overcrowded winter campaign topic, establishing a distinctive analytical investigation.<br/>"
                           "2. <b>Policy Urgency & Societal Value</b>: Evaluates systemic compliance with Law 21.331 parity mandates, exposing the severe shortage of short-stay beds.<br/>"
                           "3. <b>Referential Integrity</b>: The territorial rollup to Health Services provides 100% foreign key matching, eliminating false facility-level dropoffs.", body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Concrete Questions for Instructor Feedback:</b><br/>"
                           "1. <i>Operationalizing the Stress Metric</i>: Does the instructor recommend structuring the metric strictly as the Mental Health Stress Ratio (emergency visits / bed-days), or should we incorporate psychiatric turnover rates (`INDICE_ROTACION`) and length of stay (`PROMEDIO_DIAS_ESTADA`) to estimate an expected holding queue time?<br/>"
                           "2. <i>Handling the Pediatric Bed Vacuum</i>: Given that 18 out of 29 Health Services report 0 child/adolescent psychiatric bed-days in REM20, is it methodologically sound to document this as an empirical finding of systemic absence and segment predictive modeling to adult cohorts (15-64)?<br/>"
                           "3. <i>ML Formulation for Subsequent Deliverables</i>: Would the instructor recommend prioritizing a Spatial Risk Classification Model (predicting which Health Services will exceed critical bottleneck thresholds) or an Epidemiological Cluster Analysis?", body_style))

    story.append(Spacer(1, 6))

    # SECTION 6: PROJECT CONTINUITY
    story.append(Paragraph("6. Project Continuity: Machine Learning & BI Dashboard Specifications", h1_style))
    story.append(Paragraph("<b>Future Machine Learning Task Formulation:</b><br/>"
                           "• <b>Task Formulation</b>: Supervised Classification / Early-Warning Risk Scoring.<br/>"
                           "• <b>Target Variable ($Y$)</b>: $Y_{i, t+1} \\in \\{\\text{Low Risk}, \\text{Moderate Tension}, \\text{Critical Bottleneck}\\}$, where 'Critical Bottleneck' denotes a Mental Health Stress Ratio $> 1.20$ or psychiatric bed occupancy $> 90\\%$ in month $t+1$.<br/>"
                           "• <b>Feature Vector ($X_{i, t}$)</b>: Trailing 4-week consultation velocity in suicidal ideation (`IdCausa 37`) and self-harm (`IdCausa 35`), youth crisis ratio (visits 5-14 / total visits), psychiatric bed density per 100k population, historical length of stay, and seasonal harmonic terms.<br/>"
                           "• <b>Data Gaps to Address</b>: Absence of patient-level longitudinal identifiers requires models to operate at the Health Service or facility-cluster grain.", body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>BI Dashboard Architecture:</b><br/>"
                           "• <b>Target Audience</b>: MINSAL Mental Health Department, Regional SEREMI, and Health Service Bed Management Units (UGCC).<br/>"
                           "• <b>Update Frequency</b>: Monthly operational batch ingestion.<br/>"
                           "• <b>Core Views</b>: (1) Choropleth Map of Chile's 29 Health Services colored by Mental Health Stress Ratio; (2) Inpatient Bed Occupancy Gauges for Adult and Pediatric Short-Stay units; (3) Demographic Risk Stratification Panel tracking weekly suicidal ideation and self-harm trends across age cohorts.", body_style))

    story.append(Spacer(1, 6))

    # SECTION 7: PROCESS RECORD
    story.append(Paragraph("7. Process Record (Mandatory Component — Rubric Criterion W1-D)", h1_style))
    story.append(Paragraph("<b>7.1 Consequential Decisions and Checks Log:</b>", body_style))
    
    proc_table_data = [
        [Paragraph("Stage / Date", table_header_style),
         Paragraph("Consequential Decision", table_header_style),
         Paragraph("Alternative Considered", table_header_style),
         Paragraph("Rationale & Evidence", table_header_style),
         Paragraph("Verification Check", table_header_style),
         Paragraph("Location", table_header_style)],
        [Paragraph("Dictionary Audit<br/>(23-Sep-2026)", table_cell_style),
         Paragraph("Inspected Excel dictionaries via openpyxl & nrows=15 partial reads.", table_cell_style),
         Paragraph("Loading entire multi-sheet workbooks into memory.", table_cell_style),
         Paragraph("Prevented memory exhaustion and eliminated unnecessary overhead.", table_cell_style),
         Paragraph("Schema verified across Ficha, DiccionarioSADU, Anexo 1.", table_cell_style),
         Paragraph("Section 2 / workshop1.ipynb", table_cell_style)],
        [Paragraph("Data Ingestion<br/>(23-Sep-2026)", table_cell_style),
         Paragraph("Extracted deterministic reduced datasets into data/ via chunked clinical filtering.", table_cell_style),
         Paragraph("Loading raw 8.97M row CSV (1.2 GB) directly in notebook.", table_cell_style),
         Paragraph("Optimized load time (<7s) while preserving all 52 weeks and target causes.", table_cell_style),
         Paragraph("Verified zero row loss for target causes across 2024.", table_cell_style),
         Paragraph("Section 4.2 / audit/", table_cell_style)],
        [Paragraph("Relational Linkage<br/>(23-Sep-2026)", table_cell_style),
         Paragraph("Established master facility table as bridge between legacy and modern codes.", table_cell_style),
         Paragraph("Attempting string-based fuzzy join on hospital names.", table_cell_style),
         Paragraph("Hospital names suffer from accent, spelling, and whitespace variations; DEIS codes guarantee integrity.", table_cell_style),
         Paragraph("Empirical join test verified 100% key match on both keys.", table_cell_style),
         Paragraph("Section 6.1 / workshop1.ipynb", table_cell_style)],
        [Paragraph("Topic Selection<br/>(24-Sep-2026)", table_cell_style),
         Paragraph("Provisionally selected Candidate Line 2 (Mental Health) for C1.", table_cell_style),
         Paragraph("Developing Candidate Line 1 (Seasonal Respiratory Strain).", table_cell_style),
         Paragraph("Avoids thematic duplication; addresses urgent health policy bottleneck under Law 21.331.", table_cell_style),
         Paragraph("Multi-dimensional matrix and empirical data inspection.", table_cell_style),
         Paragraph("Section 5 / Report", table_cell_style)],
    ]
    t_proc = Table(proc_table_data, colWidths=[65, 95, 80, 105, 95, 60])
    t_proc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f7fafc')]),
    ]))
    story.append(t_proc)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>7.2 Instructor Feedback Status:</b> Formal instructor review pending. Documented technical dilemmas in Section 5.3 are prepared for class feedback.", body_style))
    story.append(Paragraph("<b>7.3 Individual Contributions:</b> Team `GROUP_01_W1`. Lead BI Strategy Consultant: hypothesis formulation, documentary research (Law 21.331, ENS 2030), comparison matrix, and report drafting. Lead Health Data Engineer: data extraction scripts, Five Cs profiling, foreign key verification, and notebook execution.", body_style))
    story.append(Paragraph("<b>7.4 AI Use & Verification Statement:</b> AI tool: Antigravity CLI / Gemini 3.8 Flash. Purpose: code scaffolding for nbformat, technical English translation, and ReportLab layout. Suggestions rejected: direct 1:1 row join between SADU and REM20 (rejected due to grain mismatch; replaced with Health Service rollup). Suggestions modified: initial query for suicide codes in `Defunciones.DIAG1` refactored to `DIAG2` after empirical audit confirmed DEIS coding architecture. All metrics, formulas, code execution, and citations were verified against official DEIS publications and real workspace data.", body_style))
    story.append(Paragraph("<b>7.5 Individual Reflection:</b> Successfully built automated, reproducible data extraction pipelines and verified foreign key integrity across 2.9M emergency consultations and hospital bed registries. Learned that public health analytics requires rigorous separation between ambulatory primary care demand and hospital bed capacity. Main uncertainty: handling the complete structural absence of child/adolescent psychiatric beds outside Santiago for predictive modeling.", body_style))

    story.append(Spacer(1, 6))

    # SECTION 8: REFERENCES
    story.append(Paragraph("8. References", h1_style))
    refs = [
        "1. Ministerio de Salud de Chile (MINSAL). (2022). <i>Estrategia Nacional de Salud para los Objetivos Sanitarios al 2030</i>. Santiago: MINSAL. Retrieved from https://www.minsal.cl",
        "2. Biblioteca del Congreso Nacional de Chile (BCN). (2021). <i>Ley N° 21.331 del Reconocimiento y Protección de los Derechos de las Personas en la Atención de Salud Mental</i>. Valparaíso: BCN. Retrieved from https://www.bcn.cl/leychile/navegar?idNorma=1159383",
        "3. Departamento de Estadísticas e Información de Salud (DEIS). (2024). <i>Manual y Diccionario de Atenciones de Urgencia (SADU)</i>. Santiago: Ministerio de Salud. Retrieved from https://deis.minsal.cl",
        "4. Departamento de Estadísticas e Información de Salud (DEIS). (2024). <i>Serie de Registro Estadístico Mensual REM20: Indicadores de Rendimiento Hospitalario y Dotación de Camas</i>. Santiago: MINSAL. Retrieved from https://deis.minsal.cl",
        "5. Departamento de Estadísticas e Información de Salud (DEIS). (2026). <i>Catálogo Maestro de Establecimientos de Salud de Chile (Snapshot 2026-09-10)</i>. Santiago: MINSAL. Retrieved from https://deis.minsal.cl",
        "6. World Health Organization (WHO). (2022). <i>World Mental Health Report: Transforming Mental Health for All</i>. Geneva: World Health Organization. Retrieved from https://www.who.int/publications/i/item/9789240049338",
        "7. Organización para la Cooperación y el Desarrollo Económicos (OCDE). (2021). <i>A New Benchmark for Mental Health Systems: Tackling the Social and Economic Costs of Mental Ill-Health</i>. OECD Health Policy Studies, Paris: OECD Publishing. Retrieved from https://www.oecd.org"
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('Ref', parent=body_style, fontSize=7.5, leading=10, spaceAfter=3)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report PDF built successfully at {filename}!")

if __name__ == '__main__':
    build_pdf()
