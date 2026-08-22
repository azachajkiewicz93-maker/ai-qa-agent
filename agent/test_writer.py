from pathlib import Path


def save_test(test_code: str) -> Path:

    output_dir = Path("tests/ai_generated")

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = output_dir / "test_ai_generated.py"

    output_file.write_text(
        test_code,
        encoding="utf-8"
    )

    return output_file