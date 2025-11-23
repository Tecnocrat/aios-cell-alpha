#!/usr/bin/env python3
"""
AIOS Database Migration Rollback Script
Restores databases from backup if consolidation needs to be undone.
"""

import shutil
from pathlib import Path

backup_dir = Path("/workspace/database_migration_backup")
root_path = Path("/workspace")

# Original database paths
original_paths = {"main_aios": PosixPath("/workspace/ai/tools/database/tachyonic/aios_data.db"), "tachyonic_archive": PosixPath("/workspace/tachyonic/archive/code_archive.db"), "legacy_tachyonic": PosixPath("/workspace/tachyonic/aios_data.db"), "knowledge_crystals": PosixPath("/workspace/runtime/context/knowledge_crystals.db"), "docs_archive": PosixPath("/workspace/docs/archive/tachyonic/tachyonic_archive.db")}

print("🔄 Rolling back database consolidation...")

# Remove consolidated database
consolidated_db = root_path / "database" / "aios_data.db"
if consolidated_db.exists():
    consolidated_db.unlink()
    print("✅ Removed consolidated database")

# Restore from backups
for db_name, original_path in original_paths.items():
    backup_files = list(backup_dir.glob(f"{db_name}_backup_*.db"))
    if backup_files:
        latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
        shutil.copy2(latest_backup, original_path)
        print(f"✅ Restored {db_name} from {latest_backup}")
    else:
        print(f"⚠️  No backup found for {db_name}")

print("✅ Rollback complete")
