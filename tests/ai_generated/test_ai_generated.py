def test_login_attempt(page):
    page.goto("http://localhost:8000/login.html")
    page.locator("#email").fill("test@example.com")
    page.locator("#password").fill("password123")
    page.locator("button:has-text('Login')").click()