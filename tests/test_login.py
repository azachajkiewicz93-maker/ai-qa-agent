from playwright.sync_api import Page, expect


def test_successful_login(page: Page):

    page.goto(
        "http://localhost:8000/login.html"
    )

    page.get_by_label("Email").fill(
        "test@example.com"
    )

    page.get_by_label("Password").fill(
        "Password123!"
    )

    page.get_by_role(
        "button",
        name="Login"
    ).click()

    expect(
        page.get_by_text("Login successful")
    ).to_be_visible()


def test_invalid_login(page: Page):

    page.goto(
        "http://localhost:8000/login.html"
    )

    page.get_by_label("Email").fill(
        "wrong@example.com"
    )

    page.get_by_label("Password").fill(
        "WrongPassword"
    )

    page.get_by_role(
        "button",
        name="Login"
    ).click()

    expect(
        page.get_by_text(
            "Invalid email or password"
        )
    ).to_be_visible()