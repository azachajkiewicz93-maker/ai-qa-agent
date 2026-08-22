from agent.ai_client import ask_ai


def generate_test_code(page_elements: list, url: str) -> str:

    prompt = f"""
Jesteś ekspertem QA Automation.

Twoim zadaniem jest wygenerowanie kodu testów
dla pytest-playwright.

URL:
{url}

ELEMENTY STRONY:
{page_elements}

BARDZO WAŻNE — ZASADY KODU:

1. Używaj WYŁĄCZNIE synchronicznego Playwright.
2. Każdy test musi mieć dokładnie postać:

def test_nazwa(page):

3. NIE używaj:
   - async def
   - await
   - pytest.mark.async_playwright
   - async_playwright
   - sync_playwright
   - browser.new_page()
   - chromium.launch()

4. Używaj fixture `page` dostarczanej przez pytest-playwright.

5. Każdy test powinien zaczynać się od:

page.goto("{url}")

6. Używaj wyłącznie locatorów wynikających
   z ELEMENTÓW STRONY.

7. Nie wymyślaj żadnych elementów ani URL.

8. Wygeneruj dokładnie 3 testy:
   - sprawdzenie pola email
   - sprawdzenie pola password
   - próba wykonania logowania

9. Kod musi być gotowy do uruchomienia poleceniem:

pytest

10. Zwróć WYŁĄCZNIE kod Python.

11. NIE dodawaj:
   - import pytest
   - import Playwright
   - dekoratorów pytest
   - komentarzy
   - markdown
   - ```python

PRZYKŁAD POPRAWNEGO TESTU:

def test_email_field_exists(page):
    page.goto("{url}")
    email = page.locator("#email")
    assert email.is_visible()

Teraz wygeneruj 3 testy.
"""

    response = ask_ai(prompt)

    response = response.replace("```python", "")
    response = response.replace("```", "")

    return response.strip()