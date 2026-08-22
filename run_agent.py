import subprocess
from pathlib import Path

from agent.error_analyzer import (
    analyze_failure,
    extract_fixed_code
)

from agent.reporter import create_report

from agent.backup import (
    create_backup,
    restore_backup,
    remove_backup
)


TEST_FILE = "tests/ai_generated/test_ai_generated.py"

MAX_RETRIES = 3

SCREENSHOTS_DIR = Path(
    "reports/screenshots"
)


def run_tests():
    """Uruchamia pytest dla wygenerowanego testu."""

    return subprocess.run(
        [
            "pytest",
            TEST_FILE,
            "-v"
        ],
        capture_output=True,
        text=True
    )


def read_test_code():
    """Odczytuje aktualny kod testu."""

    with open(
        TEST_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


def save_test_code(code):
    """Zapisuje kod testu."""

    with open(
        TEST_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(code)


def get_latest_screenshot():
    """
    Zwraca najnowszy screenshot albo None.
    """

    if not SCREENSHOTS_DIR.exists():
        return None

    screenshots = list(
        SCREENSHOTS_DIR.glob("*.png")
    )

    if not screenshots:
        return None

    return max(
        screenshots,
        key=lambda file: file.stat().st_mtime
    )


def main():

    fixes = 0
    attempts = 0

    initial_status = "UNKNOWN"
    final_status = "UNKNOWN"

    last_analysis = None
    latest_screenshot = None

    print("\n=== AI QA AGENT ===\n")

    for attempt in range(MAX_RETRIES + 1):

        attempts += 1

        print(
            f"\n=== TEST RUN #{attempts} ===\n"
        )

        result = run_tests()

        print(result.stdout)

        # ==========================================
        # INITIAL RESULT
        # ==========================================

        if attempts == 1:

            if result.returncode == 0:
                initial_status = "PASS"
            else:
                initial_status = "FAIL"

        # ==========================================
        # TESTS PASSED
        # ==========================================

        if result.returncode == 0:

            final_status = "PASS"

            latest_screenshot = get_latest_screenshot()

            print(
                "\n=== ALL TESTS PASSED ===\n"
            )

            print(
                f"Agent finished after "
                f"{fixes} fix(es)."
            )

            report_file = create_report(
                initial_status=initial_status,
                final_status=final_status,
                fixes=fixes,
                attempts=attempts,
                analysis=last_analysis,
                screenshot=latest_screenshot
            )

            print(
                f"Report saved to: {report_file}"
            )

            return

        # ==========================================
        # FAILURE
        # ==========================================

        print(
            "\n=== TEST FAILURE DETECTED ===\n"
        )

        latest_screenshot = get_latest_screenshot()

        error_output = (
            result.stdout
            + "\n"
            + result.stderr
        )

        test_code = read_test_code()

        # ==========================================
        # MAX RETRIES
        # ==========================================

        if attempts > MAX_RETRIES:

            final_status = "FAIL"

            print(
                "\n=== MAX RETRIES REACHED ===\n"
            )

            report_file = create_report(
                initial_status=initial_status,
                final_status=final_status,
                fixes=fixes,
                attempts=attempts,
                error=error_output,
                analysis=last_analysis,
                screenshot=latest_screenshot
            )

            print(
                "AI could not fix the test "
                "within the allowed number of attempts."
            )

            print(
                f"Report saved to: {report_file}"
            )

            return

        # ==========================================
        # AI ANALYSIS
        # ==========================================

        print(
            "\n=== AI ANALYZING FAILURE ===\n"
        )

        analysis = analyze_failure(
            test_code,
            error_output
        )

        last_analysis = analysis

        print(analysis)

        # ==========================================
        # AI FIX
        # ==========================================

        print(
            "\n=== AI GENERATING FIX ===\n"
        )

        try:

            fixed_code = extract_fixed_code(
                analysis
            )

        except ValueError as error:

            print(
                f"\nERROR: {error}"
            )

            final_status = "FAIL"

            report_file = create_report(
                initial_status=initial_status,
                final_status=final_status,
                fixes=fixes,
                attempts=attempts,
                error=error_output,
                analysis=analysis,
                screenshot=latest_screenshot
            )

            print(
                f"Report saved to: {report_file}"
            )

            return

        fixes += 1

        print(
            "\n=== GENERATED FIX ===\n"
        )

        print(fixed_code)

        # ==========================================
        # BACKUP
        # ==========================================

        print(
            "\n=== CREATING BACKUP ===\n"
        )

        backup_file = create_backup(
            TEST_FILE
        )

        print(
            f"Backup created: {backup_file}"
        )

        # ==========================================
        # SAVE FIX
        # ==========================================

        print(
            "\n=== SAVING FIX ===\n"
        )

        save_test_code(
            fixed_code
        )

        print(
            f"Fixed test saved to: {TEST_FILE}"
        )

        # ==========================================
        # VERIFY FIX
        # ==========================================

        print(
            "\n=== VERIFYING AI FIX ===\n"
        )

        verification = run_tests()

        print(
            verification.stdout
        )

        # ==========================================
        # FIX SUCCESSFUL
        # ==========================================

        if verification.returncode == 0:

            final_status = "PASS"

            remove_backup(
                backup_file
            )

            latest_screenshot = get_latest_screenshot()

            print(
                "\n=== AI FIX SUCCESSFUL ===\n"
            )

            report_file = create_report(
                initial_status=initial_status,
                final_status=final_status,
                fixes=fixes,
                attempts=attempts + 1,
                analysis=analysis,
                screenshot=latest_screenshot
            )

            print(
                f"Report saved to: {report_file}"
            )

            return

        # ==========================================
        # FIX FAILED → ROLLBACK
        # ==========================================

        print(
            "\n=== AI FIX FAILED ===\n"
        )

        print(
            "Restoring previous test..."
        )

        restore_backup(
            TEST_FILE,
            backup_file
        )

        remove_backup(
            backup_file
        )

        print(
            "Previous test restored."
        )

    # ==========================================
    # SAFETY FALLBACK
    # ==========================================

    final_status = "FAIL"

    report_file = create_report(
        initial_status=initial_status,
        final_status=final_status,
        fixes=fixes,
        attempts=attempts,
        analysis=last_analysis,
        screenshot=latest_screenshot
    )

    print(
        f"Report saved to: {report_file}"
    )


if __name__ == "__main__":
    main()