"""
Service Monitoring Agent Package

A Microsoft Agent Framework-based system for monitoring services
with AI agents, automated detection, analysis, and alerting.
"""

from .service_monitoring_workflow import main
from .tools.monitoring_tools import (
    get_system_status,
    check_service_health,
    analyze_metrics,
    get_service_logs,
    check_alert_rules,
    MONITORING_TOOLS
)

__version__ = "1.0.0"
__author__ = "AI Assistant"
__description__ = "Intelligent service monitoring with AI agents and monitoring tools"

__all__ = [
    "main",
    "get_system_status", 
    "check_service_health",
    "analyze_metrics", 
    "get_service_logs",
    "check_alert_rules",
    "MONITORING_TOOLS"
]