from agent.ai_client import ask_ai


def analyze_failure(test_code: str, error_output: str) -> str:

    prompt = f"""
Jesteś ekspertem QA Automation i Playwright.

Test wygenerowany przez AI zakończył się błędem.

=== TEST CODE ===

{test_code}

=== PYTEST ERROR ===

{error_output}

Przeanalizuj błąd i zaproponuj poprawkę.

Zwróć odpowiedź dokładnie w tym formacie:

ANALIZA:
<krótkie wyjaśnienie problemu>

POPRAWIONY KOD:
<cały poprawiony kod testu>

WAŻNE:
- zachowaj wszystkie testy, które nie są związane z błędem
- popraw tylko to, co jest konieczne
- używaj pytest-playwright
- używaj fixture page
- nie używaj async
- nie używaj sync_playwright
- nie wymyślaj elementów strony
- kod musi być poprawnym Pythonem
- w sekcji POPRAWIONY KOD zwróć kompletny plik
"""

    return ask_ai(prompt)

def extract_fixed_code(ai_response: str) -> str:

    marker = "POPRAWIONY KOD:"

    if marker not in ai_response:
        raise ValueError(
            "AI nie zwróciło sekcji POPRAWIONY KOD."
        )

    fixed_code = ai_response.split(
        marker,
        1
    )[1]

    fixed_code = fixed_code.strip()

    fixed_code = fixed_code.replace(
        "```python",
        ""
    )

    fixed_code = fixed_code.replace(
        "```",
        ""
    )

    return fixed_code.strip()