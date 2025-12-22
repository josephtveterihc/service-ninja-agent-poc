#!/usr/bin/env python3
"""
Demo service monitoring workflow - no Azure required

This demo simulates the service monitoring workflow using mock agents
to showcase the monitoring capabilities without requiring Azure setup.
"""

import asyncio
import random
from datetime import datetime
import json

class MockMonitoringAgent:
    """Mock agent for demonstration purposes."""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
    
    async def process_request(self, message: str) -> str:
        """Simulate agent processing with appropriate responses."""
        
        # Simulate processing delay
        await asyncio.sleep(random.uniform(0.5, 1.5))
        
        if self.role == "detector":
            return self._detector_response(message)
        elif self.role == "analyzer":
            return self._analyzer_response(message)
        elif self.role == "alerting":
            return self._alerting_response(message)
        elif self.role == "info":
            return self._info_response(message)
        
        return f"{self.name}: I received '{message}'"
    
    def _detector_response(self, message: str) -> str:
        """Generate detector agent response."""
        issues = [
            "High CPU utilization detected on web servers (85%)",
            "Database connection timeout errors increasing", 
            "Payment service response time degradation (>2s)",
            "Memory usage approaching critical threshold (90%)",
            "Authentication service returning 500 errors"
        ]
        
        detected_issue = random.choice(issues)
        severity = random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        
        return f"""🔍 ISSUE DETECTED:
        
Issue: {detected_issue}
Severity: {severity}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Service: {random.choice(['web', 'api', 'database', 'payment', 'auth'])}

Initial Assessment:
- Automated monitoring alert triggered
- Service metrics exceeded defined thresholds
- Requires further investigation

Routing to Analyzer Agent for detailed investigation..."""

    def _analyzer_response(self, message: str) -> str:
        """Generate analyzer agent response."""
        root_causes = [
            "Memory leak in application code causing gradual degradation",
            "Database query optimization needed - slow JOIN operations",
            "Traffic spike from marketing campaign overwhelming capacity", 
            "Network connectivity issues between services",
            "Configuration change deployed causing service instability"
        ]
        
        recommendations = [
            "Restart affected services to clear memory leaks",
            "Scale up instances to handle increased load",
            "Optimize database queries and add indexes",
            "Check network infrastructure and routing",
            "Rollback recent configuration changes"
        ]
        
        root_cause = random.choice(root_causes)
        recommendation = random.choice(recommendations)
        
        return f"""🔬 ANALYSIS COMPLETE:

Root Cause Analysis:
{root_cause}

Impact Assessment:
- Affected Services: 3 downstream services
- User Impact: Response times increased 300%
- Business Impact: Payment processing delays

Recommended Actions:
1. {recommendation}
2. Monitor service recovery metrics
3. Implement preventive measures

Evidence:
- CPU metrics showing sustained 85%+ usage
- Error logs indicating timeout patterns
- Response time trending upward for 15 minutes

Escalating to Alerting Agent for notification..."""

    def _alerting_response(self, message: str) -> str:
        """Generate alerting agent response."""
        severity = random.choice(["WARNING", "CRITICAL"])
        
        if severity == "CRITICAL":
            escalation = """
IMMEDIATE ACTIONS:
🚨 CRITICAL ALERT TRIGGERED
- Paging on-call engineer immediately
- Notifying incident commander
- Creating incident channel #incident-12345
- Setting up war room for coordination

Escalation Timeline:
- T+0: On-call engineer paged
- T+15min: Escalate to senior engineer if not resolved
- T+30min: Notify service owner and management
- T+1hr: Executive escalation if service still impacted"""
        else:
            escalation = """
STANDARD ESCALATION:
⚠️ Warning alert issued
- Notification sent to team Slack channel
- Creating monitoring dashboard
- On-call engineer notified via email

Next Actions:
- Monitor for 10 minutes for auto-recovery
- Escalate to senior engineer if degradation continues
- Update status page if customer-facing impact"""

        return f"""📢 ALERT PROCESSING COMPLETE:

Alert Details:
- Severity Level: {severity}
- Alert ID: ALT-{random.randint(10000, 99999)}
- Service: Production System
- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{escalation}

Communication Sent:
✅ Team notification via Slack
✅ Status page updated
✅ Monitoring dashboard activated
✅ Incident tracking ticket created

Monitoring for resolution..."""

    def _info_response(self, message: str) -> str:
        """Generate info agent response."""
        info_responses = {
            "status": """📊 SYSTEM STATUS OVERVIEW:

Overall Health: 🟢 GOOD (3 services normal, 1 warning)

Service Status:
- Web Service: 🟢 Healthy (150ms avg response)
- API Gateway: 🟢 Healthy (95ms avg response) 
- Database: 🟡 Warning (high CPU but stable)
- Payment Service: 🟢 Healthy (200ms avg response)
- Auth Service: 🟢 Healthy (50ms avg response)

System Resources:
- CPU Usage: 65% (normal)
- Memory Usage: 72% (normal)
- Disk Space: 85% (monitor closely)

Recent Activity:
- No critical alerts in last 24 hours
- 2 warnings resolved automatically
- Last deployment: 3 days ago (successful)""",

            "metrics": """📈 PERFORMANCE METRICS:

Key Performance Indicators (Last 24h):
- Average Response Time: 180ms (↓15ms from yesterday)
- Error Rate: 0.02% (within SLA of 0.1%)
- Uptime: 99.98% (SLA: 99.9%)
- Throughput: 1,250 req/min (normal load)

Top Services by Traffic:
1. API Gateway: 45% of total traffic
2. Web Service: 35% of total traffic
3. Payment Service: 20% of total traffic

Resource Utilization:
- Peak CPU: 82% (during 2PM traffic spike)
- Peak Memory: 88% (database during backup)
- Network I/O: Normal patterns

Trends:
📈 Traffic up 12% week-over-week
📉 Error rate down 25% from last week""",

            "policies": """📋 MONITORING POLICIES:

Alert Thresholds:
- CPU Usage: Warning >75%, Critical >90%
- Memory Usage: Warning >80%, Critical >95%
- Response Time: Warning >500ms, Critical >2s
- Error Rate: Warning >0.1%, Critical >1%

Escalation Procedures:
1. Level 1: Team notification (immediate)
2. Level 2: On-call engineer (5 minutes)
3. Level 3: Senior engineer (15 minutes)  
4. Level 4: Service owner (30 minutes)
5. Level 5: Management (1 hour)

On-Call Schedule:
- Primary: Alice Johnson (Dec 10-16)
- Secondary: Bob Smith (backup)
- Escalation: Sarah Wilson (team lead)

SLA Commitments:
- 99.9% uptime guarantee
- <500ms average response time
- <0.1% error rate threshold"""
        }
        
        # Determine response type based on keywords
        message_lower = message.lower()
        if any(word in message_lower for word in ['status', 'health', 'overview']):
            return info_responses['status']
        elif any(word in message_lower for word in ['metrics', 'performance', 'stats']):
            return info_responses['metrics']
        elif any(word in message_lower for word in ['policy', 'policies', 'rules', 'escalation']):
            return info_responses['policies']
        else:
            return random.choice(list(info_responses.values()))

async def demo_monitoring_workflow():
    """Run the demo monitoring workflow."""
    
    print("🔍 SERVICE MONITORING AGENT DEMO")
    print("=" * 50)
    print("This demo showcases the monitoring workflow without requiring Azure setup.")
    print("The agents will simulate real monitoring scenarios.\n")
    
    # Create mock agents
    detector = MockMonitoringAgent("Detector", "detector")
    analyzer = MockMonitoringAgent("Analyzer", "analyzer") 
    alerting = MockMonitoringAgent("Alerting", "alerting")
    info = MockMonitoringAgent("Info", "info")
    
    # Demo scenarios
    scenarios = [
        {
            "name": "Service Health Investigation",
            "input": "Investigate high response times on payment service",
            "workflow": ["detector", "analyzer", "alerting"]
        },
        {
            "name": "System Status Inquiry",
            "input": "What's the current status of all services?",
            "workflow": ["info"]
        },
        {
            "name": "Performance Monitoring",
            "input": "Show me performance metrics for the last 24 hours",
            "workflow": ["info"]
        },
        {
            "name": "Critical Alert Processing",
            "input": "Database CPU usage at 95% - critical alert triggered",
            "workflow": ["detector", "analyzer", "alerting"]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*60}")
        print(f"DEMO SCENARIO {i}: {scenario['name']}")
        print(f"{'='*60}")
        print(f"User Input: \"{scenario['input']}\"\n")
        
        # Process through workflow
        current_message = scenario['input']
        
        for agent_type in scenario['workflow']:
            if agent_type == "detector":
                print("🔍 Routing to Detector Agent...")
                response = await detector.process_request(current_message)
                print(response)
                current_message = response
                
            elif agent_type == "analyzer":
                print("\n🔬 Routing to Analyzer Agent...")
                response = await analyzer.process_request(current_message)
                print(response)
                current_message = response
                
            elif agent_type == "alerting":
                print("\n📢 Routing to Alerting Agent...")
                response = await alerting.process_request(current_message)
                print(response)
                
            elif agent_type == "info":
                print("ℹ️ Processing with Info Agent...")
                response = await info.process_request(current_message)
                print(response)
        
        print(f"\n✅ Scenario {i} Complete")
        
        if i < len(scenarios):
            print("\nPress Enter to continue to next scenario...")
            input()
    
    print(f"\n{'='*60}")
    print("🎉 DEMO COMPLETE!")
    print("=" * 60)
    print("This was a simulation of the Service Monitoring Agent workflow.")
    print("In production, these agents would:")
    print("• Connect to real monitoring systems")
    print("• Access actual service metrics and logs") 
    print("• Send real alerts and notifications")
    print("• Reference your organization's runbooks")
    print("\nTo set up the production version:")
    print("1. Configure your Microsoft Foundry project")
    print("2. Update endpoints in service_monitoring_workflow.py")
    print("3. Add your monitoring integrations")
    print("4. Customize agent instructions for your environment")

def main():
    """Main entry point for the demo."""
    try:
        asyncio.run(demo_monitoring_workflow())
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for trying Service Monitoring Agent!")
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")

if __name__ == "__main__":
    main()