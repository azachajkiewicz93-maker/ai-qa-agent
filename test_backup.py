from pathlib import Path

from agent.backup import (
    create_backup,
    restore_backup,
    remove_backup
)


TEST_FILE = "tests/ai_generated/test_ai_generated.py"


print("\n=== BACKUP/ROLLBACK TEST ===\n")


# ==========================================
# 1. READ ORIGINAL
# ==========================================

original = Path(TEST_FILE).read_text(
    encoding="utf-8"
)

print("Original test loaded.")


# ==========================================
# 2. CREATE BACKUP
# ==========================================

backup = create_backup(
    TEST_FILE
)

print(
    f"Backup created: {backup}"
)


# ==========================================
# 3. SIMULATE BAD AI FIX
# ==========================================

Path(TEST_FILE).write_text(
    "# THIS IS A BROKEN AI FIX\n"
    "THIS CODE IS INVALID!!!",
    encoding="utf-8"
)

print(
    "\nSimulated bad AI fix."
)


# ==========================================
# 4. VERIFY THAT FILE CHANGED
# ==========================================

changed = Path(TEST_FILE).read_text(
    encoding="utf-8"
)

if changed == original:

    print(
        "ERROR: Test file did not change."
    )

    remove_backup(backup)

    raise SystemExit(1)


print(
    "Test file successfully modified."
)


# ==========================================
# 5. ROLLBACK
# ==========================================

print(
    "\n=== RESTORING BACKUP ==="
)

restore_backup(
    TEST_FILE,
    backup
)

print(
    "Backup restored."
)


# ==========================================
# 6. REMOVE BACKUP
# ==========================================

remove_backup(
    backup
)

print(
    "Backup removed."
)


# ==========================================
# 7. VERIFY RESTORE
# ==========================================

restored = Path(TEST_FILE).read_text(
    encoding="utf-8"
)


if restored == original:

    print(
        "\n=== ROLLBACK SUCCESSFUL ==="
    )

else:

    print(
        "\n=== ROLLBACK FAILED ==="
    )

    raise SystemExit(1)