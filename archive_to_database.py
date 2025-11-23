#!/usr/bin/env python3
"""
AIOS Database Archival Script
=============================

Archives consciousness metrics template files to the AIOS database infrastructure
instead of cluttering the filesystem. Uses content-hash deduplication for efficient storage.

AINLP Classification: Database Infrastructure Layer
Purpose: Clean archival of consciousness metrics templates
Files: test_consciousness_*.py backup files
Target: ai/tools/database/tachyonic/aios_data.db

Created: November 23, 2025
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# Add AI paths
sys.path.insert(0, str(Path(__file__).parent / "ai"))

from ai.tools.database.aios_database import AIOSDatabase


def archive_files_to_database():
    """Archive consciousness metrics files to AIOS database."""

    print("🗄️ AIOS Database Archival - Consciousness Metrics Templates")
    print("=" * 60)

    # Initialize database connection
    db_path = Path("ai/tools/database/tachyonic/aios_data.db")
    db = AIOSDatabase(str(db_path))

    # Archive directory
    archive_dir = Path("tachyonic_archive/consciousness_metrics_backups")

    if not archive_dir.exists():
        print("❌ Archive directory not found")
        return False

    archived_files = []
    total_size = 0

    # Archive each file
    for file_path in archive_dir.glob("*"):
        if file_path.is_file() and ('.py' in file_path.name or '.json' in file_path.name):
            print(f"\n📁 Processing: {file_path.name}")

            # Read file content
            with open(file_path, 'rb') as f:
                content = f.read()

            # Archive to database
            backup_id, content_hash, is_duplicate = db.add_backup(
                filename=file_path.name,
                file_path=str(file_path),
                content=content,
                backup_timestamp=datetime.now(),
                file_type="python",
                backup_type="consciousness_metrics_template"
            )

            archived_files.append({
                "filename": file_path.name,
                "backup_id": backup_id,
                "content_hash": content_hash,
                "is_duplicate": is_duplicate,
                "size": len(content)
            })

            total_size += len(content)

            status = "🔄 Duplicate" if is_duplicate else "✅ New"
            print(f"   {status} - ID: {backup_id}, Hash: {content_hash[:8]}..., Size: {len(content)} bytes")

    # Update archival metadata
    metadata_file = archive_dir / "archival_metadata.json"
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)

        metadata.update({
            "database_archival_timestamp": datetime.now().isoformat(),
            "database_location": str(db_path),
            "archived_files": archived_files,
            "total_size_bytes": total_size,
            "deduplication_applied": True,
            "filesystem_cleanup": True
        })

        # Archive metadata file itself
        with open(metadata_file, 'rb') as f:
            metadata_content = f.read()

        backup_id, content_hash, is_duplicate = db.add_backup(
            filename="archival_metadata.json",
            file_path=str(metadata_file),
            content=metadata_content,
            backup_timestamp=datetime.now(),
            file_type="json",
            backup_type="archival_metadata"
        )

        print(f"\n📋 Metadata archived - ID: {backup_id}")

    # Clean up filesystem (remove archived files)
    print("\n🧹 Cleaning up filesystem clutter...")
    for file_path in archive_dir.glob("*"):
        if file_path.is_file():
            file_path.unlink()
            print(f"   🗑️ Removed: {file_path.name}")

    # Remove empty directory
    if archive_dir.exists() and not list(archive_dir.iterdir()):
        archive_dir.rmdir()
        print(f"   🗑️ Removed empty directory: {archive_dir.name}")

    db.close()

    print("\n✅ Database archival complete!")
    print(f"   📊 Files archived: {len(archived_files)}")
    print(f"   💾 Total size: {total_size} bytes")
    print(f"   🗄️ Database: {db_path}")

    return True


if __name__ == "__main__":
    success = archive_files_to_database()
    sys.exit(0 if success else 1)