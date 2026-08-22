from agent.ai_client import ask_ai


prompt = """
Jesteś ekspertem QA.

Wymień 5 najważniejszych testów
dla formularza logowania.

Podaj:
1. Nazwę testu
2. Cel testu
3. Oczekiwany rezultat
"""


result = ask_ai(prompt)

print("\n=== AI QA RESPONSE ===\n")
print(result)