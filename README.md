# Insurance Confirmation PDF Generator

A modern web application built with Python and Flask to generate professionally formatted insurance confirmation PDFs based on the provided Dental Insurance Confirmation template.

## 🚀 Features

- **Modern Web Interface**: Clean, dark-themed UI built with Glassmorphism principles.
- **Full Form Support**: Includes all sections from the standard Dental Insurance Form (Subscriber Info, Benefits, Frequencies, etc.).
- **Precise PDF Generation**: Uses ReportLab to recreate the layout of the sample image with high fidelity.
- **Automated Testing**: Comprehensive test suite with PDF content validation using `pytest` and `pdfplumber`.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Clone the Workspace
Navigate to your project directory.

### 3. Install Dependencies
Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

*Dependencies include: Flask, ReportLab (PDF creation), Pytest (testing suite), Pdfplumber (PDF reading for tests), and Requests.*

---

## 🏃 Running the Application

To start the web server locally:

```bash
python app.py
```

1. Open your browser and navigate to `http://127.0.0.1:5000`.
2. Fill out the form fields.
3. Click the **Export PDF** button.
4. The generated PDF will be saved to the **`output/`** folder and also automatically downloaded by your browser.

---

## 🧪 Running Tests

We use `pytest` for automated end-to-end testing. The tests start a background Flask server on a dedicated port, submit the form with dummy data, and then verify the generated PDF content.

To run the tests:

```bash
python -m pytest tests/ -v
```

### Modifying Test Data
If you want to change the values used in the automated tests (e.g., to verify different names or edge cases), you can edit:

📂 **`tests/test_data.py`**

This file contains two main dictionaries:
- `TEXT_FIELDS`: All string-based values for name, DOB, percentages, etc.
- `CHECKBOX_FIELDS`: Boolean values determines which checkboxes are "checked" in the generated PDF.

---

## 📂 Project Structure

- `app.py`: The main Flask application and routing logic.
- `pdf_generator.py`: Core logic for drawing the PDF using ReportLab.
- `templates/`: HTML templates for the web interface.
- `output/`: Default directory where generated PDFs are stored.
- `tests/`: Automated test suite and configuration.
- `requirements.txt`: List of Python dependencies.