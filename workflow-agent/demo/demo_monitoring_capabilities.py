#!/usr/bin/env python3
"""
Demo monitoring tools capabilities

This script demonstrates the monitoring tools functionality
that the agents have access to during service monitoring.
"""

import sys
import os

# Add src directory to path so we can import monitoring tools
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.tools.monitoring_tools import (
    get_system_status,
    check_service_health,
    analyze_metrics,
    get_service_logs,
    check_alert_rules,
    format_monitoring_summary
)

def demo_system_status():
    """Demonstrate system status monitoring."""
    print("🖥️  SYSTEM STATUS MONITORING")
    print("=" * 40)
    
    status = get_system_status()
    summary = format_monitoring_summary(status)
    
    print("Raw data:")
    import json
    print(json.dumps(status, indent=2))
    print(f"\nFormatted summary:")
    print(summary)
    print()

def demo_service_health():
    """Demonstrate service health checking."""
    print("🏥 SERVICE HEALTH MONITORING")
    print("=" * 40)
    
    services = ["web", "api", "database", "payment", "auth"]
    
    for service in services:
        health = check_service_health(service)
        summary = format_monitoring_summary(health)
        print(f"Service: {service}")
        print(f"  {summary}")
        if not health["healthy"]:
            print(f"  ❌ Error: {health.get('error', 'Unknown issue')}")
        print()

def demo_metrics_analysis():
    """Demonstrate metrics analysis."""
    print("📊 METRICS ANALYSIS")
    print("=" * 40)
    
    service = "web"
    metrics = ["cpu", "memory", "response_time", "error_rate"]
    
    for metric in metrics:
        analysis = analyze_metrics(service, metric, "1h")
        summary = format_monitoring_summary(analysis)
        print(f"Metric: {metric}")
        print(f"  {summary}")
        
        if analysis["status"] != "ok":
            print(f"  ⚠️  Status: {analysis['status']}")
        print()

def demo_log_analysis():
    """Demonstrate log analysis."""
    print("📋 LOG ANALYSIS")
    print("=" * 40)
    
    service = "api"
    log_levels = ["error", "warn", "info"]
    
    for level in log_levels:
        logs = get_service_logs(service, level, 10)
        summary = format_monitoring_summary(logs)
        print(f"Log Level: {level}")
        print(f"  {summary}")
        
        # Show recent log entries
        if logs["logs"]:
            print("  Recent entries:")
            for log in logs["logs"][:3]:
                print(f"    [{log['timestamp']}] {log['level']}: {log['message']}")
        print()

def demo_alert_rules():
    """Demonstrate alert rule checking."""
    print("🚨 ALERT RULES MONITORING")
    print("=" * 40)
    
    services = ["web", "api", "database"]
    
    for service in services:
        alerts = check_alert_rules(service)
        print(f"Service: {service}")
        print(f"  Configured rules: {len(alerts['alert_rules'])}")
        print(f"  Triggered alerts: {len(alerts['triggered_alerts'])}")
        print(f"  Status: {alerts['status']}")
        
        if alerts["triggered_alerts"]:
            print("  🔥 Active alerts:")
            for alert in alerts["triggered_alerts"]:
                rule = alert["rule"]
                print(f"    - {rule['metric']} > {rule['threshold']} ({rule['severity']})")
                print(f"      Current value: {alert['current_value']}")
        print()

def demo_real_time_monitoring():
    """Demonstrate continuous monitoring simulation."""
    print("⏰ REAL-TIME MONITORING SIMULATION")
    print("=" * 40)
    print("Simulating continuous monitoring for 5 cycles...")
    
    import time
    
    for cycle in range(1, 6):
        print(f"\nCycle {cycle}:")
        
        # Check overall system health
        system_status = get_system_status()
        print(f"  System Status: {system_status['status']}")
        
        # Check critical service
        critical_service = check_service_health("payment")
        if not critical_service["healthy"]:
            print(f"  🚨 CRITICAL: Payment service is down!")
            print(f"     Error: {critical_service.get('error')}")
        else:
            print(f"  ✅ Payment service healthy ({critical_service['response_time_ms']}ms)")
        
        # Check for alerts
        alerts = check_alert_rules("payment")
        if alerts["triggered_alerts"]:
            print(f"  ⚠️  {len(alerts['triggered_alerts'])} active alerts")
        
        # Simulate monitoring interval
        time.sleep(1)
    
    print("\nReal-time monitoring simulation complete!")

def main():
    """Run all monitoring tool demos."""
    print("🔍 SERVICE MONITORING TOOLS DEMO")
    print("=" * 50)
    print("This demo shows the monitoring capabilities available to the AI agents.\n")
    
    demos = [
        ("System Status", demo_system_status),
        ("Service Health", demo_service_health),
        ("Metrics Analysis", demo_metrics_analysis),
        ("Log Analysis", demo_log_analysis),
        ("Alert Rules", demo_alert_rules),
        ("Real-time Monitoring", demo_real_time_monitoring)
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        print(f"\n{i}. {name}")
        print("-" * 50)
        
        try:
            demo_func()
        except Exception as e:
            print(f"❌ Error in {name} demo: {str(e)}")
        
        if i < len(demos):
            print("\nPress Enter to continue...")
            input()
    
    print("\n" + "=" * 50)
    print("🎉 ALL DEMOS COMPLETE!")
    print("=" * 50)
    print("These tools provide the AI agents with:")
    print("• Real-time system and service monitoring")
    print("• Historical performance analysis")
    print("• Log parsing and error detection")
    print("• Alert management and escalation")
    print("• Comprehensive status reporting")
    print("\nIn production, these tools can be extended to:")
    print("• Connect to Prometheus, Grafana, or other monitoring systems")
    print("• Interface with your existing alerting infrastructure")
    print("• Access real service logs and metrics")
    print("• Integrate with incident management systems")

if __name__ == "__main__":
    main()