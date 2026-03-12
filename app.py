"""
Flask web application for Insurance Confirmation PDF generation.
Run this file and visit http://localhost:5000 to use the form.
"""
import os
from flask import Flask, render_template, request, send_file, jsonify
from pdf_generator import generate_pdf

app = Flask(__name__)

# Output directory for exported PDFs
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def index():
    """Render the main form page."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """Process the form data, save PDF to output/ folder, and return it."""
    data = {}

    # --- Text fields ---
    text_fields = [
        "subscriber_name", "subscriber_dob", "patient_name", "patient_dob",
        "member_id", "ss_number", "reference_number",
        "employer", "group_number", "payor_id", "group_name",
        "date_verified", "effective_date", "insurance_company",
        "claims_address", "claims_city", "claims_state", "claims_zip",
        "phone", "fax", "month_start",
        "max_per_year", "used_amount",
        "deductible", "deductible_slash", "family_deductible", "family_deductible_slash",
        "waiting_how_long", "age_limit_coverage", "claim_filing_deadline",
        "coordination_benefits",
        "level1_preventive", "level2_basic", "level3_major",
        "endo_pct", "perio_pct", "oral_surgery_pct", "buildup_pct",
        "pan_fmx_pct", "pan_fmx_last_taken",
        "limited_exam_pct",
        "adult_prophy_age",
        "bwx_last_taken",
        "pas_pct", "pas_freq",
        "fluoride_pct", "fluoride_age",
        "sealants_pct", "sealants_age", "sealants_times_per",
        "replacement_period",
        "filling_freq",
        "d4346_pct", "d4355_pct", "d4355_times_per",
        "srp_pct", "srp_times_per",
        "perio_maint_pct",
        "occlusal_pct", "occlusal_per",
        "implant_pct",
        "bone_graft_pct", "surgical_extraction_pct",
        "notes",
    ]

    for field in text_fields:
        data[field] = request.form.get(field, "")

    # --- Checkbox fields ---
    checkbox_fields = [
        "network_in", "network_out",
        "waiting_yes", "waiting_no",
        "missing_tooth_yes", "missing_tooth_no",
        "pan_fmx_3yrs", "pan_fmx_5yrs",
        "exams_1x6mo", "exams_2xyr",
        "cleanings_1x6mo", "cleanings_2xyr",
        "share_freq_yes", "share_freq_no",
        "same_day_tx_yes", "same_day_tx_no",
        "bwx_1x6mo", "bwx_1xyr", "bwx_2xyr",
        "fluoride_1x6mo", "fluoride_1xyr", "fluoride_2xyr",
        "premolars_yes", "premolars_no",
        "pays_on_prep", "pays_on_seat",
        "filling_downgrade_yes", "filling_downgrade_no",
        "crown_downgrade_yes", "crown_downgrade_no",
        "d4346_1x6mo", "d4346_1xyr", "d4346_2xyr",
        "d4346_shares_yes", "d4346_shares_no",
        "d4355_shares_yes", "d4355_shares_no",
        "srp_quads_yes", "srp_quads_no",
        "perio_maint_1x6mo", "perio_maint_1x", "perio_maint_4xyr",
        "perio_shares_yes", "perio_shares_no",
        "bruxism_yes", "bruxism_no",
        "abutment_placement_yes", "abutment_placement_no",
        "abutment_crown_yes", "abutment_crown_no",
        "surgical_dental", "surgical_medical",
    ]

    for field in checkbox_fields:
        data[field] = field in request.form

    # Generate the PDF
    pdf_buffer = generate_pdf(data)

    # Save to output/ folder
    output_path = os.path.join(OUTPUT_DIR, "insurance_confirmation.pdf")
    with open(output_path, "wb") as f:
        f.write(pdf_buffer.read())

    # Return the saved file to the browser as well
    return send_file(
        output_path,
        as_attachment=True,
        download_name="insurance_confirmation.pdf",
        mimetype="application/pdf",
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
