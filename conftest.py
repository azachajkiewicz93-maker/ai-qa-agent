import pytest
from pathlib import Path
from datetime import datetime


SCREENSHOTS_DIR = Path(
    "reports/screenshots"
)

SCREENSHOTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@pytest.fixture
def page(page):

    yield page


@pytest.fixture(
    autouse=True
)
def screenshot_on_failure(
    request,
    page
):

    yield

    if hasattr(
        request.node,
        "rep_call"
    ):

        if request.node.rep_call.failed:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            test_name = request.node.name.replace(
                "[",
                "_"
            ).replace(
                "]",
                ""
            )

            screenshot_path = (
                SCREENSHOTS_DIR
                / f"{test_name}_{timestamp}.png"
            )

            page.screenshot(
                path=str(
                    screenshot_path
                ),
                full_page=True
            )


@pytest.hookimpl(
    hookwrapper=True
)
def pytest_runtest_makereport(
    item,
    call
):

    outcome = yield

    rep = outcome.get_result()

    setattr(
        item,
        f"rep_{rep.when}",
        rep
    )