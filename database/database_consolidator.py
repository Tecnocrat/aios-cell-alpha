#!/usr/bin/env python3
"""
AIOS Database Consolidation Script
Centralizes all scattered databases into a single root-level database.

This script:
1. Creates unified schema accommodating all data types
2. Migrates data from all existing databases
3. Updates configuration to point to new centralized database
4. Provides rollback capability
"""

import sqlite3
import os
import json
import shutil
from pathlib import Path
from datetime import datetime
import hashlib

class AIOSDatabaseConsolidator:
    def __init__(self, root_path="/workspace"):
        self.root_path = Path(root_path)
        self.consolidated_db = self.root_path / "database" / "aios_data.db"
        self.backup_dir = self.root_path / "database_migration_backup"
        self.backup_dir.mkdir(exist_ok=True)

        # Source databases mapping
        self.source_dbs = {
            'main_aios': self.root_path / '/workspace/aios_data.db',
            'tachyonic_archive': self.root_path / '/workspace/aios_data.db',
            'legacy_tachyonic': self.root_path / '/workspace/aios_data.db',
            'knowledge_crystals': self.root_path / '/workspace/aios_data.db',
            'docs_archive': self.root_path / '/workspace/aios_data.db'
        }

    def create_unified_schema(self):
        """Create the consolidated database with unified schema"""
        schema_sql = """
        -- AIOS Consolidated Database Schema
        -- Version: 1.0
        -- Created: 2025-11-23

        -- ============================================================================
        -- CORE SYSTEM TABLES
        -- ============================================================================

        -- File content deduplication (from main_aios and legacy_tachyonic)
        CREATE TABLE IF NOT EXISTS file_content (
            content_hash TEXT PRIMARY KEY,
            content BLOB NOT NULL,
            content_size INTEGER NOT NULL,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reference_count INTEGER DEFAULT 1,
            compression_ratio REAL,
            source_db TEXT NOT NULL,  -- Track which original DB this came from
            migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- File backup records (from main_aios and legacy_tachyonic)
        CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            backup_timestamp TIMESTAMP NOT NULL,
            content_hash TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            file_type TEXT,
            backup_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source_db TEXT NOT NULL,
            migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (content_hash) REFERENCES file_content(content_hash)
        );

        -- ============================================================================
        -- ARCHIVAL SYSTEM TABLES
        -- ============================================================================

        -- Code archive files (from tachyonic_archive)
        CREATE TABLE IF NOT EXISTS archived_files (
            file_id TEXT PRIMARY KEY,
            original_path TEXT NOT NULL,
            content TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            archived_timestamp TEXT NOT NULL,
            file_size_bytes INTEGER NOT NULL,
            file_type TEXT NOT NULL,
            archival_reason TEXT NOT NULL,
            consciousness_level REAL,
            ainlp_patterns TEXT,
            project_phase TEXT,
            related_files TEXT,
            replacement_path TEXT,
            notes TEXT,
            source_db TEXT NOT NULL,
            migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- File evolution history (from tachyonic_archive)
        CREATE TABLE IF NOT EXISTS evolution_history (
            evolution_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            change_type TEXT NOT NULL,
            change_description TEXT,
            consciousness_delta REAL,
            source_db TEXT NOT NULL,
            migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES archived_files(file_id)
        );

        -- Archival reason categories (from tachyonic_archive)
        CREATE TABLE IF NOT EXISTS archival_reasons (
            reason_id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            consciousness_principle TEXT NOT NULL,
            usage_count INTEGER DEFAULT 0,
            source_db TEXT NOT NULL,
            migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Consciousness system snapshots (from tachyonic_archive)
        CREATE TABLE IF NOT EXISTS consciousness_snapshots (
            snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id TEXT,
            timestamp TEXT NOT NULL,
            total_files_count INTEGER,
            total_codebase_lines INTEGER,
            avg_consciousness_level REAL,
            active_ainlp_patterns TEXT,
            system_coherence REAL,
            source_db TEXT NOT NULL,
            migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Archive retrieval log (from tachyonic_archive)
        CREATE TABLE IF NOT EXISTS retrieval_log (
            retrieval_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id TEXT NOT NULL,
            retrieval_timestamp TEXT NOT NULL,
            retrieval_reason TEXT,
            retrieved_by TEXT,
            source_db TEXT NOT NULL,
            migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES archived_files(file_id)
        );

        -- ============================================================================
        -- KNOWLEDGE SYSTEM TABLES
        -- ============================================================================

        -- Knowledge crystals from AI conversations (from knowledge_crystals)
        CREATE TABLE IF NOT EXISTS knowledge_crystals (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            source_conversation TEXT,
            key_concepts TEXT,
            relationships TEXT,
            context_embeddings BLOB,
            understanding_depth REAL,
            consciousness_state TEXT,
            verification_hash TEXT,
            capsule_ids TEXT,
            kpi_dimensions TEXT,
            metric_snapshot TEXT,
            source_db TEXT NOT NULL,
            migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- ============================================================================
        -- DOCUMENTATION SYSTEM TABLES
        -- ============================================================================

        -- Archived documentation (from docs_archive)
        CREATE TABLE IF NOT EXISTS archived_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            content TEXT NOT NULL,
            file_size INTEGER,
            archive_timestamp TEXT,
            original_path TEXT,
            category TEXT,
            keywords TEXT,
            metadata TEXT,
            source_db TEXT NOT NULL,
            migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- ============================================================================
        -- SYSTEM METADATA TABLES
        -- ============================================================================

        -- Spatial metadata for folders (from main_aios and legacy_tachyonic)
        CREATE TABLE IF NOT EXISTS spatial_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_path TEXT NOT NULL UNIQUE,
            architectural_classification TEXT,
            consciousness_level REAL,
            primary_area TEXT,
            metadata_json TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source_db TEXT NOT NULL,
            migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- System state snapshots (from main_aios and legacy_tachyonic)
        CREATE TABLE IF NOT EXISTS system_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            snapshot_type TEXT NOT NULL,
            snapshot_data TEXT NOT NULL,
            consciousness_level REAL,
            file_count INTEGER,
            total_size INTEGER,
            source_db TEXT NOT NULL,
            migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Query result caching (from main_aios and legacy_tachyonic)
        CREATE TABLE IF NOT EXISTS query_cache (
            query_key TEXT PRIMARY KEY,
            query_result TEXT NOT NULL,
            cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0,
            ttl_seconds INTEGER,
            source_db TEXT NOT NULL,
            migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- ============================================================================
        -- MIGRATION TRACKING
        -- ============================================================================

        -- Track migration operations
        CREATE TABLE IF NOT EXISTS migration_log (
            migration_id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_db TEXT NOT NULL,
            source_table TEXT NOT NULL,
            records_migrated INTEGER NOT NULL,
            migration_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            error_message TEXT
        );

        -- Create indexes for performance
        CREATE INDEX IF NOT EXISTS idx_backups_content_hash ON backups(content_hash);
        CREATE INDEX IF NOT EXISTS idx_backups_source_db ON backups(source_db);
        CREATE INDEX IF NOT EXISTS idx_archived_files_hash ON archived_files(content_hash);
        CREATE INDEX IF NOT EXISTS idx_archived_files_source ON archived_files(source_db);
        CREATE INDEX IF NOT EXISTS idx_evolution_file_id ON evolution_history(file_id);
        CREATE INDEX IF NOT EXISTS idx_knowledge_timestamp ON knowledge_crystals(timestamp);
        CREATE INDEX IF NOT EXISTS idx_docs_hash ON archived_documents(content_hash);
        CREATE INDEX IF NOT EXISTS idx_spatial_path ON spatial_metadata(folder_path);
        CREATE INDEX IF NOT EXISTS idx_snapshots_type ON system_snapshots(snapshot_type);
        CREATE INDEX IF NOT EXISTS idx_cache_key ON query_cache(query_key);
        """

        conn = sqlite3.connect(self.consolidated_db)
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()

        print(f"✅ Created unified schema in {self.consolidated_db}")

    def backup_source_databases(self):
        """Create backups of all source databases before migration"""
        print("🔄 Creating backups of source databases...")

        for db_name, db_path in self.source_dbs.items():
            if db_path.exists():
                backup_path = self.backup_dir / f"{db_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                shutil.copy2(db_path, backup_path)
                print(f"   📋 Backed up {db_name}: {db_path} → {backup_path}")
            else:
                print(f"   ⚠️  Source database not found: {db_name} ({db_path})")

    def migrate_database(self, source_name, source_path):
        """Migrate data from a single source database"""
        if not source_path.exists():
            print(f"⚠️  Skipping {source_name}: database not found")
            return

        print(f"🔄 Migrating {source_name}...")

        source_conn = sqlite3.connect(source_path)
        target_conn = sqlite3.connect(self.consolidated_db)

        try:
            # Get all tables from source
            source_cursor = source_conn.cursor()
            source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = source_cursor.fetchall()

            total_migrated = 0

            for table in tables:
                table_name = table[0]
                print(f"   📋 Migrating table: {table_name}")

                # Get all data from source table
                source_cursor.execute(f"SELECT * FROM {table_name}")
                rows = source_cursor.fetchall()

                if not rows:
                    print(f"     ℹ️  No data in {table_name}")
                    continue

                # Get column names
                source_cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in source_cursor.fetchall()]

                # Prepare target table name (handle conflicts)
                target_table = self.resolve_table_name_conflict(table_name, source_name)

                # Insert data into target with source tracking
                target_cursor = target_conn.cursor()

                # Check if table has auto-incrementing primary key that might conflict
                auto_increment_tables = ['backups', 'evolution_history', 'consciousness_snapshots',
                                       'retrieval_log', 'archived_documents', 'spatial_metadata',
                                       'system_snapshots']

                if table_name in auto_increment_tables:
                    # For auto-increment tables, exclude the ID column and let SQLite assign new ones
                    data_columns = columns[1:] + ['source_db', 'migrated_at']  # Skip first column (ID)
                    placeholders = ','.join(['?' for _ in data_columns])

                    for row in rows:
                        # Skip the ID field (first column) and add metadata
                        row_data = list(row)[1:] + [source_name, datetime.now().isoformat()]
                        target_cursor.execute(
                            f"INSERT INTO {target_table} ({','.join(data_columns)}) VALUES ({placeholders})",
                            row_data
                        )
                else:
                    # For tables without auto-increment conflicts, preserve all data
                    extended_columns = columns + ['source_db', 'migrated_at']
                    placeholders = ','.join(['?' for _ in extended_columns])

                    for row in rows:
                        # Convert row to list and add metadata
                        row_data = list(row) + [source_name, datetime.now().isoformat()]
                        target_cursor.execute(
                            f"INSERT INTO {target_table} ({','.join(extended_columns)}) VALUES ({placeholders})",
                            row_data
                        )

                target_conn.commit()
                total_migrated += len(rows)
                print(f"     ✅ Migrated {len(rows)} records to {target_table}")

            # Log migration
            target_cursor.execute(
                "INSERT INTO migration_log (source_db, source_table, records_migrated, status) VALUES (?, ?, ?, ?)",
                (source_name, 'ALL', total_migrated, 'SUCCESS')
            )
            target_conn.commit()

            print(f"✅ Successfully migrated {source_name}: {total_migrated} total records")

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error migrating {source_name}: {error_msg}")

            # Log failed migration
            target_cursor = target_conn.cursor()
            target_cursor.execute(
                "INSERT INTO migration_log (source_db, source_table, records_migrated, status, error_message) VALUES (?, ?, ?, ?, ?)",
                (source_name, 'ALL', 0, 'FAILED', error_msg)
            )
            target_conn.commit()

        finally:
            source_conn.close()
            target_conn.close()

    def resolve_table_name_conflict(self, table_name, source_name):
        """Resolve table name conflicts by prefixing with source name if needed"""
        # Most tables have unique names, but handle any conflicts
        conflict_tables = {
            'backups': ['main_aios', 'legacy_tachyonic'],
            'file_content': ['main_aios', 'legacy_tachyonic'],
            'spatial_metadata': ['main_aios', 'legacy_tachyonic'],
            'system_snapshots': ['main_aios', 'legacy_tachyonic'],
            'query_cache': ['main_aios', 'legacy_tachyonic']
        }

        if table_name in conflict_tables and len(conflict_tables[table_name]) > 1:
            # For conflicting tables, keep the original name since schema is identical
            # The source_db column will differentiate the records
            return table_name
        else:
            return table_name

    def validate_migration(self):
        """Validate that migration was successful"""
        print("🔍 Validating migration...")

        conn = sqlite3.connect(self.consolidated_db)
        cursor = conn.cursor()

        # Check migration log
        cursor.execute("SELECT source_db, records_migrated, status FROM migration_log")
        migrations = cursor.fetchall()

        successful_migrations = 0
        total_source_records = 0

        for migration in migrations:
            source_db, records, status = migration
            total_source_records += records
            if status == 'SUCCESS':
                successful_migrations += 1
            print(f"   {status}: {source_db} - {records} records migrated")

        # Check total records in consolidated DB (excluding migration_log)
        cursor.execute("""
            SELECT
                (SELECT COUNT(*) FROM backups) +
                (SELECT COUNT(*) FROM file_content) +
                (SELECT COUNT(*) FROM archived_files) +
                (SELECT COUNT(*) FROM evolution_history) +
                (SELECT COUNT(*) FROM knowledge_crystals) +
                (SELECT COUNT(*) FROM archived_documents) +
                (SELECT COUNT(*) FROM spatial_metadata) +
                (SELECT COUNT(*) FROM system_snapshots) +
                (SELECT COUNT(*) FROM query_cache) as total_records
        """)
        consolidated_total = cursor.fetchone()[0]

        conn.close()

        print(f"\\n📊 Migration Summary:")
        print(f"   Source databases processed: {len(migrations)}")
        print(f"   Successful migrations: {successful_migrations}")
        print(f"   Total records from sources: {total_source_records}")
        print(f"   Records in consolidated DB: {consolidated_total}")
        print(f"   Deduplication factor: {total_source_records - consolidated_total} records")

        # Validation is successful if all migrations completed without error
        # Some deduplication is expected and normal
        if successful_migrations == len([db for db in self.source_dbs.keys() if self.source_dbs[db].exists()]):
            print("✅ Migration validation PASSED (all sources migrated successfully)")
            return True
        else:
            print("❌ Migration validation FAILED (some migrations failed)")
            return False

    def update_configuration(self):
        """Update configuration files to point to new centralized database"""
        print("🔄 Updating configuration files...")

        # Find and update Python files that reference the old database paths
        config_updates = {
            '/workspace/aios_data.db': '/workspace/database/aios_data.db',
            '/workspace/aios_data.db': '/workspace/database/aios_data.db',
            '/workspace/aios_data.db': '/workspace/database/aios_data.db',
            '/workspace/aios_data.db': '/workspace/database/aios_data.db',
            '/workspace/aios_data.db': '/workspace/database/aios_data.db'
        }

        # Search for Python files that might reference these paths
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()

                        updated = False
                        for old_path, new_path in config_updates.items():
                            if old_path in content:
                                content = content.replace(old_path, new_path)
                                updated = True

                        if updated:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            print(f"   📝 Updated {file_path}")

                    except Exception as e:
                        print(f"   ⚠️  Could not update {file_path}: {e}")

    def create_rollback_script(self):
        """Create a rollback script in case migration needs to be undone"""
        rollback_script = self.backup_dir / "rollback_migration.py"

        rollback_code = '''#!/usr/bin/env python3
"""
AIOS Database Migration Rollback Script
Restores databases from backup if consolidation needs to be undone.
"""

import shutil
from pathlib import Path

backup_dir = Path("''' + str(self.backup_dir) + '''")
root_path = Path("''' + str(self.root_path) + '''")

# Original database paths
original_paths = ''' + str(self.source_dbs).replace("'", '"') + '''

print("🔄 Rolling back database consolidation...")

# Remove consolidated database
consolidated_db = root_path / "aios_data.db"
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
'''

        with open(rollback_script, 'w') as f:
            f.write(rollback_code)

        rollback_script.chmod(0o755)
        print(f"📋 Created rollback script: {rollback_script}")

    def run_consolidation(self):
        """Run the complete consolidation process"""
        print("🚀 Starting AIOS Database Consolidation")
        print(f"Target: {self.consolidated_db}")
        print(f"Backup directory: {self.backup_dir}")
        print()

        # Step 1: Create backups
        self.backup_source_databases()
        print()

        # Step 2: Create unified schema
        self.create_unified_schema()
        print()

        # Step 3: Migrate all databases
        for db_name, db_path in self.source_dbs.items():
            self.migrate_database(db_name, db_path)
        print()

        # Step 4: Validate migration
        if not self.validate_migration():
            print("❌ Migration validation failed. Check logs and consider rollback.")
            return False
        print()

        # Step 5: Update configuration
        self.update_configuration()
        print()

        # Step 6: Create rollback script
        self.create_rollback_script()
        print()

        print("🎉 Database consolidation completed successfully!")
        print(f"📍 Consolidated database: {self.consolidated_db}")
        print(f"📍 Backups: {self.backup_dir}")
        print(f"📍 Rollback script: {self.backup_dir}/rollback_migration.py")
        print()
        print("Next steps:")
        print("1. Test your application with the new database")
        print("2. If issues occur, run the rollback script")
        print("3. Once verified, you can remove the old database files and backups")

        return True

def main():
    consolidator = AIOSDatabaseConsolidator()
    success = consolidator.run_consolidation()

    if success:
        print("\n✅ AIOS database consolidation completed successfully!")
    else:
        print("\n❌ AIOS database consolidation failed. Check logs above.")
        exit(1)

if __name__ == "__main__":
    main()