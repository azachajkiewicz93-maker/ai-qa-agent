from datetime import datetime
from pathlib import Path
from html import escape
import shutil


REPORTS_DIR = Path("reports")
HISTORY_DIR = REPORTS_DIR / "history"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

HISTORY_DIR.mkdir(
    parents=True,
    exist_ok=True
)

SCREENSHOTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def create_report(
    initial_status,
    final_status,
    fixes,
    attempts,
    error=None,
    analysis=None,
    screenshot=None
):
    """
    Tworzy raport HTML i TXT.
    Każde uruchomienie jest zapisywane w historii.
    """

    timestamp = datetime.now()

    timestamp_display = timestamp.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    timestamp_file = timestamp.strftime(
        "%Y%m%d_%H%M%S"
    )

    # ==========================================
    # STATUS
    # ==========================================

    if final_status == "PASS":
        status_class = "pass"
        status_text = "PASS"
    else:
        status_class = "fail"
        status_text = "FAIL"

    # ==========================================
    # SAFE HTML VALUES
    # ==========================================

    error_html = ""

    if error:
        error_html = f"""
        <section>
            <h2>Test Failure</h2>
            <pre>{escape(error)}</pre>
        </section>
        """

    analysis_html = ""

    if analysis:
        analysis_html = f"""
        <section>
            <h2>AI Analysis</h2>
            <pre>{escape(analysis)}</pre>
        </section>
        """

    screenshot_html = ""

    if screenshot:

        screenshot_path = Path(screenshot)

        if screenshot_path.exists():

            # Kopiujemy screenshot do historycznego katalogu.
            screenshot_copy = (
                HISTORY_DIR
                / f"{timestamp_file}_{screenshot_path.name}"
            )

            shutil.copy2(
                screenshot_path,
                screenshot_copy
            )

            screenshot_html = f"""
            <section>
                <h2>Failure Screenshot</h2>

                <img
                    src="{screenshot_copy.name}"
                    alt="Failure screenshot"
                >
            </section>
            """

    # ==========================================
    # HTML REPORT
    # ==========================================

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<title>AI QA Agent Report</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #f4f4f4;
    margin: 40px;
}}

.container {{
    max-width: 1100px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 10px;
}}

h1 {{
    margin-top: 0;
}}

h2 {{
    margin-top: 30px;
}}

.status {{
    padding: 15px;
    border-radius: 8px;
    font-size: 22px;
    font-weight: bold;
}}

.pass {{
    background: #d4edda;
    color: #155724;
}}

.fail {{
    background: #f8d7da;
    color: #721c24;
}}

.info {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 20px 0;
}}

.card {{
    background: #f7f7f7;
    padding: 15px;
    border-radius: 6px;
}}

pre {{
    background: #111;
    color: #eee;
    padding: 20px;
    overflow-x: auto;
    border-radius: 6px;
    white-space: pre-wrap;
}}

img {{
    max-width: 100%;
    border: 1px solid #ccc;
    border-radius: 6px;
}}

</style>

</head>

<body>

<div class="container">

<h1>🤖 AI QA Agent Report</h1>

<div class="status {status_class}">
Final Status: {status_text}
</div>

<div class="info">

<div class="card">
<strong>Initial Status</strong>
<br>
{escape(str(initial_status))}
</div>

<div class="card">
<strong>Final Status</strong>
<br>
{escape(str(final_status))}
</div>

<div class="card">
<strong>AI Fixes</strong>
<br>
{fixes}
</div>

<div class="card">
<strong>Attempts</strong>
<br>
{attempts}
</div>

<div class="card">
<strong>Date</strong>
<br>
{timestamp_display}
</div>

</div>

{error_html}

{analysis_html}

{screenshot_html}

</div>

</body>

</html>
"""

    # ==========================================
    # SAVE HISTORY HTML
    # ==========================================

    history_html = (
        HISTORY_DIR
        / f"run_{timestamp_file}.html"
    )

    history_html.write_text(
        html,
        encoding="utf-8"
    )

    # ==========================================
    # UPDATE LATEST HTML
    # ==========================================

    latest_html = (
        REPORTS_DIR
        / "latest_report.html"
    )

    latest_html.write_text(
        html,
        encoding="utf-8"
    )

    # ==========================================
    # TXT REPORT
    # ==========================================

    txt = f"""
AI QA AGENT REPORT
==================

Date:
{timestamp_display}

Initial status:
{initial_status}

Final status:
{final_status}

AI fixes:
{fixes}

Attempts:
{attempts}
"""

    if error:
        txt += f"""

TEST FAILURE
============

{error}
"""

    if analysis:
        txt += f"""

AI ANALYSIS
===========

{analysis}
"""

    history_txt = (
        HISTORY_DIR
        / f"run_{timestamp_file}.txt"
    )

    history_txt.write_text(
        txt.strip(),
        encoding="utf-8"
    )

    latest_txt = (
        REPORTS_DIR
        / "latest_report.txt"
    )

    latest_txt.write_text(
        txt.strip(),
        encoding="utf-8"
    )

    return str(latest_html)