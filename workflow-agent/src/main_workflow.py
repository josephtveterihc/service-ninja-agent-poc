from azure.identity.aio import DefaultAzureCredential
from agent_framework import (
    ChatAgent,
    ChatMessage,
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    WorkflowOutputEvent,
    handler,
    executor,
)

import asyncio
import json
import os
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

# Add the src directory to Python path for imports when running as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import agent utilities
try:
    from .project_util.agent_util import get_agent_list, get_agent_by_name, get_agent_by_id, get_agents_by_name, print_agent_instructions
    from .tools.monitoring_tools import (
        get_system_status, check_service_health, analyze_metrics, 
        get_service_logs, check_alert_rules, format_monitoring_summary
    )
except ImportError:
    from project_util.agent_util import get_agent_list, get_agent_by_name, get_agent_by_id, get_agents_by_name, print_agent_instructions
    from tools.monitoring_tools import (
        get_system_status, check_service_health, analyze_metrics, 
        get_service_logs, check_alert_rules, format_monitoring_summary
    )

from azure.ai.projects.aio import AIProjectClient

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Load .env file from the parent directory (workflow-agent/)
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    load_dotenv(env_path)
except ImportError:
    # python-dotenv not installed, skip loading .env file
    pass


class InputSource(Enum):
    """Enumeration for different input sources"""
    COMMAND_LINE = "cli"
    API_CALL = "api"
    TEAMS_INTEGRATION = "teams"


class MonitoringWorkflow:
    """
    Main workflow coordinator for the service monitoring agent system.
    Manages multiple specialized agents and routes requests based on context.
    """
    
    """
      Method: __init__
      Description: Initialize the MonitoringWorkflow with empty agents and context
      Args:
        None
      Returns:
        None: Initializes instance variables for agents, session_id, and context
    """
    def __init__(self):
        self.agents = {}
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.context = {
            "current_services": [],
            "recent_issues": [],
            "alert_rules": {},
            "session_id": self.session_id
        }
        self.workflow = self.initialize_agents()
    
    """
      Method: initialize_agents
      Description: Initialize all required monitoring agents from Azure AI Projects
      Args:
        None
      Returns:
        bool: True if at least one agent was successfully initialized, False otherwise
    """
    async def initialize_agents(self):
        required_agents = {
            "main": "JET-Service-Ninja-Agent",
            "route_request": "JET-Service-Ninja-Agent-Request-Router",
            "status_checker": "JET-Service-Ninja-Agent-Status-Checker", 
            "solution_finder": "JET-Service-Ninja-Agent-Solution-Finder",
            "data_processor": "JET-Service-Ninja-Agent-Data-Processor"
        }
        
        print("🚀 Initializing Service Monitoring Workflow")
        print("=" * 60)
        
        # Get all required agents at once
        agent_names = list(required_agents.values())
        found_agents = await get_agents_by_name(
            agent_names, 
            print_instructions=(os.getenv("DEBUG_AGENTS", "false").lower() == "true")
        )
        
        # Map found agents to their roles
        for role, agent_name in required_agents.items():
            if agent_name in found_agents:
                self.agents[role] = found_agents[agent_name]
                print(f"✅ {role.title()} agent loaded successfully")
            else:
                print(f"❌ Failed to load {role} agent: {agent_name}")
                # Create placeholder for missing agents
                self.agents[role] = {
                    "name": agent_name,
                    "id": f"placeholder_{role}",
                    "status": "not_found",
                    "instructions": f"Placeholder for {role} functionality"
                }
        
        print(f"\n🎯 Workflow initialized with {len([a for a in self.agents.values() if a.get('status') != 'not_found'])} active agents")
        # return len(self.agents) > 0
        return WorkflowBuilder().set_start_executor(route_request)
        """
        WorkflowBuilder()
                    // add_edge
                    # Routing logic: start with router, then branch to either info or approval workflow
                    .add_edge(route_request, pto_info_executor)  # INFO: route
                    .add_edge(route_request, employee_executor)   # REQUEST: route
                    # Approval workflow chain with human-in-the-loop
                    .add_edge(employee_executor, manager_executor)
                    .add_edge(manager_executor, notifier_executor)
                    .set_start_executor(route_request)  # Start with routing
                    .build()
        """
        

    """
      Method: process_request
      Description: Main entry point for processing user requests from any source and routing to appropriate agents
      Args:
        user_input (str): The user's request text
        source (InputSource): Source of the request (CLI, API, or Teams)
        context (Optional[Dict[str, Any]]): Additional context for the request (defaults to None)
      Returns:
        Dict[str, Any]: Processed result with workflow data, summary, and recommendations
    """
    async def process_request(self, user_input: str, source: InputSource, context: Dict[str, Any] = None) -> Dict[str, Any]:
        print(f"\n📨 Processing request from {source.value}")
        print(f"Input: {user_input[:100]}{'...' if len(user_input) > 100 else ''}")
        
        # Update context
        if context:
            self.context.update(context)
        
        # Analyze input to determine routing strategy
        routing_decision = await self._analyze_input(user_input, source)
        
        # Execute workflow based on routing decision
        result = await self._execute_workflow(user_input, routing_decision, source)
        
        return result

    """
      Method: _analyze_input
      Description: Analyze user input to determine which agents to involve and workflow routing strategy
      Args:
        user_input (str): The user's request text
        source (InputSource): Source of the request for context
      Returns:
        Dict[str, Any]: Routing decision with primary agent, required agents, workflow type, and priority
    """
    async def _analyze_input(self, user_input: str, source: InputSource) -> Dict[str, Any]:
        
        input_lower = user_input.lower()
        
        # Determine intent and required agents
        routing = {
            "primary_agent": "main",
            "required_agents": ["main"],
            "workflow_type": "general",
            "priority": "normal",
            "estimated_complexity": "low"
        }
        
        # Status checking requests
        if any(keyword in input_lower for keyword in ["status", "health", "check", "up", "down", "running"]):
            routing.update({
                "primary_agent": "status_checker",
                "required_agents": ["status_checker", "data_processor"],
                "workflow_type": "status_check",
                "priority": "high" if "critical" in input_lower or "emergency" in input_lower else "normal"
            })
        
        # Issue analysis and solution finding
        elif any(keyword in input_lower for keyword in ["error", "issue", "problem", "failed", "solution", "fix", "troubleshoot"]):
            routing.update({
                "primary_agent": "solution_finder", 
                "required_agents": ["status_checker", "solution_finder", "data_processor"],
                "workflow_type": "problem_solving",
                "priority": "high",
                "estimated_complexity": "high"
            })
        
        # Data processing and reporting
        elif any(keyword in input_lower for keyword in ["report", "analyze", "metrics", "logs", "data", "summary"]):
            routing.update({
                "primary_agent": "data_processor",
                "required_agents": ["data_processor"],
                "workflow_type": "data_analysis", 
                "priority": "normal"
            })
            
        # Monitoring setup or configuration
        elif any(keyword in input_lower for keyword in ["monitor", "alert", "configure", "setup", "rules"]):
            routing.update({
                "primary_agent": "main",
                "required_agents": ["main", "status_checker"],
                "workflow_type": "configuration",
                "priority": "normal"
            })
        
        print(f"🎯 Routing decision: {routing['workflow_type']} -> Primary: {routing['primary_agent']}")
        return routing

    """
      Method: _execute_workflow
      Description: Execute the monitoring workflow based on routing decision and workflow type
      Args:
        user_input (str): The user's request text
        routing (Dict[str, Any]): Routing decision from input analysis
        source (InputSource): Source of the request
      Returns:
        Dict[str, Any]: Workflow execution results with data, summary, and recommendations
    """
    async def _execute_workflow(self, user_input: str, routing: Dict[str, Any], source: InputSource) -> Dict[str, Any]:
        
        workflow_type = routing["workflow_type"]
        results = {
            "workflow_type": workflow_type,
            "timestamp": datetime.now().isoformat(),
            "source": source.value,
            "agents_used": [],
            "data": {},
            "summary": "",
            "recommendations": []
        }
        
        try:
            if workflow_type == "status_check":
                results = await self._handle_status_check(user_input, routing, results)
            elif workflow_type == "problem_solving":
                results = await self._handle_problem_solving(user_input, routing, results)
            elif workflow_type == "data_analysis":
                results = await self._handle_data_analysis(user_input, routing, results)
            elif workflow_type == "configuration":
                results = await self._handle_configuration(user_input, routing, results)
            else:
                results = await self._handle_general_request(user_input, routing, results)
            
        except Exception as e:
            results["error"] = str(e)
            results["summary"] = f"Error processing {workflow_type} request: {e}"
            print(f"❌ Workflow execution error: {e}")
        
        return results

    """
      Method: _handle_status_check
      Description: Handle service status checking workflow including system and service health analysis
      Args:
        user_input (str): The user's request text
        routing (Dict[str, Any]): Routing decision configuration
        results (Dict[str, Any]): Initial results structure to populate
      Returns:
        Dict[str, Any]: Updated results with system status, service health, and recommendations
    """
    async def _handle_status_check(self, user_input: str, routing: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        print("\n🔍 Executing status check workflow...")
        
        # Step 1: Get system status
        system_status = get_system_status()
        results["data"]["system_status"] = system_status
        results["agents_used"].append("status_checker")
        
        # Step 2: Check specific services if mentioned
        services_to_check = self._extract_service_names(user_input)
        if not services_to_check:
            services_to_check = ["web", "api", "database"]  # Default services
        
        service_results = {}
        for service in services_to_check:
            service_health = check_service_health(service)
            service_results[service] = service_health
        
        results["data"]["service_health"] = service_results
        
        # Step 3: Generate summary using data processor agent
        results["agents_used"].append("data_processor")
        
        # Create summary
        healthy_services = [s for s, data in service_results.items() if data.get("healthy", False)]
        unhealthy_services = [s for s, data in service_results.items() if not data.get("healthy", False)]
        
        summary_parts = [
            f"System Status: {system_status['status']}",
            f"Services Checked: {len(service_results)}",
            f"Healthy: {len(healthy_services)}",
            f"Issues: {len(unhealthy_services)}"
        ]
        
        if unhealthy_services:
            summary_parts.append(f"Services with issues: {', '.join(unhealthy_services)}")
            results["recommendations"].extend([
                f"Investigate {service} service immediately" for service in unhealthy_services
            ])
        
        results["summary"] = " | ".join(summary_parts)
        
        return results

    """
      Method: _handle_problem_solving
      Description: Handle problem analysis and solution finding workflow with comprehensive diagnostics
      Args:
        user_input (str): The user's request text
        routing (Dict[str, Any]): Routing decision configuration
        results (Dict[str, Any]): Initial results structure to populate
      Returns:
        Dict[str, Any]: Updated results with problem analysis, log analysis, and solution recommendations
    """
    async def _handle_problem_solving(self, user_input: str, routing: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        print("\n🔧 Executing problem solving workflow...")
        
        results["agents_used"].extend(["status_checker", "solution_finder", "data_processor"])
        
        # Step 1: Get current status to understand the problem scope
        system_status = get_system_status()
        results["data"]["system_status"] = system_status
        
        # Step 2: Analyze logs for errors
        services = self._extract_service_names(user_input) or ["web", "api", "database"]
        log_analysis = {}
        
        for service in services:
            logs = get_service_logs(service, level="error", lines=20)
            log_analysis[service] = logs
        
        results["data"]["log_analysis"] = log_analysis
        
        # Step 3: Check alert rules
        alert_status = {}
        for service in services:
            alerts = check_alert_rules(service)
            alert_status[service] = alerts
        
        results["data"]["alert_status"] = alert_status
        
        # Step 4: Generate solutions and recommendations
        recommendations = []
        
        # Analyze system issues
        if system_status.get("status") != "healthy":
            if system_status.get("system", {}).get("cpu_usage", 0) > 80:
                recommendations.append("High CPU usage detected - consider scaling or optimizing processes")
            if system_status.get("system", {}).get("memory_usage", 0) > 85:
                recommendations.append("High memory usage - investigate memory leaks or scale memory resources")
        
        # Analyze service-specific issues
        for service, logs in log_analysis.items():
            if logs.get("analysis", {}).get("error_count", 0) > 5:
                recommendations.append(f"Multiple errors in {service} - check service configuration and dependencies")
        
        # Analyze triggered alerts
        for service, alerts in alert_status.items():
            if alerts.get("triggered_alerts"):
                for alert in alerts["triggered_alerts"]:
                    recommendations.append(f"{service}: {alert['rule']['metric']} exceeded threshold ({alert['current_value']})")
        
        if not recommendations:
            recommendations.append("No specific issues detected - system appears to be functioning normally")
        
        results["recommendations"] = recommendations
        results["summary"] = f"Problem analysis completed for {len(services)} services. Found {len(recommendations)} recommendations."
        
        return results

    """
      Method: _handle_data_analysis
      Description: Handle data processing and reporting workflow for metrics analysis
      Args:
        user_input (str): The user's request text
        routing (Dict[str, Any]): Routing decision configuration
        results (Dict[str, Any]): Initial results structure to populate
      Returns:
        Dict[str, Any]: Updated results with metrics analysis data and summary reports
    """
    async def _handle_data_analysis(self, user_input: str, routing: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        print("\n📊 Executing data analysis workflow...")
        
        results["agents_used"].append("data_processor")
        
        # Extract what kind of analysis is requested
        input_lower = user_input.lower()
        
        services = self._extract_service_names(user_input) or ["web", "api", "database"]
        analysis_data = {}
        
        # Determine metrics to analyze
        metric_types = []
        if "cpu" in input_lower:
            metric_types.append("cpu")
        if "memory" in input_lower:
            metric_types.append("memory")
        if "response" in input_lower or "latency" in input_lower:
            metric_types.append("response_time")
        if "error" in input_lower:
            metric_types.append("error_rate")
        
        if not metric_types:
            metric_types = ["cpu", "memory", "response_time"]  # Default metrics
        
        # Analyze metrics for each service
        for service in services:
            service_metrics = {}
            for metric_type in metric_types:
                metrics = analyze_metrics(service, metric_type, "1h")
                service_metrics[metric_type] = metrics
            analysis_data[service] = service_metrics
        
        results["data"]["metrics_analysis"] = analysis_data
        
        # Generate summary report
        summary_points = []
        for service, metrics in analysis_data.items():
            for metric_type, data in metrics.items():
                status = data.get("status", "unknown")
                avg_value = data.get("statistics", {}).get("average", 0)
                summary_points.append(f"{service} {metric_type}: {status} (avg: {avg_value:.1f})")
        
        results["summary"] = f"Analyzed {len(metric_types)} metrics across {len(services)} services. " + "; ".join(summary_points[:3])
        
        return results

    """
      Method: _handle_configuration
      Description: Handle monitoring configuration and setup workflow for alerts and rules
      Args:
        user_input (str): The user's request text
        routing (Dict[str, Any]): Routing decision configuration
        results (Dict[str, Any]): Initial results structure to populate
      Returns:
        Dict[str, Any]: Updated results with configuration status and setup recommendations
    """
    async def _handle_configuration(self, user_input: str, routing: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        print("\n⚙️ Executing configuration workflow...")
        
        results["agents_used"].extend(["main", "status_checker"])
        
        # This would typically involve setting up monitoring rules, alerts, etc.
        results["data"]["configuration"] = {
            "monitoring_enabled": True,
            "alert_rules_configured": True,
            "services_monitored": ["web", "api", "database", "cache"]
        }
        
        results["summary"] = "Monitoring configuration updated successfully"
        results["recommendations"] = [
            "Review alert thresholds regularly",
            "Set up notification channels for critical alerts", 
            "Schedule regular health checks"
        ]
        
        return results

    """
      Method: _handle_general_request
      Description: Handle general monitoring requests that don't fit specific workflow categories
      Args:
        user_input (str): The user's request text
        routing (Dict[str, Any]): Routing decision configuration
        results (Dict[str, Any]): Initial results structure to populate
      Returns:
        Dict[str, Any]: Updated results with general information and available commands
    """
    async def _handle_general_request(self, user_input: str, routing: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        print("\n💬 Executing general request workflow...")
        
        results["agents_used"].append("main")
        results["summary"] = "General monitoring information provided"
        results["data"]["available_commands"] = [
            "Check service status", 
            "Analyze metrics",
            "Review logs",
            "Generate reports"
        ]
        
        return results

    """
      Method: _extract_service_names
      Description: Extract service names from user input text by matching against known services
      Args:
        text (str): User input text to analyze for service names
      Returns:
        List[str]: List of recognized service names found in the text
    """
    def _extract_service_names(self, text: str) -> List[str]:
        known_services = ["web", "api", "database", "cache", "auth", "payment", "nginx", "redis", "postgres"]
        text_lower = text.lower()
        
        found_services = []
        for service in known_services:
            if service in text_lower:
                found_services.append(service)
        
        return found_services

    """
      Method: handle_api_request
      Description: Handle requests from API endpoints by extracting query and context
      Args:
        request_data (Dict[str, Any]): API request data containing query and context
      Returns:
        Dict[str, Any]: Processed result from the monitoring workflow
    """
    async def handle_api_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        user_input = request_data.get("query", "")
        context = request_data.get("context", {})
        
        return await self.process_request(user_input, InputSource.API_CALL, context)

    """
      Method: handle_teams_request
      Description: Handle requests from Microsoft Teams integration with Teams-specific context
      Args:
        teams_message (str): Message received from Microsoft Teams
        teams_context (Optional[Dict[str, Any]]): Teams-specific context like channel ID (defaults to None)
      Returns:
        Dict[str, Any]: Processed result from the monitoring workflow
    """
    async def handle_teams_request(self, teams_message: str, teams_context: Dict[str, Any] = None) -> Dict[str, Any]:
        context = teams_context or {}
        context["teams_channel"] = teams_context.get("channel_id", "unknown") if teams_context else "unknown"
        
        return await self.process_request(teams_message, InputSource.TEAMS_INTEGRATION, context)

    """
      Method: handle_cli_request
      Description: Handle requests from command line interface
      Args:
        cli_input (str): Command line input from the user
      Returns:
        Dict[str, Any]: Processed result from the monitoring workflow
    """
    async def handle_cli_request(self, cli_input: str) -> Dict[str, Any]:
        return await self.process_request(cli_input, InputSource.COMMAND_LINE)


# Global workflow instance
workflow = MonitoringWorkflow()


"""
  Method: main
  Description: Main function to demonstrate the monitoring workflow system
  Args:
    None
  Returns:
    None: Runs the interactive monitoring workflow demonstration
"""
async def main():
    global workflow
    
    # Initialize the workflow
    success = await workflow.initialize_agents()
    
    if not success:
        print("❌ Failed to initialize workflow - some agents may be missing")
        return
    
    print("\n🎉 Service Monitoring Workflow Ready!")
    print("\nExample commands you can try:")
    print("  - 'Check the status of all services'")
    print("  - 'Analyze CPU metrics for the web service'") 
    print("  - 'What errors are happening in the API service?'")
    print("  - 'Generate a system health report'")
    
    # Interactive CLI mode
    print("\n" + "="*60)
    print("💬 Interactive Mode - Type 'quit' to exit")
    print("="*60)
    
    while True:
        try:
            user_input = input("\n🔍 Enter monitoring request: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Process the request
            result = await workflow.handle_cli_request(user_input)
            
            # Display results
            print(f"\n📋 Result Summary: {result['summary']}")
            
            if result.get('recommendations'):
                print("\n💡 Recommendations:")
                for i, rec in enumerate(result['recommendations'], 1):
                    print(f"  {i}. {rec}")
            
            if result.get('error'):
                print(f"\n❌ Error: {result['error']}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


# Keep the original test functions for reference
"""
  Method: test_functions
  Description: Original test functions for reference and backward compatibility
  Args:
    None
  Returns:
    None: Contains commented test code for agent retrieval functionality
"""
async def test_functions():
    
    # Test 1: Get list of all agents
    # print("\n1️⃣ Retrieving all agents from project...")
    # agent_list = await get_agent_list()
    
    # if agent_list:
    #     print(f"\n📋 Available Agents in Project ({len(agent_list)}):")
    #     for i, agent in enumerate(agent_list, 1):
    #         print(f"  {i}. {agent['name']} (ID: {agent['id']})")
    #         print(f"     Description: {agent['description']}")
    #         print(f"     Model: {agent.get('model', 'N/A')}")
    #         print()
    # else:
    #     print("\n❌ Could not retrieve agent list")
    #     return
    
    
 
    # Test 2: Get specific agent by name
    # print("\n2️⃣ Searching for specific agent by name...")
    # agent_name = "JET-Service-Ninja-Agent"

    # specific_agent = await get_agent_by_name(agent_name)
    
    # if specific_agent:
    #     print(f"\n✅ Found specific agent:")
    #     print(f"  Name: {specific_agent['name']}")
    #     print(f"  ID: {specific_agent['id']}")
    #     print(f"  Description: {specific_agent['description']}")
    #     print(f"  Instructions: {specific_agent['instructions']}")
    # else:
    #     print(f"\n❌ Could not find agent named: {agent_name}")
    
    # Test 3: Get agent by ID (using first agent from list)
    # if agent_list:
    #     print("\n3️⃣ Testing agent retrieval by ID...")
    #     first_agent_id = agent_list[0]['id']
    #     agent_by_id = await get_agent_by_id(first_agent_id)
        
    #     if agent_by_id:
    #         print(f"✅ Retrieved agent by ID: {agent_by_id['name']}")
    #     else:
    #         print(f"❌ Could not retrieve agent by ID: {first_agent_id}")
    
    pass


if __name__ == "__main__":
    asyncio.run(main())