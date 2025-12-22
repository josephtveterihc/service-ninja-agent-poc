"""
Service monitoring utilities for the monitoring workflow system.
Provides tools to check service health, analyze metrics, parse logs, and manage alerts.
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import os
import subprocess
import psutil

"""
  Method: get_system_status
  Description: Get current system status and health metrics
  Args:
    None
  Returns:
    Dict[str, Any]: System status including CPU, memory, disk usage and overall health
"""
def get_system_status() -> Dict[str, Any]:
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        status = {
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available": memory.available,
                "disk_usage": disk.percent,
                "disk_free": disk.free
            },
            "status": "healthy" if cpu_percent < 80 and memory.percent < 85 else "warning"
        }
        
        return status
    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "status": "error"
        }

"""
  Method: check_service_health
  Description: Check the health status of a specific service
  Args:
    service_name (str): Name of the service to check (e.g., 'web', 'api', 'database')
    endpoint (Optional[str]): Optional endpoint URL to test (defaults to None)
  Returns:
    Dict[str, Any]: Service health status including response time, status, and details
"""
def check_service_health(service_name: str, endpoint: str = None) -> Dict[str, Any]:
    
    # Simulate service health check
    # In a real implementation, this would make HTTP requests, check process status, etc.
    services = {
        "web": {"port": 80, "process": "nginx"},
        "api": {"port": 8080, "process": "api-server"},
        "database": {"port": 5432, "process": "postgres"},
        "cache": {"port": 6379, "process": "redis"},
        "auth": {"port": 8000, "process": "auth-service"},
        "payment": {"port": 8001, "process": "payment-service"}
    }
    
    service_info = services.get(service_name.lower(), {"port": 8080, "process": service_name})
    
    # Simulate health check results
    is_healthy = random.choice([True, True, True, False])  # 75% healthy
    response_time = random.randint(50, 500)  # ms
    
    status = {
        "service": service_name,
        "endpoint": endpoint or f"http://localhost:{service_info['port']}",
        "timestamp": datetime.now().isoformat(),
        "healthy": is_healthy,
        "response_time_ms": response_time,
        "status_code": 200 if is_healthy else random.choice([500, 503, 404]),
        "details": {
            "port": service_info["port"],
            "process": service_info["process"],
            "uptime": f"{random.randint(1, 720)} hours"
        }
    }
    
    if not is_healthy:
        status["error"] = random.choice([
            "Connection timeout",
            "Service unavailable", 
            "Database connection failed",
            "High response time",
            "Authentication failed"
        ])
    
    return status

"""
  Method: analyze_metrics
  Description: Analyze service metrics over a specified time range
  Args:
    service_name (str): Name of the service to analyze
    metric_type (str): Type of metric to analyze (default: 'cpu')
    time_range (str): Time range for analysis (default: '1h')
  Returns:
    Dict[str, Any]: Metrics analysis including current, average, min, max values and trends
"""
def analyze_metrics(service_name: str, metric_type: str = "cpu", time_range: str = "1h") -> Dict[str, Any]:
    
    # Simulate metric analysis
    time_ranges = {
        "5m": 5,
        "15m": 15, 
        "1h": 60,
        "6h": 360,
        "24h": 1440
    }
    
    minutes = time_ranges.get(time_range, 60)
    
    # Generate sample metric data
    metrics = []
    base_time = datetime.now() - timedelta(minutes=minutes)
    
    for i in range(0, minutes, max(1, minutes//20)):  # ~20 data points
        timestamp = base_time + timedelta(minutes=i)
        
        if metric_type == "cpu":
            value = random.uniform(10, 90)
        elif metric_type == "memory":
            value = random.uniform(30, 80)
        elif metric_type == "response_time":
            value = random.uniform(50, 1000)
        elif metric_type == "error_rate":
            value = random.uniform(0, 5)
        else:
            value = random.uniform(0, 100)
            
        metrics.append({
            "timestamp": timestamp.isoformat(),
            "value": round(value, 2)
        })
    
    # Calculate statistics
    values = [m["value"] for m in metrics]
    avg_value = sum(values) / len(values)
    max_value = max(values)
    min_value = min(values)
    
    # Determine status based on thresholds
    thresholds = {
        "cpu": {"warning": 70, "critical": 90},
        "memory": {"warning": 75, "critical": 90},
        "response_time": {"warning": 500, "critical": 1000},
        "error_rate": {"warning": 2, "critical": 5}
    }
    
    threshold = thresholds.get(metric_type, {"warning": 70, "critical": 90})
    
    if avg_value > threshold["critical"]:
        status = "critical"
    elif avg_value > threshold["warning"]:
        status = "warning"
    else:
        status = "ok"
    
    return {
        "service": service_name,
        "metric_type": metric_type,
        "time_range": time_range,
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "statistics": {
            "average": round(avg_value, 2),
            "maximum": round(max_value, 2),
            "minimum": round(min_value, 2),
            "data_points": len(metrics)
        },
        "metrics": metrics[-5:],  # Return last 5 data points
        "thresholds": threshold
    }

"""
  Method: get_service_logs
  Description: Retrieve and parse service logs for analysis
  Args:
    service_name (str): Name of the service to get logs for
    level (str): Log level to filter by (default: 'error')
    lines (int): Number of log lines to retrieve (default: 50)
  Returns:
    Dict[str, Any]: Service logs with entries, summary, and metadata
"""
def get_service_logs(service_name: str, level: str = "error", lines: int = 50) -> Dict[str, Any]:
    
    # Simulate log entries
    log_levels = ["INFO", "WARN", "ERROR", "DEBUG"]
    if level.upper() in log_levels:
        target_level = level.upper()
    else:
        target_level = "ERROR"
    
    sample_messages = {
        "ERROR": [
            "Database connection timeout after 30 seconds",
            "Failed to authenticate user: invalid token",
            "Service unavailable: circuit breaker open",
            "Memory allocation failed: out of memory",
            "API request failed with status 500"
        ],
        "WARN": [
            "High CPU usage detected: 85%",
            "Slow query detected: execution time 2.5s",
            "Rate limit approaching: 90% of quota used",
            "Disk space low: 15% remaining",
            "Cache miss ratio high: 75%"
        ],
        "INFO": [
            "Service started successfully",
            "Health check passed",
            "User authenticated successfully",
            "Request processed in 150ms",
            "Database connection established"
        ]
    }
    
    # Generate log entries
    logs = []
    messages = sample_messages.get(target_level, sample_messages["ERROR"])
    
    for i in range(min(lines, 100)):  # Limit to 100 entries
        timestamp = datetime.now() - timedelta(minutes=i*5)
        log_entry = {
            "timestamp": timestamp.isoformat(),
            "level": target_level,
            "service": service_name,
            "message": random.choice(messages),
            "request_id": f"req_{random.randint(1000, 9999)}"
        }
        logs.append(log_entry)
    
    # Analyze logs for patterns
    error_count = len([log for log in logs if log["level"] == "ERROR"])
    warning_count = len([log for log in logs if log["level"] == "WARN"])
    
    return {
        "service": service_name,
        "log_level": target_level,
        "timestamp": datetime.now().isoformat(),
        "total_entries": len(logs),
        "analysis": {
            "error_count": error_count,
            "warning_count": warning_count,
            "recent_errors": error_count > 5,
            "status": "critical" if error_count > 10 else "warning" if error_count > 5 else "ok"
        },
        "logs": logs[:10]  # Return first 10 entries
    }

"""
  Method: check_alert_rules
  Description: Check if any alert rules are triggered for a service
  Args:
    service_name (str): Name of the service to check alert rules for
  Returns:
    Dict[str, Any]: Alert rules status including triggered alerts and rule details
"""
def check_alert_rules(service_name: str) -> Dict[str, Any]:
    
    # Simulate alert rules configuration
    alert_rules = {
        "web": [
            {"metric": "response_time", "threshold": 500, "severity": "warning"},
            {"metric": "error_rate", "threshold": 2, "severity": "critical"},
            {"metric": "cpu_usage", "threshold": 80, "severity": "warning"}
        ],
        "api": [
            {"metric": "response_time", "threshold": 200, "severity": "warning"},
            {"metric": "memory_usage", "threshold": 85, "severity": "critical"},
            {"metric": "request_rate", "threshold": 1000, "severity": "info"}
        ],
        "database": [
            {"metric": "cpu_usage", "threshold": 70, "severity": "warning"},
            {"metric": "connection_count", "threshold": 100, "severity": "warning"},
            {"metric": "disk_usage", "threshold": 90, "severity": "critical"}
        ]
    }
    
    rules = alert_rules.get(service_name.lower(), [
        {"metric": "cpu_usage", "threshold": 80, "severity": "warning"},
        {"metric": "memory_usage", "threshold": 85, "severity": "critical"}
    ])
    
    # Check if any rules are currently triggered
    triggered_alerts = []
    for rule in rules:
        if random.choice([True, False, False]):  # 33% chance of trigger
            triggered_alerts.append({
                "rule": rule,
                "triggered_at": datetime.now().isoformat(),
                "current_value": rule["threshold"] + random.randint(1, 20)
            })
    
    return {
        "service": service_name,
        "timestamp": datetime.now().isoformat(),
        "alert_rules": rules,
        "triggered_alerts": triggered_alerts,
        "status": "alerting" if triggered_alerts else "ok"
    }

"""
  Method: format_monitoring_summary
  Description: Format monitoring data into a readable summary
  Args:
    data (Dict[str, Any]): Raw monitoring data to format
  Returns:
    str: Formatted, human-readable summary of monitoring data
"""
def format_monitoring_summary(data: Dict[str, Any]) -> str:
    
    if "system" in data:
        # System status summary
        system = data["system"]
        return f"System Status: {data['status']} | CPU: {system['cpu_usage']:.1f}% | Memory: {system['memory_usage']:.1f}% | Disk: {system['disk_usage']:.1f}%"
    
    elif "service" in data and "healthy" in data:
        # Service health summary
        health_status = "✅ Healthy" if data["healthy"] else "❌ Unhealthy"
        return f"Service {data['service']}: {health_status} | Response: {data['response_time_ms']}ms | Status: {data['status_code']}"
    
    elif "metric_type" in data:
        # Metrics summary
        stats = data["statistics"]
        return f"Metrics for {data['service']} ({data['metric_type']}): Avg: {stats['average']}, Max: {stats['maximum']}, Status: {data['status']}"
    
    elif "log_level" in data:
        # Logs summary
        analysis = data["analysis"]
        return f"Logs for {data['service']}: {data['total_entries']} entries | Errors: {analysis['error_count']} | Status: {analysis['status']}"
    
    else:
        return str(data)

# Tool definitions for the agent framework
MONITORING_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_system_status",
            "description": "Get current system status including CPU, memory, and disk usage",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "check_service_health",
            "description": "Check the health status of a specific service",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service to check (e.g., 'web', 'api', 'database')"
                    },
                    "endpoint": {
                        "type": "string", 
                        "description": "Optional service endpoint URL to check"
                    }
                },
                "required": ["service_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_metrics", 
            "description": "Analyze service metrics over a specified time range",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service to analyze"
                    },
                    "metric_type": {
                        "type": "string",
                        "description": "Type of metric to analyze",
                        "enum": ["cpu", "memory", "response_time", "error_rate"]
                    },
                    "time_range": {
                        "type": "string", 
                        "description": "Time range for analysis",
                        "enum": ["5m", "15m", "1h", "6h", "24h"]
                    }
                },
                "required": ["service_name", "metric_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_service_logs",
            "description": "Retrieve and analyze service logs",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service to get logs for"
                    },
                    "level": {
                        "type": "string",
                        "description": "Log level to filter by",
                        "enum": ["error", "warn", "info", "debug"]
                    },
                    "lines": {
                        "type": "integer",
                        "description": "Number of log lines to retrieve (max 100)"
                    }
                },
                "required": ["service_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_alert_rules",
            "description": "Check configured alert rules for a service",
            "parameters": {
                "type": "object", 
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service to check alert rules for"
                    }
                },
                "required": ["service_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "format_monitoring_summary",
            "description": "Format monitoring data into human-readable summary",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "Monitoring data to format"
                    }
                },
                "required": ["data"]
            }
        }
    }
]