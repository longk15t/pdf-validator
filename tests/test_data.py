"""
Test data module — single source of truth for all form field values
used across test cases.
"""


# ---------------------------------------------------------------------------
# Dummy text field values
# ---------------------------------------------------------------------------
TEXT_FIELDS = {
    # Subscriber & Patient Info
    "subscriber_name": "Long Tran",
    "subscriber_dob": "04/04/1111",
    "patient_name": "Tran Long",
    "patient_dob": "04/04/1111",
    "member_id": "MEM-987654",
    "ss_number": "123-45-6789",
    "reference_number": "REF-2026-03-001",

    # Employer / Group
    "employer": "TechCorp Industries",
    "group_number": "GRP-44210",
    "payor_id": "PAY-88100",
    "group_name": "TechCorp Dental Plan",

    # Insurance Information
    "date_verified": "03/10/2026",
    "effective_date": "01/01/2026",
    "insurance_company": "Delta Dental Premier",
    "claims_address": "123 Insurance Blvd",
    "claims_city": "Sacramento",
    "claims_state": "CA",
    "claims_zip": "95814",
    "phone": "800-555-1234",
    "fax": "800-555-5678",
    "month_start": "January",
    "max_per_year": "2000",
    "used_amount": "350",
    "deductible": "50",
    "deductible_slash": "150",
    "family_deductible": "150",
    "family_deductible_slash": "450",
    "waiting_how_long": "6 months",
    "age_limit_coverage": "26",
    "claim_filing_deadline": "12 months",
    "coordination_benefits": "Standard COB",

    # Benefit Coverage
    "level1_preventive": "100",
    "level2_basic": "80",
    "level3_major": "50",
    "endo_pct": "80",
    "perio_pct": "80",
    "oral_surgery_pct": "80",
    "buildup_pct": "50",

    # Frequencies / Limitations
    "pan_fmx_pct": "100",
    "pan_fmx_last_taken": "06/15/2024",
    "limited_exam_pct": "100",
    "adult_prophy_age": "14",
    "bwx_last_taken": "01/20/2025",
    "pas_pct": "100",
    "pas_freq": "As needed",
    "fluoride_pct": "100",
    "fluoride_age": "16",
    "sealants_pct": "100",
    "sealants_age": "14",
    "sealants_times_per": "1 per tooth",
    "replacement_period": "5",
    "filling_freq": "2 years",
    "d4346_pct": "80",
    "d4355_pct": "80",
    "d4355_times_per": "4 per year",
    "srp_pct": "80",
    "srp_times_per": "Once per quad",
    "perio_maint_pct": "80",
    "occlusal_pct": "50",
    "occlusal_per": "lifetime",
    "implant_pct": "50",
    "bone_graft_pct": "50",
    "surgical_extraction_pct": "80",

    # Notes
    "notes": "Em làm cái này có 30 phút thôi cô",
}

# ---------------------------------------------------------------------------
# Dummy checkbox values  (True = checked)
# ---------------------------------------------------------------------------
CHECKBOX_FIELDS = {
    "network_in": True,
    "network_out": False,
    "waiting_yes": False,
    "waiting_no": True,
    "missing_tooth_yes": True,
    "missing_tooth_no": False,
    "pan_fmx_3yrs": False,
    "pan_fmx_5yrs": True,
    "exams_1x6mo": True,
    "exams_2xyr": False,
    "cleanings_1x6mo": True,
    "cleanings_2xyr": False,
    "share_freq_yes": False,
    "share_freq_no": True,
    "same_day_tx_yes": True,
    "same_day_tx_no": False,
    "bwx_1x6mo": True,
    "bwx_1xyr": False,
    "bwx_2xyr": False,
    "fluoride_1x6mo": True,
    "fluoride_1xyr": False,
    "fluoride_2xyr": False,
    "premolars_yes": False,
    "premolars_no": True,
    "pays_on_prep": False,
    "pays_on_seat": True,
    "filling_downgrade_yes": True,
    "filling_downgrade_no": False,
    "crown_downgrade_yes": False,
    "crown_downgrade_no": True,
    "d4346_1x6mo": False,
    "d4346_1xyr": True,
    "d4346_2xyr": False,
    "d4346_shares_yes": True,
    "d4346_shares_no": False,
    "d4355_shares_yes": False,
    "d4355_shares_no": True,
    "srp_quads_yes": True,
    "srp_quads_no": False,
    "perio_maint_1x6mo": False,
    "perio_maint_1x": False,
    "perio_maint_4xyr": True,
    "perio_shares_yes": True,
    "perio_shares_no": False,
    "bruxism_yes": True,
    "bruxism_no": False,
    "abutment_placement_yes": True,
    "abutment_placement_no": False,
    "abutment_crown_yes": True,
    "abutment_crown_no": False,
    "surgical_dental": True,
    "surgical_medical": False,
}
