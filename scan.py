import json

from playwright.sync_api import sync_playwright

from agent.page_scanner import scan_page
from agent.ai_client import ask_ai
from agent.test_generator import generate_test_code
from agent.test_writer import save_test


URL = "http://localhost:8000/login.html"


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(URL)

    elements = scan_page(page)

    print("\n=== PAGE ELEMENTS ===\n")

    for element in elements:
        print(element)

    page_data = json.dumps(
        elements,
        indent=2,
        ensure_ascii=False
    )

    prompt = f"""
Jesteś ekspertem QA Automation.

Przeanalizuj elementy strony internetowej
zeskanowane przez Playwright.

ELEMENTY STRONY:

{page_data}

Na podstawie tych elementów:

1. Określ, co można przetestować.
2. Wygeneruj 5 najważniejszych przypadków testowych.
3. Dla każdego przypadku podaj:
   - nazwę testu
   - dane wejściowe
   - oczekiwany rezultat

Nie wymyślaj elementów, których nie ma na stronie.

Odpowiedź przygotuj w języku polskim.
"""

    print("\n=== AI QA ANALYSIS ===\n")

    result = ask_ai(prompt)

    print(result)

    print("\n=== GENERATING PLAYWRIGHT TESTS ===\n")

test_code = generate_test_code(elements, URL)

print(test_code)

test_file = save_test(test_code)

print("\n=== TEST SAVED ===")
print(test_file)
