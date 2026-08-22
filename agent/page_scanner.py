from playwright.sync_api import Page


def scan_page(page: Page):

    elements = page.locator(
        "input, button, textarea, select, a"
    )

    result = []

    for i in range(elements.count()):

        element = elements.nth(i)

        tag = element.evaluate(
            "(element) => element.tagName"
        )

        element_id = element.get_attribute("id")
        name = element.get_attribute("name")
        element_type = element.get_attribute("type")
        placeholder = element.get_attribute(
            "placeholder"
        )

        try:
            text = element.inner_text()
        except Exception:
            text = ""

        result.append({
            "tag": tag,
            "id": element_id,
            "name": name,
            "type": element_type,
            "placeholder": placeholder,
            "text": text
        })

    return result