"""
PDF Generator module for Insurance Confirmation form.
Uses ReportLab to create a PDF matching the sample layout.
"""
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def draw_checkbox(c, x, y, checked=False, size=8):
    """Draw a checkbox at the given position."""
    c.rect(x, y, size, size, stroke=1, fill=0)
    if checked:
        c.line(x, y, x + size, y + size)
        c.line(x, y + size, x + size, y)


def draw_underline_field(c, x, y, width, value="", font_size=9):
    """Draw an underlined field with optional value."""
    c.setFont("Helvetica", font_size)
    if value:
        c.drawString(x, y + 2, value)
    c.line(x, y, x + width, y)


def generate_pdf(data):
    """Generate an Insurance Confirmation PDF from form data."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setTitle("Insurance Confirmation")
    width, height = letter  # 612 x 792

    # --- Page margins ---
    left_margin = 40
    right_margin = width - 40
    page_width = right_margin - left_margin

    # =====================================================
    # TOP BOX - Subscriber / Patient Info
    # =====================================================
    box_top = height - 40
    box_left = left_margin + 30
    box_right = right_margin - 30
    box_height = 70
    box_bottom = box_top - box_height

    c.setStrokeColor(HexColor("#000000"))
    c.setLineWidth(1)
    c.rect(box_left, box_bottom, box_right - box_left, box_height, stroke=1, fill=0)

    y = box_top - 16
    c.setFont("Helvetica-Bold", 9)
    c.drawString(box_left + 5, y, "Subscriber Name:")
    c.setFont("Helvetica", 9)
    draw_underline_field(c, box_left + 100, y - 2, 170, data.get("subscriber_name", ""))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(box_left + 285, y, "DOB:")
    draw_underline_field(c, box_left + 310, y - 2, 100, data.get("subscriber_dob", ""))

    y -= 16
    c.setFont("Helvetica-Bold", 9)
    c.drawString(box_left + 5, y, "Patient Name:")
    draw_underline_field(c, box_left + 100, y - 2, 170, data.get("patient_name", ""))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(box_left + 285, y, "DOB:")
    draw_underline_field(c, box_left + 310, y - 2, 100, data.get("patient_dob", ""))

    y -= 16
    c.setFont("Helvetica-Bold", 9)
    c.drawString(box_left + 5, y, "Member ID#:")
    draw_underline_field(c, box_left + 100, y - 2, 120, data.get("member_id", ""))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(box_left + 230, y, "SS#:")
    draw_underline_field(c, box_left + 255, y - 2, 80, data.get("ss_number", ""))

    y -= 16
    c.setFont("Helvetica-Bold", 9)
    c.drawString(box_left + 5, y, "Reference# for call:")
    draw_underline_field(c, box_left + 115, y - 2, 200, data.get("reference_number", ""))

    # =====================================================
    # TITLE - Insurance Confirmation
    # =====================================================
    y = box_bottom - 22
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(HexColor("#00BFBF"))
    title_text = "Insurance Confirmation"
    title_width = c.stringWidth(title_text, "Helvetica-Bold", 14)
    c.drawString((width - title_width) / 2, y, title_text)
    # Underline the title
    c.setStrokeColor(HexColor("#00BFBF"))
    c.line((width - title_width) / 2, y - 2, (width + title_width) / 2, y - 2)
    c.setFillColor(HexColor("#000000"))
    c.setStrokeColor(HexColor("#000000"))

    # =====================================================
    # EMPLOYER / GROUP INFO
    # =====================================================
    y -= 22
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "Employer:")
    draw_underline_field(c, left_margin + 55, y - 2, 200, data.get("employer", ""))
    c.drawString(left_margin + 265, y, "Group#:")
    draw_underline_field(c, left_margin + 305, y - 2, 100, data.get("group_number", ""))
    c.drawString(left_margin + 415, y, "Payor ID #:")
    draw_underline_field(c, left_margin + 470, y - 2, 90, data.get("payor_id", ""))

    y -= 16
    c.drawString(left_margin + 200, y, "Group Name:")
    draw_underline_field(c, left_margin + 265, y - 2, 200, data.get("group_name", ""))

    # =====================================================
    # INSURANCE INFORMATION SECTION
    # =====================================================
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_margin + 20, y, "•  Insurance Information:")

    y -= 16
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "Date Verified:")
    draw_underline_field(c, left_margin + 78, y - 2, 120, data.get("date_verified", ""))

    y -= 14
    c.drawString(left_margin, y, "Effective Date:")
    draw_underline_field(c, left_margin + 78, y - 2, 120, data.get("effective_date", ""))

    y -= 14
    c.drawString(left_margin, y, "Insurance Company:")
    draw_underline_field(c, left_margin + 107, y - 2, 350, data.get("insurance_company", ""))

    y -= 14
    c.drawString(left_margin, y, "Claims Address:")
    draw_underline_field(c, left_margin + 90, y - 2, 150, data.get("claims_address", ""))
    c.drawString(left_margin + 250, y, "City:")
    draw_underline_field(c, left_margin + 275, y - 2, 100, data.get("claims_city", ""))
    c.drawString(left_margin + 385, y, "State:")
    draw_underline_field(c, left_margin + 415, y - 2, 50, data.get("claims_state", ""))
    c.drawString(left_margin + 475, y, "Zip:")
    draw_underline_field(c, left_margin + 495, y - 2, 65, data.get("claims_zip", ""))

    y -= 14
    c.drawString(left_margin, y, "Phone #:")
    draw_underline_field(c, left_margin + 50, y - 2, 210, data.get("phone", ""))
    c.drawString(left_margin + 280, y, "Fax #:")
    draw_underline_field(c, left_margin + 310, y - 2, 190, data.get("fax", ""))

    y -= 16
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "IN/OUT Network?")
    draw_checkbox(c, left_margin + 92, y - 1, data.get("network_in", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 103, y, "IN")
    draw_checkbox(c, left_margin + 118, y - 1, data.get("network_out", False))
    c.drawString(left_margin + 129, y, "OUT")

    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin + 160, y, "Calendar/Contract Yr- Month start:")
    draw_underline_field(c, left_margin + 358, y - 2, 140, data.get("month_start", ""))

    y -= 14
    c.drawString(left_margin, y, "Max per year: $")
    draw_underline_field(c, left_margin + 88, y - 2, 140, data.get("max_per_year", ""))
    c.drawString(left_margin + 240, y, "Used: $")
    draw_underline_field(c, left_margin + 278, y - 2, 80, data.get("used_amount", ""))

    y -= 14
    c.drawString(left_margin, y, "Deductible: $")
    draw_underline_field(c, left_margin + 75, y - 2, 55, data.get("deductible", ""))
    c.drawString(left_margin + 135, y, "/")
    draw_underline_field(c, left_margin + 145, y - 2, 40, data.get("deductible_slash", ""))
    c.drawString(left_margin + 200, y, "Family Deductible: $")
    draw_underline_field(c, left_margin + 310, y - 2, 55, data.get("family_deductible", ""))
    c.drawString(left_margin + 370, y, "/")
    draw_underline_field(c, left_margin + 380, y - 2, 40, data.get("family_deductible_slash", ""))

    y -= 14
    c.drawString(left_margin, y, "Waiting Period:")
    draw_checkbox(c, left_margin + 85, y - 1, data.get("waiting_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 96, y, "Yes")
    draw_checkbox(c, left_margin + 118, y - 1, data.get("waiting_no", False))
    c.drawString(left_margin + 129, y, "No")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin + 150, y, "If Yes: How Long:")
    draw_underline_field(c, left_margin + 248, y - 2, 120, data.get("waiting_how_long", ""))

    y -= 14
    c.drawString(left_margin, y, "Missing Tooth Clause:")
    draw_checkbox(c, left_margin + 118, y - 1, data.get("missing_tooth_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 129, y, "Yes")
    draw_checkbox(c, left_margin + 153, y - 1, data.get("missing_tooth_no", False))
    c.drawString(left_margin + 164, y, "No")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin + 185, y, "Age limit for coverage:")
    draw_underline_field(c, left_margin + 310, y - 2, 55, data.get("age_limit_coverage", ""))
    c.drawString(left_margin + 375, y, "Claim filing deadline:")
    draw_underline_field(c, left_margin + 490, y - 2, 70, data.get("claim_filing_deadline", ""))

    y -= 14
    c.drawString(left_margin, y, "Co-ordination of Benefits:")
    draw_underline_field(c, left_margin + 140, y - 2, 115, data.get("coordination_benefits", ""))
    c.drawString(left_margin + 265, y, "Type of Coverage:")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin + 358, y, "Indiv/Indiv & Spouse/Family")

    # =====================================================
    # BENEFIT COVERAGE SECTION
    # =====================================================
    y -= 22
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_margin + 20, y, "•  Benefit Coverage:")

    y -= 16
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "Level 1-Preventive:")
    draw_underline_field(c, left_margin + 108, y - 2, 30, data.get("level1_preventive", ""))
    c.drawString(left_margin + 142, y, "%")

    c.drawString(left_margin + 230, y, "If Prev pays less than 100%, does deductible apply? yes/ no")

    y -= 14
    c.drawString(left_margin, y, "Level 2-Basic:")
    draw_underline_field(c, left_margin + 108, y - 2, 30, data.get("level2_basic", ""))
    c.drawString(left_margin + 142, y, "%")

    c.drawString(left_margin + 230, y, "Does Preventive go against maximum?  yes/ no")

    y -= 14
    c.drawString(left_margin, y, "Level 3-Major:")
    draw_underline_field(c, left_margin + 108, y - 2, 30, data.get("level3_major", ""))
    c.drawString(left_margin + 142, y, "%")

    y -= 14
    c.drawString(left_margin, y, "Endo:")
    draw_underline_field(c, left_margin + 35, y - 2, 25, data.get("endo_pct", ""))
    c.drawString(left_margin + 63, y, "%")
    c.drawString(left_margin + 85, y, "Perio:")
    draw_underline_field(c, left_margin + 115, y - 2, 25, data.get("perio_pct", ""))
    c.drawString(left_margin + 143, y, "%")
    c.drawString(left_margin + 170, y, "Oral Surgery:")
    draw_underline_field(c, left_margin + 240, y - 2, 25, data.get("oral_surgery_pct", ""))
    c.drawString(left_margin + 268, y, "%")

    y -= 14
    c.drawString(left_margin, y, "Buildup (2950):")
    draw_underline_field(c, left_margin + 88, y - 2, 30, data.get("buildup_pct", ""))
    c.drawString(left_margin + 122, y, "%")

    # =====================================================
    # FREQUENCIES / LIMITATIONS SECTION
    # =====================================================
    y -= 22
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_margin + 20, y, "•  Frequencies/Limitations:")

    y -= 16
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "Pan/FMX  Covered:")
    draw_underline_field(c, left_margin + 105, y - 2, 25, data.get("pan_fmx_pct", ""))
    c.drawString(left_margin + 133, y, "%")
    draw_checkbox(c, left_margin + 150, y - 1, data.get("pan_fmx_3yrs", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 161, y, "3yrs")
    draw_checkbox(c, left_margin + 185, y - 1, data.get("pan_fmx_5yrs", False))
    c.drawString(left_margin + 196, y, "5yrs")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin + 220, y, "last taken:")
    draw_underline_field(c, left_margin + 277, y - 2, 120, data.get("pan_fmx_last_taken", ""))

    y -= 14
    c.drawString(left_margin, y, "Exams Covered (0120/0180):")
    draw_checkbox(c, left_margin + 152, y - 1, data.get("exams_1x6mo", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 163, y, "1 x per 6 months")
    draw_checkbox(c, left_margin + 250, y - 1, data.get("exams_2xyr", False))
    c.drawString(left_margin + 261, y, "2 x per year")

    y -= 14
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "Cleanings: (1110/1120):")
    draw_checkbox(c, left_margin + 130, y - 1, data.get("cleanings_1x6mo", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 141, y, "1 x per 6 months")
    draw_checkbox(c, left_margin + 228, y - 1, data.get("cleanings_2xyr", False))
    c.drawString(left_margin + 239, y, "2 x per year")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin + 305, y, "Age for adult prophy:")
    draw_underline_field(c, left_margin + 415, y - 2, 45, data.get("adult_prophy_age", ""))
    c.drawString(left_margin + 470, y, "& over")

    y -= 14
    c.drawString(left_margin, y, "Limited exam: D0140@")
    draw_underline_field(c, left_margin + 122, y - 2, 25, data.get("limited_exam_pct", ""))
    c.drawString(left_margin + 150, y, "%")
    c.drawString(left_margin + 230, y, "Share freq?")
    draw_checkbox(c, left_margin + 292, y - 1, data.get("share_freq_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 303, y, "Y")
    draw_checkbox(c, left_margin + 315, y - 1, data.get("share_freq_no", False))
    c.drawString(left_margin + 326, y, "N")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin + 350, y, "Same day TX?")
    draw_checkbox(c, left_margin + 420, y - 1, data.get("same_day_tx_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 431, y, "Y")
    draw_checkbox(c, left_margin + 445, y - 1, data.get("same_day_tx_no", False))
    c.drawString(left_margin + 456, y, "N")

    y -= 14
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "BWX: (0274/0272)")
    draw_checkbox(c, left_margin + 100, y - 1, data.get("bwx_1x6mo", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 111, y, "1 x per 6 months")
    draw_checkbox(c, left_margin + 198, y - 1, data.get("bwx_1xyr", False))
    c.drawString(left_margin + 209, y, "1 x per year")
    draw_checkbox(c, left_margin + 273, y - 1, data.get("bwx_2xyr", False))
    c.drawString(left_margin + 284, y, "2 x per year")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin + 345, y, "Last taken:")
    draw_underline_field(c, left_margin + 400, y - 2, 100, data.get("bwx_last_taken", ""))

    y -= 14
    c.drawString(left_margin, y, "PA's 0220/0230:")
    draw_underline_field(c, left_margin + 90, y - 2, 30, data.get("pas_pct", ""))
    c.drawString(left_margin + 124, y, "% freq:")
    draw_underline_field(c, left_margin + 160, y - 2, 120, data.get("pas_freq", ""))

    y -= 14
    c.drawString(left_margin, y, "Fluoride (1206): Covered @")
    draw_underline_field(c, left_margin + 155, y - 2, 25, data.get("fluoride_pct", ""))
    c.drawString(left_margin + 183, y, "% up to age")
    draw_underline_field(c, left_margin + 240, y - 2, 30, data.get("fluoride_age", ""))
    draw_checkbox(c, left_margin + 285, y - 1, data.get("fluoride_1x6mo", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 296, y, "1 x per 6 Months")
    draw_checkbox(c, left_margin + 383, y - 1, data.get("fluoride_1xyr", False))
    c.drawString(left_margin + 394, y, "1 x per year")
    draw_checkbox(c, left_margin + 455, y - 1, data.get("fluoride_2xyr", False))
    c.drawString(left_margin + 466, y, "2 x per year")

    y -= 14
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "Sealants (1351): Covered @")
    draw_underline_field(c, left_margin + 155, y - 2, 25, data.get("sealants_pct", ""))
    c.drawString(left_margin + 183, y, "% up to age")
    draw_underline_field(c, left_margin + 240, y - 2, 30, data.get("sealants_age", ""))
    c.drawString(left_margin + 290, y, "times per")
    draw_underline_field(c, left_margin + 340, y - 2, 50, data.get("sealants_times_per", ""))
    c.drawString(left_margin + 400, y, "Premolars:")
    draw_checkbox(c, left_margin + 452, y - 1, data.get("premolars_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 463, y, "Y")
    draw_checkbox(c, left_margin + 478, y - 1, data.get("premolars_no", False))
    c.drawString(left_margin + 489, y, "N")

    y -= 14
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "Replacement period for prosthodontics & crowns:")
    draw_underline_field(c, left_margin + 275, y - 2, 40, data.get("replacement_period", ""))
    c.drawString(left_margin + 320, y, "year replacement  Pays on:")
    draw_checkbox(c, left_margin + 455, y - 1, data.get("pays_on_prep", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 466, y, "Prep")
    draw_checkbox(c, left_margin + 493, y - 1, data.get("pays_on_seat", False))
    c.drawString(left_margin + 504, y, "Seat")

    y -= 14
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "Filling freq? 1 per")
    draw_underline_field(c, left_margin + 100, y - 2, 40, data.get("filling_freq", ""))
    c.drawString(left_margin + 148, y, "Downgrades on fillings?")
    draw_checkbox(c, left_margin + 273, y - 1, data.get("filling_downgrade_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 284, y, "Yes")
    draw_checkbox(c, left_margin + 308, y - 1, data.get("filling_downgrade_no", False))
    c.drawString(left_margin + 319, y, "No")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin + 340, y, "Downgrades on crowns?")
    draw_checkbox(c, left_margin + 460, y - 1, data.get("crown_downgrade_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 471, y, "Yes")
    draw_checkbox(c, left_margin + 495, y - 1, data.get("crown_downgrade_no", False))
    c.drawString(left_margin + 506, y, "No")

    y -= 14
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "D4346: @")
    draw_underline_field(c, left_margin + 53, y - 2, 25, data.get("d4346_pct", ""))
    c.drawString(left_margin + 81, y, "%")
    draw_checkbox(c, left_margin + 95, y - 1, data.get("d4346_1x6mo", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 106, y, "1 x per 6 mos")
    draw_checkbox(c, left_margin + 178, y - 1, data.get("d4346_1xyr", False))
    c.drawString(left_margin + 189, y, "1 x per year")
    draw_checkbox(c, left_margin + 253, y - 1, data.get("d4346_2xyr", False))
    c.drawString(left_margin + 264, y, "2 x per year")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin + 370, y, "Shares w/prophy?")
    draw_checkbox(c, left_margin + 462, y - 1, data.get("d4346_shares_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 473, y, "Y")
    draw_checkbox(c, left_margin + 488, y - 1, data.get("d4346_shares_no", False))
    c.drawString(left_margin + 499, y, "N")

    y -= 14
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "D4355: @")
    draw_underline_field(c, left_margin + 53, y - 2, 25, data.get("d4355_pct", ""))
    c.drawString(left_margin + 81, y, "%")
    c.drawString(left_margin + 120, y, "times per")
    draw_underline_field(c, left_margin + 170, y - 2, 60, data.get("d4355_times_per", ""))
    c.drawString(left_margin + 370, y, "Shares w/prophy?")
    draw_checkbox(c, left_margin + 462, y - 1, data.get("d4355_shares_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 473, y, "Y")
    draw_checkbox(c, left_margin + 488, y - 1, data.get("d4355_shares_no", False))
    c.drawString(left_margin + 499, y, "N")

    y -= 14
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "SRP: (4342/4341) @")
    draw_underline_field(c, left_margin + 112, y - 2, 25, data.get("srp_pct", ""))
    c.drawString(left_margin + 140, y, "%")
    c.drawString(left_margin + 170, y, "Times per")
    draw_underline_field(c, left_margin + 220, y - 2, 70, data.get("srp_times_per", ""))
    c.drawString(left_margin + 340, y, "All 4 quads same day?")
    draw_checkbox(c, left_margin + 460, y - 1, data.get("srp_quads_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 471, y, "Y")
    draw_checkbox(c, left_margin + 488, y - 1, data.get("srp_quads_no", False))
    c.drawString(left_margin + 499, y, "N")

    y -= 14
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "Perio maintenance (4910) @")
    draw_underline_field(c, left_margin + 152, y - 2, 25, data.get("perio_maint_pct", ""))
    c.drawString(left_margin + 180, y, "%")
    draw_checkbox(c, left_margin + 198, y - 1, data.get("perio_maint_1x6mo", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 209, y, "1 x per 6 mos")
    draw_checkbox(c, left_margin + 280, y - 1, data.get("perio_maint_1x", False))
    c.drawString(left_margin + 291, y, "2")
    draw_checkbox(c, left_margin + 305, y - 1, data.get("perio_maint_4xyr", False))
    c.drawString(left_margin + 316, y, "4 x per yr")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin + 370, y, "Shares w/prophy?")
    draw_checkbox(c, left_margin + 462, y - 1, data.get("perio_shares_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 473, y, "Y")
    draw_checkbox(c, left_margin + 488, y - 1, data.get("perio_shares_no", False))
    c.drawString(left_margin + 499, y, "N")

    y -= 14
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "Occlusal guard coverage: (9944)")
    draw_underline_field(c, left_margin + 185, y - 2, 25, data.get("occlusal_pct", ""))
    c.drawString(left_margin + 213, y, "%")
    c.drawString(left_margin + 240, y, "per")
    draw_underline_field(c, left_margin + 260, y - 2, 60, data.get("occlusal_per", ""))
    c.drawString(left_margin + 370, y, "Bruxism only?")
    draw_checkbox(c, left_margin + 445, y - 1, data.get("bruxism_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 456, y, "Y")
    draw_checkbox(c, left_margin + 472, y - 1, data.get("bruxism_no", False))
    c.drawString(left_margin + 483, y, "N")

    y -= 14
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "Implant (6010):")
    draw_underline_field(c, left_margin + 85, y - 2, 25, data.get("implant_pct", ""))
    c.drawString(left_margin + 113, y, "%")
    c.drawString(left_margin + 140, y, "Abutment placement (5057):")
    draw_checkbox(c, left_margin + 290, y - 1, data.get("abutment_placement_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 301, y, "Y")
    draw_checkbox(c, left_margin + 315, y - 1, data.get("abutment_placement_no", False))
    c.drawString(left_margin + 326, y, "N")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin + 345, y, "Abutment/Crown (6058-6059):")
    draw_checkbox(c, left_margin + 500, y - 1, data.get("abutment_crown_yes", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 511, y, "Y")
    draw_checkbox(c, left_margin + 525, y - 1, data.get("abutment_crown_no", False))
    c.drawString(left_margin + 536, y, "N")

    y -= 14
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "Bone graft replacement (D7953):")
    draw_underline_field(c, left_margin + 190, y - 2, 25, data.get("bone_graft_pct", ""))
    c.drawString(left_margin + 218, y, "%")

    y -= 14
    c.drawString(left_margin, y, "Surgical extractions D7220 - D7250:")
    draw_underline_field(c, left_margin + 205, y - 2, 25, data.get("surgical_extraction_pct", ""))
    c.drawString(left_margin + 233, y, "%")
    draw_checkbox(c, left_margin + 260, y - 1, data.get("surgical_dental", False))
    c.setFont("Helvetica", 8)
    c.drawString(left_margin + 271, y, "Dental")
    draw_checkbox(c, left_margin + 305, y - 1, data.get("surgical_medical", False))
    c.drawString(left_margin + 316, y, "Medical")

    # =====================================================
    # NOTES SECTION
    # =====================================================
    y -= 22
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y, "Notes:")
    y -= 4
    c.line(left_margin + 38, y, right_margin, y)
    y -= 14
    c.line(left_margin, y, right_margin, y)
    notes = data.get("notes", "")
    if notes:
        c.setFont("Helvetica", 9)
        c.drawString(left_margin + 40, y + 18, notes)

    c.save()
    buffer.seek(0)
    return buffer
