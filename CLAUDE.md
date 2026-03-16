# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📦 Project Overview

Insurance Confirmation PDF Generator - A Flask web application that creates professionally formatted insurance confirmation PDFs using ReportLab, based on form data submitted via a web interface.

## 🛠️ Commands

### Development
```bash
# Start the web server
python app.py

# Navigate to http://127.0.0.1:5000 in your browser
```

### Testing
```bash
# Run all tests
python -m pytest tests/ -v

# Run a single test
python -m pytest tests/test_pdf_generation.py::TestPdfGeneration::test_generate_pdf_with_all_fields -v

# Run tests with coverage (if you want to add it later)
python -m pytest tests/ -v --cov=pdf_generator
```

### Modifying Test Data
To change the dummy data used in automated tests:
- Edit `tests/test_data.py` - contains `TEXT_FIELDS` and `CHECKBOX_FIELDS` dictionaries

## 🏗️ Architecture Overview

The application follows a simple MVC-like structure:

```
pdf-validator/
├── app.py                 # Flask app with routes and form handling
│   ├── / route → index() → renders templates/index.html
│   └── /generate route → generate() → processes form, saves PDF
│
├── pdf_generator.py       # Core PDF generation logic using ReportLab
│   ├── draw_checkbox()    # Draws a checkbox with optional checkmark
│   ├── draw_underline_field()  # Creates underlined text field with wrapping
│   ├── get_underline_field_height()  # Calculates height for wrapped text
│   ├── PDFLayout class    # Manages page layout, margins, and page breaks
│   └── generate_pdf()     # Main entry point - builds multi-page PDF
│
├── templates/             # Flask HTML templates
│   └── index.html        # Form UI with glassmorphism dark theme
│
├── tests/                 # Pytest test suite with end-to-end testing
│   ├── conftest.py       # pytest fixtures (flask_server, clean_output_dir)
│   ├── test_data.py      # Test data dictionaries
│   └── test_pdf_generation.py  # Test cases for PDF content validation
│
└── output/                # Generated PDFs are saved here
```

### Key Design Patterns

1. **PDF Layout Management** (`pdf_generator.py:PDFLayout`):
   - Uses `check_page_break()` to detect when vertical space is insufficient
   - Automatically adds page numbers before starting a new page
   - Handles multi-line text wrapping via `simpleSplit()`

2. **Form-Driven Generation**:
   - `app.py` extracts both text fields and checkboxes from the form submission
   - Text fields are always included in the PDF (may be empty)
   - Checkbox fields only appear if they were checked in the form

3. **Text Wrapping Support**:
   - Long field values (e.g., insurance company name) automatically wrap
   - The `check_page_break()` call after drawing content ensures proper page breaks

## 📝 Important Implementation Details

### Text Field Rendering
- Empty fields show only the underline box
- Multi-line text is handled via `simpleSplit()` and renders multiple lines under a single underline

### Checkbox Logic
- A checkbox is "checked" if it exists in `request.form` (HTML sends "on" when checked)
- Unchecked checkboxes are not included in the form data at all

### Page Break Strategy
1. After drawing content, estimate the height needed for remaining sections
2. Call `check_page_break(estimated_height)` before starting new sections
3. This prevents underflow and ensures clean page breaks

### Multi-Page PDFs
- Page numbers are added at the bottom of each page (`c.drawCentredString(..., "Page {n}")`)
- The footer is drawn on page 1, then pages start at a different Y position

## 🔧 Common Development Tasks

### Adding a New Form Field
1. Add the field name to `app.py`'s `text_fields` or `checkbox_fields` list
2. Add the draw call in `pdf_generator.py` under the appropriate section
3. Update the HTML form template if needed

### Running Specific Test Types
```bash
# Test PDF content validation only
python -m pytest tests/test_pdf_generation.py::TestPdfGeneration::test_generate_pdf_with_all_fields -v

# Test title presence
python -m pytest tests/test_pdf_generation.py::TestPdfGeneration::test_pdf_contains_title -v

# Test form labels
python -m pytest tests/test_pdf_generation.py::TestPdfGeneration::test_pdf_contains_form_labels -v
```

## 📁 Dependencies
- Flask: Web framework
- ReportLab: PDF generation
- Pytest: Testing framework
- pdfplumber: PDF reading for test validation
- Requests: HTTP client for tests
