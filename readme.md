# System-test-report

This repo contains:
- **System Testing report** (put your Word/PDF in `/report`)
- **Selenium automated tests** (Python + pytest)
- A GitHub Actions workflow to run tests and publish an HTML report.

## Local run
```bash
python -m venv .venv
# Windows: .\.venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -U pip -r requirements.txt
pytest -q --html=report.html --self-contained-html
