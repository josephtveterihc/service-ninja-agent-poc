#!/usr/bin/env python3
"""
Test suite for monitoring tools

Tests the service monitoring functionality to ensure
all monitoring tools work correctly.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.tools.monitoring_tools import (
    get_system_status,
    check_service_health,
    analyze_metrics,
    get_service_logs,
    check_alert_rules,
    format_monitoring_summary
)

class TestMonitoringTools(unittest.TestCase):
    """Test cases for monitoring tools functionality."""
    
    def test_get_system_status(self):
        """Test system status retrieval."""
        print("\n🧪 Testing system status retrieval...")
        
        status = get_system_status()
        
        # Verify required fields exist
        self.assertIn('timestamp', status)
        self.assertIn('status', status)
        
        if 'system' in status:
            system = status['system']
            self.assertIn('cpu_usage', system)
            self.assertIn('memory_usage', system)
            self.assertIn('disk_usage', system)
            
            # Verify reasonable ranges
            self.assertGreaterEqual(system['cpu_usage'], 0)
            self.assertLessEqual(system['cpu_usage'], 100)
            
            print(f"✅ System status test passed - CPU: {system['cpu_usage']:.1f}%")
        else:
            print("✅ System status test passed (error case)")
    
    def test_check_service_health(self):
        """Test service health checking."""
        print("\n🧪 Testing service health checking...")
        
        services = ['web', 'api', 'database', 'payment']
        
        for service in services:
            health = check_service_health(service)
            
            # Verify required fields
            self.assertIn('service', health)
            self.assertIn('timestamp', health)
            self.assertIn('healthy', health)
            self.assertIn('response_time_ms', health)
            self.assertIn('status_code', health)
            
            # Verify service name matches
            self.assertEqual(health['service'], service)
            
            # Verify response time is reasonable
            self.assertGreater(health['response_time_ms'], 0)
            self.assertLess(health['response_time_ms'], 5000)  # Less than 5 seconds
            
        print(f"✅ Service health test passed for {len(services)} services")
    
    def test_analyze_metrics(self):
        """Test metrics analysis."""
        print("\n🧪 Testing metrics analysis...")
        
        service = 'test-service'
        metrics = ['cpu', 'memory', 'response_time', 'error_rate']
        time_ranges = ['5m', '1h', '24h']
        
        for metric in metrics:
            for time_range in time_ranges:
                analysis = analyze_metrics(service, metric, time_range)
                
                # Verify required fields
                self.assertIn('service', analysis)
                self.assertIn('metric_type', analysis)
                self.assertIn('time_range', analysis)
                self.assertIn('status', analysis)
                self.assertIn('statistics', analysis)
                self.assertIn('metrics', analysis)
                
                # Verify values match input
                self.assertEqual(analysis['service'], service)
                self.assertEqual(analysis['metric_type'], metric)
                self.assertEqual(analysis['time_range'], time_range)
                
                # Verify statistics
                stats = analysis['statistics']
                self.assertIn('average', stats)
                self.assertIn('maximum', stats)
                self.assertIn('minimum', stats)
                self.assertGreaterEqual(stats['maximum'], stats['average'])
                self.assertLessEqual(stats['minimum'], stats['average'])
        
        print(f"✅ Metrics analysis test passed for {len(metrics)} metrics")
    
    def test_get_service_logs(self):
        """Test log retrieval and analysis."""
        print("\n🧪 Testing service log retrieval...")
        
        service = 'test-service'
        log_levels = ['error', 'warn', 'info', 'debug']
        
        for level in log_levels:
            logs = get_service_logs(service, level, 20)
            
            # Verify required fields
            self.assertIn('service', logs)
            self.assertIn('log_level', logs)
            self.assertIn('timestamp', logs)
            self.assertIn('total_entries', logs)
            self.assertIn('analysis', logs)
            self.assertIn('logs', logs)
            
            # Verify service name and level
            self.assertEqual(logs['service'], service)
            self.assertEqual(logs['log_level'], level.upper())
            
            # Verify log entries structure
            for log_entry in logs['logs'][:5]:  # Check first 5 entries
                self.assertIn('timestamp', log_entry)
                self.assertIn('level', log_entry)
                self.assertIn('message', log_entry)
                self.assertIn('service', log_entry)
                
                self.assertEqual(log_entry['level'], level.upper())
                self.assertEqual(log_entry['service'], service)
        
        print(f"✅ Log retrieval test passed for {len(log_levels)} log levels")
    
    def test_check_alert_rules(self):
        """Test alert rule checking."""
        print("\n🧪 Testing alert rule checking...")
        
        services = ['web', 'api', 'database', 'unknown-service']
        
        for service in services:
            alerts = check_alert_rules(service)
            
            # Verify required fields
            self.assertIn('service', alerts)
            self.assertIn('timestamp', alerts)
            self.assertIn('alert_rules', alerts)
            self.assertIn('triggered_alerts', alerts)
            self.assertIn('status', alerts)
            
            # Verify service name
            self.assertEqual(alerts['service'], service)
            
            # Verify alert rules structure
            for rule in alerts['alert_rules']:
                self.assertIn('metric', rule)
                self.assertIn('threshold', rule)
                self.assertIn('severity', rule)
            
            # Verify triggered alerts structure
            for alert in alerts['triggered_alerts']:
                self.assertIn('rule', alert)
                self.assertIn('triggered_at', alert)
                self.assertIn('current_value', alert)
        
        print(f"✅ Alert rules test passed for {len(services)} services")
    
    def test_format_monitoring_summary(self):
        """Test monitoring data formatting."""
        print("\n🧪 Testing monitoring data formatting...")
        
        # Test system status formatting
        system_data = {
            'status': 'healthy',
            'system': {
                'cpu_usage': 45.2,
                'memory_usage': 68.7,
                'disk_usage': 23.1
            }
        }
        
        summary = format_monitoring_summary(system_data)
        self.assertIsInstance(summary, str)
        self.assertIn('System Status', summary)
        self.assertIn('45.2%', summary)
        
        # Test service health formatting
        service_data = {
            'service': 'web',
            'healthy': True,
            'response_time_ms': 150,
            'status_code': 200
        }
        
        summary = format_monitoring_summary(service_data)
        self.assertIsInstance(summary, str)
        self.assertIn('web', summary)
        self.assertIn('150ms', summary)
        
        print("✅ Formatting test passed")
    
    def test_integration_workflow(self):
        """Test complete monitoring workflow integration."""
        print("\n🧪 Testing complete monitoring workflow...")
        
        # Simulate complete monitoring check
        service_name = 'production-api'
        
        # Step 1: Check system status
        system_status = get_system_status()
        self.assertIn('status', system_status)
        
        # Step 2: Check service health
        service_health = check_service_health(service_name)
        self.assertIn('healthy', service_health)
        
        # Step 3: Analyze metrics if service is unhealthy
        if not service_health['healthy']:
            metrics_analysis = analyze_metrics(service_name, 'cpu', '1h')
            self.assertIn('status', metrics_analysis)
        
        # Step 4: Check logs for errors
        error_logs = get_service_logs(service_name, 'error', 10)
        self.assertIn('analysis', error_logs)
        
        # Step 5: Check alert rules
        alert_status = check_alert_rules(service_name)
        self.assertIn('triggered_alerts', alert_status)
        
        print("✅ Integration workflow test passed")

def run_monitoring_tool_demos():
    """Run interactive demos of monitoring tools."""
    print("\n🎯 MONITORING TOOLS DEMONSTRATION")
    print("=" * 50)
    
    print("\n1. System Status Check:")
    status = get_system_status()
    print(format_monitoring_summary(status))
    
    print("\n2. Service Health Checks:")
    for service in ['web', 'api', 'database']:
        health = check_service_health(service)
        print(f"  {format_monitoring_summary(health)}")
    
    print("\n3. Metrics Analysis Sample:")
    metrics = analyze_metrics('web', 'cpu', '1h')
    print(f"  {format_monitoring_summary(metrics)}")
    
    print("\n4. Log Analysis Sample:")
    logs = get_service_logs('api', 'error', 5)
    print(f"  {format_monitoring_summary(logs)}")
    
    print("\n5. Alert Status Check:")
    alerts = check_alert_rules('database')
    print(f"  Service: {alerts['service']}")
    print(f"  Alert Rules: {len(alerts['alert_rules'])}")
    print(f"  Triggered Alerts: {len(alerts['triggered_alerts'])}")
    print(f"  Status: {alerts['status']}")

def main():
    """Run tests with optional demo mode."""
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        run_monitoring_tool_demos()
        return
    
    print("🧪 MONITORING TOOLS TEST SUITE")
    print("=" * 40)
    
    # Run the test suite
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n" + "=" * 40)
    print("✅ All monitoring tools tests completed!")
    print("=" * 40)
    print("\nTo see interactive demos, run:")
    print("python test_monitoring_tools.py --demo")

if __name__ == '__main__':
    main()