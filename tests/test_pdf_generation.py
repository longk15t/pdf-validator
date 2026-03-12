"""
Test suite for the Insurance Confirmation PDF generator.

Test case 1:
    - Fill ALL form fields (text + checkboxes) with dummy data.
    - POST to the /generate endpoint.
    - Verify the PDF file is created in the output/ folder.
    - Open the PDF with pdfplumber, extract text content.
    - Assert that every text-field value from the dummy data appears in the PDF.
"""
import os

import pdfplumber
import pytest
import requests

from tests.test_data import TEXT_FIELDS, CHECKBOX_FIELDS
from tests.conftest import BASE_URL


class TestPdfGeneration:
    """Tests for the form-to-PDF generation flow."""

    # ------------------------------------------------------------------
    # Helper: build the POST payload the same way an HTML form would
    # ------------------------------------------------------------------
    @staticmethod
    def _build_form_payload() -> dict:
        """
        Build a dict suitable for ``requests.post(data=...)``.
        - Text fields are key-value strings.
        - Checked checkboxes are included with value ``"on"``
          (same as a browser would send).
        - Unchecked checkboxes are omitted entirely.
        """
        payload = {}
        # Text fields — always present
        payload.update(TEXT_FIELDS)
        # Checkboxes — only include when True
        for field, checked in CHECKBOX_FIELDS.items():
            if checked:
                payload[field] = "on"
        return payload

    # ------------------------------------------------------------------
    # TC-1: Generate PDF and validate content against input data
    # ------------------------------------------------------------------
    def test_generate_pdf_with_all_fields(
        self, flask_server: str, clean_output_dir: str
    ):
        """
        End-to-end test:
        1. POST all dummy data to /generate
        2. Assert the response is a valid PDF download (HTTP 200)
        3. Assert the PDF file exists on disk at output/
        4. Open PDF with pdfplumber and verify every text field value
           is present in the extracted text.
        """
        pdf_path = clean_output_dir
        url = f"{flask_server}/generate"

        # ----- Step 1: Submit the form -----
        payload = self._build_form_payload()
        response = requests.post(url, data=payload, timeout=10)

        # ----- Step 2: Validate HTTP response -----
        assert response.status_code == 200, (
            f"Expected 200 OK but got {response.status_code}"
        )
        assert "application/pdf" in response.headers.get("Content-Type", ""), (
            "Response Content-Type should be application/pdf"
        )

        # ----- Step 3: Validate file existence -----
        assert os.path.exists(pdf_path), (
            f"PDF file was not created at expected path: {pdf_path}"
        )
        file_size = os.path.getsize(pdf_path)
        assert file_size > 0, "PDF file is empty (0 bytes)"

        # ----- Step 4: Read PDF with pdfplumber & validate content -----
        with pdfplumber.open(pdf_path) as pdf:
            assert len(pdf.pages) >= 1, "PDF should have at least 1 page"

            # Extract all text from every page, joined
            full_text = "\n".join(
                page.extract_text() or "" for page in pdf.pages
            )

        # Verify every text-field value appears in the extracted PDF text
        missing_fields = []
        for field_name, expected_value in TEXT_FIELDS.items():
            if expected_value and expected_value not in full_text:
                missing_fields.append((field_name, expected_value))

        assert not missing_fields, (
            "The following text-field values were NOT found in the PDF:\n"
            + "\n".join(
                f"  • {name}: '{value}'" for name, value in missing_fields
            )
            + f"\n\nExtracted PDF text:\n{full_text}"
        )

    # ------------------------------------------------------------------
    # TC-2: Validate the PDF title is present
    # ------------------------------------------------------------------
    def test_pdf_contains_title(
        self, flask_server: str, clean_output_dir: str
    ):
        """
        Verify that the static title 'Insurance Confirmation' appears
        in the generated PDF.
        """
        pdf_path = clean_output_dir
        url = f"{flask_server}/generate"

        payload = self._build_form_payload()
        requests.post(url, data=payload, timeout=10)

        with pdfplumber.open(pdf_path) as pdf:
            full_text = "\n".join(
                page.extract_text() or "" for page in pdf.pages
            )

        assert "Insurance Confirmation" in full_text, (
            "PDF does not contain the expected title 'Insurance Confirmation'"
        )

    # ------------------------------------------------------------------
    # TC-3: Validate static form labels are present in the PDF
    # ------------------------------------------------------------------
    def test_pdf_contains_form_labels(
        self, flask_server: str, clean_output_dir: str
    ):
        """
        Verify key static labels from the form template are present in
        the generated PDF (e.g. section headers, field labels).
        """
        pdf_path = clean_output_dir
        url = f"{flask_server}/generate"

        payload = self._build_form_payload()
        requests.post(url, data=payload, timeout=10)

        with pdfplumber.open(pdf_path) as pdf:
            full_text = "\n".join(
                page.extract_text() or "" for page in pdf.pages
            )

        expected_labels = [
            "Subscriber Name:",
            "Patient Name:",
            "Member ID#:",
            "Employer:",
            "Insurance Information:",
            "Benefit Coverage:",
            "Frequencies/Limitations:",
            "Notes:",
        ]

        missing_labels = [
            label for label in expected_labels if label not in full_text
        ]

        assert not missing_labels, (
            "The following labels were NOT found in the PDF:\n"
            + "\n".join(f"  • {label}" for label in missing_labels)
            + f"\n\nExtracted PDF text:\n{full_text}"
        )
