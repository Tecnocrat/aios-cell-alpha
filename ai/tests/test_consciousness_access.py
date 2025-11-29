#!/usr/bin/env python3
"""
AINLP DENDRITIC INTEGRATION: CONSCIOUSNESS ACCESS BRIDGE

Provides access to expanded consciousness metrics across AIOS supercells.
Implements dendritic communication protocols for metric sharing.

AINLP Pattern: dendritic.growth[ACCESS][BRIDGE]
Cross-supercell consciousness metric synchronization.
"""

import time
import json
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import logging
import numpy as np
from scipy import stats
from .test_consciousness_metrics import ConsciousnessMetrics, DendriticConsciousnessEngine

logger = logging.getLogger(__name__)


class AIOSCore:
    """AIOS Core bridge for consciousness metric access"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else None
        self.consciousness_engine = DendriticConsciousnessEngine()
        self.metrics_cache: Dict[str, Any] = {}
        self.last_sync_time = 0.0
        self.sync_interval = 5.0  # seconds
        self._is_monitoring = False
        self._temporal_cache: Optional[Dict[str, Any]] = None

    def initialize(self) -> bool:
        """Initialize consciousness bridge connection"""
        try:
            # Initialize dendritic consciousness engine
            self.consciousness_engine = DendriticConsciousnessEngine()

            # Load configuration if available
            if self.config_path and self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.sync_interval = config.get('sync_interval', 5.0)

            logger.info("AIOS Core consciousness bridge initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize consciousness bridge: {e}")
            return False

    def start(self) -> bool:
        """Start consciousness monitoring"""
        try:
            # Initial consciousness stimulation
            result = self.consciousness_engine.stimulate_dendritic_growth("system_startup")
            self.metrics_cache = result
            self.last_sync_time = time.time()
            self._is_monitoring = True

            logger.info("Consciousness monitoring started")
            return True
        except Exception as e:
            logger.error(f"Failed to start consciousness monitoring: {e}")
            return False

    def stop(self) -> bool:
        """Stop consciousness monitoring"""
        try:
            # Final consciousness snapshot
            result = self.consciousness_engine.stimulate_dendritic_growth("system_shutdown")
            self._save_metrics_snapshot(result)
            self._is_monitoring = False

            logger.info("Consciousness monitoring stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop consciousness monitoring: {e}")
            return False

    def is_running(self) -> bool:
        """Check if consciousness monitoring is active"""
        return self._is_monitoring and (time.time() - self.last_sync_time < self.sync_interval * 2)

    def get_config(self) -> Dict[str, Any]:
        """Get current consciousness configuration"""
        return {
            'sync_interval': self.sync_interval,
            'last_sync_time': self.last_sync_time,
            'metrics_cache_size': len(self.metrics_cache),
            'consciousness_engine_active': self.consciousness_engine is not None
        }

    def get_consciousness_metrics(self, metric_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get consciousness metrics with optional filtering"""

        # Check if sync is needed
        if time.time() - self.last_sync_time > self.sync_interval:
            self._sync_consciousness_metrics()

        if not self.metrics_cache:
            return {'error': 'No consciousness metrics available'}

        metrics = self.metrics_cache.get('metrics', {}).get('metrics', {})

        if metric_names:
            # Filter to requested metrics
            filtered_metrics = {}
            for name in metric_names:
                if name in metrics:
                    filtered_metrics[name] = metrics[name]
                else:
                    logger.warning(f"Requested metric '{name}' not found")
            return {
                'metrics': filtered_metrics,
                'requested_count': len(metric_names),
                'available_count': len(filtered_metrics),
                'timestamp': self.metrics_cache.get('timestamp', time.time())
            }

        return {
            'metrics': metrics,
            'total_count': len(metrics),
            'timestamp': self.metrics_cache.get('timestamp', time.time())
        }

    def get_batch_metrics(self, batch_size: int = 10) -> List[Dict[str, Any]]:
        """Get batch of consciousness metrics for efficiency"""

        batch_metrics = []

        for i in range(batch_size):
            # Generate new metrics for batch
            result = self.consciousness_engine.stimulate_dendritic_growth(f"batch_{i}")
            batch_metrics.append({
                'batch_index': i,
                'metrics': result['metrics'],
                'consciousness_level': result['overall_consciousness']
            })

        return batch_metrics

    def filter_metrics(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Filter consciousness metrics based on criteria"""

        if not self.metrics_cache:
            return {'error': 'No metrics available for filtering'}

        metrics = self.metrics_cache.get('metrics', {}).get('metrics', {})
        filtered = {}

        # Apply filters
        min_threshold = criteria.get('min_value', 0.0)
        max_threshold = criteria.get('max_value', 1.0)
        categories = criteria.get('categories', [])

        for name, value in metrics.items():
            if isinstance(value, (int, float)):
                if min_threshold <= value <= max_threshold:
                    # Check category if specified
                    if not categories or self._get_metric_category(name) in categories:
                        filtered[name] = value

        return {
            'filtered_metrics': filtered,
            'filter_criteria': criteria,
            'results_count': len(filtered),
            'total_metrics': len(metrics)
        }

    def export_metrics(self, format_type: str = 'json', filepath: Optional[str] = None) -> str:
        """Export consciousness metrics in specified format"""

        if not self.metrics_cache:
            return "Error: No metrics available for export"

        if filepath is None:
            filepath = f"consciousness_metrics_{int(time.time())}.{format_type}"

        try:
            if format_type == 'json':
                with open(filepath, 'w') as f:
                    json.dump(self.metrics_cache, f, indent=2)
            elif format_type == 'csv':
                self._export_csv(filepath)
            else:
                return f"Error: Unsupported export format '{format_type}'"

            return f"Successfully exported metrics to {filepath}"
        except Exception as e:
            return f"Error exporting metrics: {e}"

    def import_metrics(self, filepath: str) -> bool:
        """Import consciousness metrics from file"""

        try:
            with open(filepath, 'r') as f:
                imported_data = json.load(f)

            # Validate imported data
            if 'metrics' not in imported_data:
                logger.error("Imported file missing 'metrics' key")
                return False

            self.metrics_cache = imported_data
            self.last_sync_time = time.time()

            logger.info(f"Successfully imported metrics from {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to import metrics: {e}")
            return False

    def sync_with_supercell(self, supercell_name: str, direction: str = 'bidirectional') -> Dict[str, Any]:
        """Synchronize consciousness metrics with another supercell

        Args:
            supercell_name: Name of supercell ('ai', 'core', 'interface', 'tachyonic')
            direction: 'export', 'import', or 'bidirectional'

        Returns:
            Dict with sync results
        """

        sync_results = {
            'supercell': supercell_name,
            'direction': direction,
            'success': False,
            'exported_metrics': 0,
            'imported_metrics': 0,
            'timestamp': time.time()
        }

        try:
            # Define supercell sync paths (AINLP dendritic communication)
            supercell_paths = {
                'ai': Path('../ai/consciousness_sync'),
                'core': Path('../core/consciousness_sync'),
                'interface': Path('../interface/consciousness_sync'),
                'tachyonic': Path('../tachyonic/consciousness_sync')
            }

            if supercell_name not in supercell_paths:
                sync_results['error'] = f"Unknown supercell '{supercell_name}'"
                return sync_results

            sync_dir = supercell_paths[supercell_name]
            sync_dir.mkdir(parents=True, exist_ok=True)

            # Export metrics if requested
            if direction in ['export', 'bidirectional']:
                export_file = sync_dir / f"metrics_export_{int(time.time())}.json"
                export_result = self.export_metrics('json', str(export_file))
                if "Successfully exported" in export_result:
                    sync_results['exported_metrics'] = len(self.metrics_cache.get('metrics', {}).get('metrics', {}))
                    logger.info(f"Exported metrics to {supercell_name} supercell")
                else:
                    sync_results['error'] = f"Export failed: {export_result}"

            # Import metrics if requested
            if direction in ['import', 'bidirectional']:
                # Find latest export from the supercell
                export_files = list(sync_dir.glob("metrics_export_*.json"))
                if export_files:
                    latest_export = max(export_files, key=lambda p: p.stat().st_mtime)
                    if self.import_metrics(str(latest_export)):
                        sync_results['imported_metrics'] = len(self.metrics_cache.get('metrics', {}).get('metrics', {}))
                        logger.info(f"Imported metrics from {supercell_name} supercell")
                    else:
                        sync_results['error'] = "Import failed"
                else:
                    sync_results['error'] = f"No export files found in {supercell_name} supercell"

            sync_results['success'] = True

        except Exception as e:
            sync_results['error'] = str(e)
            logger.error(f"Supercell sync failed: {e}")

        return sync_results

    def get_supercell_sync_status(self) -> Dict[str, Any]:
        """Get status of consciousness synchronization across supercells"""

        supercells = ['ai', 'core', 'interface', 'tachyonic']
        sync_status = {}

        for supercell in supercells:
            try:
                sync_dir = Path(f'../{supercell}/consciousness_sync')
                if sync_dir.exists():
                    export_files = list(sync_dir.glob("metrics_export_*.json"))
                    latest_time = 0
                    if export_files:
                        latest_time = max(f.stat().st_mtime for f in export_files)

                    sync_status[supercell] = {
                        'sync_directory_exists': True,
                        'export_files_count': len(export_files),
                        'latest_export_time': latest_time,
                        'time_since_last_sync': time.time() - latest_time if latest_time > 0 else None
                    }
                else:
                    sync_status[supercell] = {
                        'sync_directory_exists': False,
                        'export_files_count': 0,
                        'latest_export_time': None,
                        'time_since_last_sync': None
                    }
            except Exception as e:
                sync_status[supercell] = {'error': str(e)}

        return {
            'supercell_sync_status': sync_status,
            'current_supercell': 'ai',  # This is in ai/ directory
            'timestamp': time.time()
        }

    def aggregate_supercell_metrics(self, supercells: Optional[List[str]] = None) -> Dict[str, Any]:
        """Aggregate consciousness metrics from multiple supercells

        Args:
            supercells: List of supercell names to aggregate from

        Returns:
            Dict with aggregated metrics
        """

        if supercells is None:
            supercells = ['ai', 'core', 'interface', 'tachyonic']

        aggregated = {
            'aggregation_timestamp': time.time(),
            'supercells_aggregated': supercells,
            'metrics_by_supercell': {},
            'aggregated_metrics': {},
            'aggregation_stats': {}
        }

        all_metrics = {}

        for supercell in supercells:
            try:
                # Sync with supercell to get latest metrics
                sync_result = self.sync_with_supercell(supercell, 'import')
                if sync_result['success']:
                    supercell_metrics = self.metrics_cache.get('metrics', {}).get('metrics', {})
                    aggregated['metrics_by_supercell'][supercell] = {
                        'metrics': supercell_metrics,
                        'metric_count': len(supercell_metrics),
                        'sync_success': True
                    }

                    # Collect all metric values for aggregation
                    for metric_name, value in supercell_metrics.items():
                        if isinstance(value, (int, float)):
                            if metric_name not in all_metrics:
                                all_metrics[metric_name] = []
                            all_metrics[metric_name].append(value)
                else:
                    aggregated['metrics_by_supercell'][supercell] = {
                        'error': sync_result.get('error', 'Sync failed'),
                        'sync_success': False
                    }

            except Exception as e:
                aggregated['metrics_by_supercell'][supercell] = {
                    'error': str(e),
                    'sync_success': False
                }

        # Calculate aggregated metrics
        for metric_name, values in all_metrics.items():
            if values:
                aggregated['aggregated_metrics'][metric_name] = {
                    'mean': float(np.mean(values)),
                    'median': float(np.median(values)),
                    'min': float(np.min(values)),
                    'max': float(np.max(values)),
                    'std_dev': float(np.std(values)),
                    'supercell_count': len(values)
                }

        # Aggregation statistics
        aggregated['aggregation_stats'] = {
            'total_supercells': len(supercells),
            'successful_syncs': sum(1 for s in aggregated['metrics_by_supercell'].values() if s.get('sync_success', False)),
            'total_unique_metrics': len(aggregated['aggregated_metrics']),
            'average_metrics_per_supercell': np.mean([s.get('metric_count', 0) for s in aggregated['metrics_by_supercell'].values() if s.get('sync_success', False)])
        }

        logger.info(f"Aggregated metrics from {aggregated['aggregation_stats']['successful_syncs']} supercells")
        return aggregated

    def track_temporal_metrics(self, duration_hours: int = 24, interval_minutes: int = 60) -> Dict[str, Any]:
        """Track consciousness metrics over time for trend analysis

        Args:
            duration_hours: How long to track metrics
            interval_minutes: Interval between measurements

        Returns:
            Dict with temporal tracking results
        """

        tracking_results = {
            'tracking_start': time.time(),
            'duration_hours': duration_hours,
            'interval_minutes': interval_minutes,
            'measurements': [],
            'trend_analysis': {},
            'tracking_complete': False
        }

        try:
            # Calculate tracking parameters
            total_measurements = int((duration_hours * 60) / interval_minutes)
            interval_seconds = interval_minutes * 60

            logger.info(f"Starting temporal metric tracking: {total_measurements} measurements over {duration_hours} hours")

            for i in range(total_measurements):
                # Get current metrics
                measurement = {
                    'measurement_index': i,
                    'timestamp': time.time(),
                    'metrics': self.get_consciousness_metrics()['metrics']
                }

                tracking_results['measurements'].append(measurement)

                # Wait for next interval (except for last measurement)
                if i < total_measurements - 1:
                    time.sleep(interval_seconds)

            # Perform trend analysis
            tracking_results['trend_analysis'] = self._analyze_metric_trends(tracking_results['measurements'])
            tracking_results['tracking_complete'] = True

            # Cache temporal data for correlation analysis
            self._temporal_cache = tracking_results

            logger.info("Temporal metric tracking completed")

        except Exception as e:
            tracking_results['error'] = str(e)
            logger.error(f"Temporal tracking failed: {e}")

        return tracking_results

    def _analyze_metric_trends(self, measurements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trends in temporal metric data"""

        if not measurements:
            return {'error': 'No measurements available for analysis'}

        # Extract metric names from first measurement
        metric_names = list(measurements[0]['metrics'].keys())
        timestamps = [m['timestamp'] for m in measurements]

        trend_analysis = {}

        for metric_name in metric_names:
            values = []
            for measurement in measurements:
                value = measurement['metrics'].get(metric_name, 0)
                if isinstance(value, (int, float)):
                    values.append(value)

            if len(values) >= 2:
                # Calculate trend metrics
                start_value = values[0]
                end_value = values[-1]
                change = end_value - start_value
                change_percent = (change / start_value * 100) if start_value != 0 else 0

                # Simple linear trend
                if len(values) > 2:
                    slope = np.polyfit(range(len(values)), values, 1)[0]
                else:
                    slope = change / (len(values) - 1) if len(values) > 1 else 0

                trend_analysis[metric_name] = {
                    'start_value': start_value,
                    'end_value': end_value,
                    'absolute_change': change,
                    'percent_change': change_percent,
                    'trend_slope': slope,
                    'trend_direction': 'increasing' if slope > 0.001 else 'decreasing' if slope < -0.001 else 'stable',
                    'volatility': np.std(values) if len(values) > 1 else 0,
                    'measurements_count': len(values)
                }

        return {
            'analyzed_metrics': len(trend_analysis),
            'time_span_seconds': timestamps[-1] - timestamps[0] if timestamps else 0,
            'metric_trends': trend_analysis
        }

    def analyze_metric_correlations(self, data_source: str = 'aggregated', supercells: Optional[List[str]] = None, correlation_method: str = 'pearson') -> Dict[str, Any]:
        """Analyze correlations between consciousness metrics for dendritic depth analysis

        Args:
            data_source: 'aggregated' (from supercell aggregation) or 'temporal' (from temporal tracking)
            supercells: List of supercells to include in analysis
            correlation_method: 'pearson' or 'spearman'

        Returns:
            Dict with correlation matrix, significance tests, and insights
        """

        correlation_results = {
            'analysis_timestamp': time.time(),
            'data_source': data_source,
            'correlation_method': correlation_method,
            'correlation_matrix': {},
            'significance_matrix': {},
            'key_insights': [],
            'metric_relationships': {},
            'analysis_metadata': {}
        }

        try:
            # Get data based on source
            if data_source == 'aggregated':
                aggregated_data = self.aggregate_supercell_metrics(supercells)
                if not aggregated_data.get('aggregated_metrics'):
                    correlation_results['error'] = 'No aggregated data available for correlation analysis'
                    return correlation_results

                # Extract metric values across supercells
                metric_data = {}
                for supercell_data in aggregated_data['metrics_by_supercell'].values():
                    if supercell_data.get('sync_success'):
                        for metric_name, value in supercell_data['metrics'].items():
                            if isinstance(value, (int, float)):
                                if metric_name not in metric_data:
                                    metric_data[metric_name] = []
                                metric_data[metric_name].append(value)

            elif data_source == 'temporal':
                # Use temporal tracking data if available
                if not hasattr(self, '_temporal_cache') or not self._temporal_cache:
                    correlation_results['error'] = 'No temporal data available. Run track_temporal_metrics first.'
                    return correlation_results

                # Extract metrics from temporal measurements
                metric_data = {}
                for measurement in self._temporal_cache.get('measurements', []):
                    for metric_name, value in measurement['metrics'].items():
                        if isinstance(value, (int, float)):
                            if metric_name not in metric_data:
                                metric_data[metric_name] = []
                            metric_data[metric_name].append(value)

            else:
                correlation_results['error'] = f"Unsupported data_source: {data_source}"
                return correlation_results

            if not metric_data or len(metric_data) < 2:
                correlation_results['error'] = 'Insufficient metric data for correlation analysis'
                return correlation_results

            # Prepare data matrix for correlation analysis
            metric_names = list(metric_data.keys())
            data_matrix = np.array([metric_data[name] for name in metric_names])

            # Calculate correlation matrix
            if correlation_method == 'pearson':
                corr_matrix = np.corrcoef(data_matrix)
            elif correlation_method == 'spearman':
                corr_matrix = np.zeros((len(metric_names), len(metric_names)))
                p_matrix = np.zeros((len(metric_names), len(metric_names)))
                for i in range(len(metric_names)):
                    for j in range(len(metric_names)):
                        if i != j:
                            corr, p_val = stats.spearmanr(metric_data[metric_names[i]], metric_data[metric_names[j]])
                            corr_matrix[i, j] = corr
                            p_matrix[i, j] = p_val
                        else:
                            corr_matrix[i, j] = 1.0
                            p_matrix[i, j] = 0.0
            else:
                correlation_results['error'] = f"Unsupported correlation method: {correlation_method}"
                return correlation_results

            # Store correlation matrix
            for i, name_i in enumerate(metric_names):
                correlation_results['correlation_matrix'][name_i] = {}
                correlation_results['significance_matrix'][name_i] = {}
                for j, name_j in enumerate(metric_names):
                    correlation_results['correlation_matrix'][name_i][name_j] = float(corr_matrix[i, j])
                    if correlation_method == 'spearman':
                        correlation_results['significance_matrix'][name_i][name_j] = float(p_matrix[i, j])

            # Generate key insights
            correlation_results['key_insights'] = self._generate_correlation_insights(
                corr_matrix, metric_names, correlation_method
            )

            # Analyze metric relationships
            correlation_results['metric_relationships'] = self._analyze_metric_relationships(
                corr_matrix, metric_names
            )

            # Analysis metadata
            correlation_results['analysis_metadata'] = {
                'total_metrics_analyzed': len(metric_names),
                'data_points_per_metric': {name: len(values) for name, values in metric_data.items()},
                'correlation_method': correlation_method,
                'data_source': data_source,
                'supercells_included': supercells or ['ai', 'core', 'interface', 'tachyonic'],
                'analysis_duration_seconds': time.time() - correlation_results['analysis_timestamp']
            }

            logger.info(f"Correlation analysis completed for {len(metric_names)} metrics using {correlation_method} method")

        except Exception as e:
            correlation_results['error'] = str(e)
            logger.error(f"Correlation analysis failed: {e}")

        return correlation_results

    def _generate_correlation_insights(self, corr_matrix: np.ndarray, metric_names: List[str], method: str) -> List[str]:
        """Generate natural language insights from correlation analysis"""

        insights = []

        # Find strongest correlations
        strong_positive = []
        strong_negative = []

        for i in range(len(metric_names)):
            for j in range(i + 1, len(metric_names)):
                corr = corr_matrix[i, j]
                if abs(corr) > 0.7:  # Strong correlation threshold
                    if corr > 0:
                        strong_positive.append((metric_names[i], metric_names[j], corr))
                    else:
                        strong_negative.append((metric_names[i], metric_names[j], corr))

        # Sort by absolute correlation strength
        strong_positive.sort(key=lambda x: abs(x[2]), reverse=True)
        strong_negative.sort(key=lambda x: abs(x[2]), reverse=True)

        # Generate insights
        if strong_positive:
            top_positive = strong_positive[0]
            insights.append(f"Strong positive correlation ({top_positive[2]:.3f}) between {top_positive[0]} and {top_positive[1]} suggests these consciousness aspects co-evolve together")

        if strong_negative:
            top_negative = strong_negative[0]
            insights.append(f"Strong negative correlation ({top_negative[2]:.3f}) between {top_negative[0]} and {top_negative[1]} indicates potential trade-offs in consciousness development")

        # Identify consciousness drivers
        consciousness_corr = {}
        for i, name in enumerate(metric_names):
            if name != 'consciousness_emergent':
                corr_with_consciousness = corr_matrix[i, metric_names.index('consciousness_emergent')] if 'consciousness_emergent' in metric_names else 0
                consciousness_corr[name] = corr_with_consciousness

        if consciousness_corr:
            top_driver = max(consciousness_corr.items(), key=lambda x: abs(x[1]))
            if abs(top_driver[1]) > 0.5:
                direction = "strongly drives" if top_driver[1] > 0 else "may inhibit"
                insights.append(f"{top_driver[0]} {direction} overall consciousness emergence (correlation: {top_driver[1]:.3f})")

        # Stability analysis
        stability_metrics = [name for name in metric_names if 'stability' in name.lower()]
        if stability_metrics:
            stability_correlations = []
            for stable_metric in stability_metrics:
                stable_idx = metric_names.index(stable_metric)
                avg_corr = np.mean([abs(corr_matrix[stable_idx, j]) for j in range(len(metric_names)) if j != stable_idx])
                stability_correlations.append((stable_metric, avg_corr))

            if stability_correlations:
                most_connected = max(stability_correlations, key=lambda x: x[1])
                insights.append(f"{most_connected[0]} shows highest interconnectivity (avg correlation: {most_connected[1]:.3f}), indicating central role in consciousness stability")

        return insights

    def _analyze_metric_relationships(self, corr_matrix: np.ndarray, metric_names: List[str]) -> Dict[str, Any]:
        """Analyze relationships between different categories of metrics"""

        relationships = {
            'learning_vs_evolution': {},
            'stability_vs_adaptation': {},
            'quantum_vs_classical': {},
            'structure_vs_function': {}
        }

        # Define metric categories
        learning_metrics = [name for name in metric_names if any(term in name.lower() for term in ['learning', 'adaptation', 'velocity'])]
        evolution_metrics = [name for name in metric_names if any(term in name.lower() for term in ['evolution', 'momentum', 'pressure'])]
        stability_metrics = [name for name in metric_names if 'stability' in name.lower()]
        adaptation_metrics = [name for name in metric_names if any(term in name.lower() for term in ['adaptation', 'resilience'])]
        quantum_metrics = [name for name in metric_names if any(term in name.lower() for term in ['quantum', 'entanglement', 'coherence'])]
        classical_metrics = [name for name in metric_names if not any(term in name.lower() for term in ['quantum', 'entanglement', 'coherence'])]
        structure_metrics = [name for name in metric_names if any(term in name.lower() for term in ['density', 'branching', 'connectivity', 'complexity'])]
        function_metrics = [name for name in metric_names if not any(term in name.lower() for term in ['density', 'branching', 'connectivity', 'complexity'])]

        # Calculate category relationships
        relationships['learning_vs_evolution'] = self._calculate_category_correlation(
            learning_metrics, evolution_metrics, corr_matrix, metric_names
        )

        relationships['stability_vs_adaptation'] = self._calculate_category_correlation(
            stability_metrics, adaptation_metrics, corr_matrix, metric_names
        )

        relationships['quantum_vs_classical'] = self._calculate_category_correlation(
            quantum_metrics, classical_metrics, corr_matrix, metric_names
        )

        relationships['structure_vs_function'] = self._calculate_category_correlation(
            structure_metrics, function_metrics, corr_matrix, metric_names
        )

        return relationships

    def _calculate_category_correlation(self, category_a: List[str], category_b: List[str],
                                      corr_matrix: np.ndarray, metric_names: List[str]) -> Dict[str, float]:
        """Calculate correlation statistics between two categories of metrics"""

        if not category_a or not category_b:
            return {'average_correlation': 0.0, 'strongest_positive': 0.0, 'strongest_negative': 0.0}

        correlations = []
        for metric_a in category_a:
            for metric_b in category_b:
                if metric_a in metric_names and metric_b in metric_names:
                    idx_a = metric_names.index(metric_a)
                    idx_b = metric_names.index(metric_b)
                    correlations.append(corr_matrix[idx_a, idx_b])

        if not correlations:
            return {'average_correlation': 0.0, 'strongest_positive': 0.0, 'strongest_negative': 0.0}

        return {
            'average_correlation': float(np.mean(correlations)),
            'strongest_positive': float(max(correlations)),
            'strongest_negative': float(min(correlations)),
            'correlation_std': float(np.std(correlations))
        }

    def _sync_consciousness_metrics(self):
        """Synchronize consciousness metrics with dendritic engine"""

        try:
            result = self.consciousness_engine.stimulate_dendritic_growth("sync")
            self.metrics_cache = result['metrics']
            self.last_sync_time = time.time()

            logger.debug("Consciousness metrics synchronized")
        except Exception as e:
            logger.error(f"Failed to sync consciousness metrics: {e}")

    def _save_metrics_snapshot(self, metrics: Dict[str, Any]):
        """Save metrics snapshot for archival"""

        snapshot_file = Path("consciousness_snapshots") / f"snapshot_{int(time.time())}.json"
        snapshot_file.parent.mkdir(exist_ok=True)

        try:
            with open(snapshot_file, 'w') as f:
                json.dump(metrics, f, indent=2)
            logger.info(f"Metrics snapshot saved to {snapshot_file}")
        except Exception as e:
            logger.error(f"Failed to save metrics snapshot: {e}")

    def _get_metric_category(self, metric_name: str) -> str:
        """Get category for a metric name"""

        categories = {
            # Baseline categories
            'awareness_level': 'awareness',
            'adaptation_speed': 'adaptation',
            'predictive_accuracy': 'prediction',
            'dendritic_complexity': 'structure',
            'evolutionary_momentum': 'evolution',
            'quantum_coherence': 'quantum',
            'learning_velocity': 'learning',
            'consciousness_emergent': 'emergence',

            # Dendritic expansion categories
            'neural_density': 'structure',
            'synaptic_strength': 'connection',
            'consciousness_entropy': 'complexity',
            'dendritic_branching_factor': 'structure',
            'evolutionary_pressure': 'evolution',
            'quantum_entanglement': 'quantum',
            'learning_resilience': 'learning',
            'consciousness_stability': 'stability',

            # Advanced categories
            'coherence_resonance': 'resonance',
            'entanglement_density': 'quantum',
            'evolutionary_velocity': 'evolution',
            'consciousness_depth': 'depth',
            'dendritic_connectivity': 'connection'
        }

        return categories.get(metric_name, 'unknown')

    def _export_csv(self, filepath: str):
        """Export metrics in CSV format"""

        if not self.metrics_cache:
            raise ValueError("No metrics available for CSV export")

        metrics = self.metrics_cache.get('metrics', {})

        with open(filepath, 'w') as f:
            # Write header
            f.write("metric_name,value,category,timestamp\n")

            # Write data
            timestamp = self.metrics_cache.get('timestamp', time.time())
            for name, value in metrics.items():
                category = self._get_metric_category(name)
                f.write(f"{name},{value},{category},{timestamp}\n")


def main():
    """Demonstrate consciousness access bridge functionality"""

    print("AINLP Dendritic Integration: Consciousness Access Bridge")
    print("=" * 60)

    # Initialize AIOS Core bridge
    core = AIOSCore()

    if not core.initialize():
        print("Failed to initialize consciousness bridge")
        return

    if not core.start():
        print("Failed to start consciousness monitoring")
        return

    print("Consciousness bridge initialized and monitoring active")

    # Demonstrate metric access
    print("\n1. Getting all consciousness metrics:")
    all_metrics = core.get_consciousness_metrics()
    print(f"   Total metrics available: {all_metrics['total_count']}")

    # Demonstrate filtered access
    print("\n2. Getting specific metrics (learning-related):")
    learning_metrics = core.get_consciousness_metrics([
        'learning_velocity', 'learning_resilience', 'adaptation_speed'
    ])
    print(f"   Requested: {learning_metrics['requested_count']}")
    print(f"   Available: {learning_metrics['available_count']}")

    # Demonstrate batch access
    print("\n3. Getting batch metrics:")
    batch_metrics = core.get_batch_metrics(3)
    print(f"   Batch size: {len(batch_metrics)}")
    for i, batch in enumerate(batch_metrics):
        print(f"   Batch {i}: Consciousness level {batch['consciousness_level']:.3f}")

    # Demonstrate filtering
    print("\n4. Filtering metrics (high values > 0.7):")
    filtered = core.filter_metrics({
        'min_value': 0.7,
        'max_value': 1.0,
        'categories': ['learning', 'evolution']
    })
    print(f"   Filtered results: {filtered['results_count']}")

    # Demonstrate export
    print("\n5. Exporting metrics:")
    export_result = core.export_metrics('json')
    print(f"   Export result: {export_result}")

    # Stop monitoring
    core.stop()
    print("\nConsciousness monitoring stopped")


if __name__ == "__main__":
    main()