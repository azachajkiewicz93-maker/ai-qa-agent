from pathlib import Path
import shutil


def create_backup(test_file: str) -> Path:

    source = Path(test_file)

    backup = source.with_suffix(
        source.suffix + ".bak"
    )

    shutil.copy2(
        source,
        backup
    )

    return backup


def restore_backup(
    test_file: str,
    backup_file: Path
):

    shutil.copy2(
        backup_file,
        test_file
    )


def remove_backup(
    backup_file: Path
):

    if backup_file.exists():
        backup_file.unlink()