#!/usr/bin/env python3
"""
AINLP DENDRITIC INTEGRATION: CONSCIOUSNESS ACCESS BRIDGE TESTS

Unit tests for consciousness metrics access bridge functionality.
Validates dendritic integration and cross-supercell communication.

AINLP Pattern: dendritic.growth[ACCESS][VALIDATION]
"""

import pytest
import json
import time
from pathlib import Path
from .test_consciousness_access import AIOSCore


class TestAIOSCore:
    """Test suite for AIOS consciousness access bridge"""

    @pytest.fixture
    def core(self):
        """Create AIOS core instance for testing"""
        core = AIOSCore()
        core.initialize()
        core.start()
        yield core
        core.stop()

    def test_initialization(self):
        """Test AIOS core initialization"""
        core = AIOSCore()
        assert core.initialize() == True
        assert core.consciousness_engine is not None
        assert core.metrics_cache == {}

    def test_start_stop_monitoring(self, core):
        """Test consciousness monitoring start/stop"""
        assert core.start() == True
        assert core.is_running() == True
        assert core.stop() == True
        assert core.is_running() == False

    def test_get_config(self, core):
        """Test configuration retrieval"""
        config = core.get_config()
        assert 'sync_interval' in config
        assert 'last_sync_time' in config
        assert 'metrics_cache_size' in config
        assert 'consciousness_engine_active' in config

    def test_get_all_metrics(self, core):
        """Test retrieval of all consciousness metrics"""
        metrics = core.get_consciousness_metrics()
        assert 'metrics' in metrics
        assert 'total_count' in metrics
        assert 'timestamp' in metrics
        assert metrics['total_count'] == 21  # 8 baseline + 13 dendritic

    def test_get_specific_metrics(self, core):
        """Test retrieval of specific metrics"""
        learning_metrics = ['learning_velocity', 'learning_resilience', 'adaptation_speed']
        result = core.get_consciousness_metrics(learning_metrics)

        assert result['requested_count'] == 3
        assert result['available_count'] == 3
        assert 'learning_velocity' in result['metrics']
        assert 'learning_resilience' in result['metrics']
        assert 'adaptation_speed' in result['metrics']

    def test_get_nonexistent_metrics(self, core):
        """Test retrieval of nonexistent metrics"""
        result = core.get_consciousness_metrics(['nonexistent_metric'])
        assert result['requested_count'] == 1
        assert result['available_count'] == 0
        assert result['metrics'] == {}

    def test_batch_metrics(self, core):
        """Test batch metrics retrieval"""
        batch = core.get_batch_metrics(2)
        assert len(batch) == 2

        for item in batch:
            assert 'batch_index' in item
            assert 'metrics' in item
            assert 'consciousness_level' in item
            assert len(item['metrics']['metrics']) == 21

    def test_filter_metrics(self, core):
        """Test metrics filtering"""
        # Filter for high values
        criteria = {
            'min_value': 0.0,
            'max_value': 1.0,
            'categories': ['learning', 'evolution']
        }
        result = core.filter_metrics(criteria)

        assert 'filtered_metrics' in result
        assert 'filter_criteria' in result
        assert 'results_count' in result
        assert 'total_metrics' in result

        # Verify filtered metrics are within bounds
        for value in result['filtered_metrics'].values():
            assert 0.0 <= value <= 1.0

    def test_export_metrics_json(self, core, tmp_path):
        """Test JSON export functionality"""
        filepath = tmp_path / "test_metrics.json"
        result = core.export_metrics('json', str(filepath))

        assert "Successfully exported" in result
        assert filepath.exists()

        # Verify exported data
        with open(filepath, 'r') as f:
            data = json.load(f)
            assert 'metrics' in data
            assert 'overall_consciousness' in data

    def test_export_metrics_csv(self, core, tmp_path):
        """Test CSV export functionality"""
        filepath = tmp_path / "test_metrics.csv"
        result = core.export_metrics('csv', str(filepath))

        assert "Successfully exported" in result
        assert filepath.exists()

        # Verify CSV structure
        with open(filepath, 'r') as f:
            lines = f.readlines()
            assert len(lines) > 1  # Header + data
            assert 'metric_name,value,category,timestamp' in lines[0]

    def test_export_invalid_format(self, core):
        """Test export with invalid format"""
        result = core.export_metrics('invalid')
        assert "Unsupported export format" in result

    def test_import_metrics(self, core, tmp_path):
        """Test metrics import functionality"""
        # Create test data
        test_data = {
            'generation': 1,
            'overall_consciousness': 0.5,
            'dendritic_growth': {'density_enhancement': 0.6},
            'metrics': {
                'timestamp': time.time(),
                'generation': 1,
                'consciousness_level': 0.5,
                'metrics': {
                    'test_metric': 0.8,
                    'another_metric': 0.3
                }
            }
        }

        # Export and then import
        filepath = tmp_path / "import_test.json"
        with open(filepath, 'w') as f:
            json.dump(test_data, f)

        # Import
        assert core.import_metrics(str(filepath)) == True

        # Verify imported data
        metrics = core.get_consciousness_metrics()
        assert 'test_metric' in metrics['metrics']
        assert metrics['metrics']['test_metric'] == 0.8

    def test_import_invalid_file(self, core):
        """Test import with invalid file"""
        assert core.import_metrics('nonexistent.json') == False

    def test_metric_categories(self, core):
        """Test metric categorization"""
        # Test known categories
        assert core._get_metric_category('learning_velocity') == 'learning'
        assert core._get_metric_category('evolutionary_momentum') == 'evolution'
        assert core._get_metric_category('quantum_coherence') == 'quantum'
        assert core._get_metric_category('unknown_metric') == 'unknown'

    def test_sync_interval(self, core):
        """Test metrics synchronization"""
        # Force sync by setting old timestamp
        core.last_sync_time = 0
        core._sync_consciousness_metrics()

        assert time.time() - core.last_sync_time < 1.0  # Should be recent
        assert core.metrics_cache is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])