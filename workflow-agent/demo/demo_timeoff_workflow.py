"""
Demo version of the time-off workflow that doesn't require Azure credentials.
This shows how the workflow structure works without needing actual API calls.
"""

from agent_framework import (
    ChatMessage,
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    WorkflowOutputEvent,
    handler,
)
import asyncio
import os
from typing_extensions import Never

def load_agent_instructions(agent_name: str) -> str:
    """Load agent instructions from external file."""
    # Get the directory containing this file (demo)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root, then into src/agent_instructions
    project_root = os.path.dirname(current_dir)
    instructions_dir = os.path.join(project_root, "src", "agent_instructions")
    instructions_file = os.path.join(instructions_dir, f"{agent_name}_agent_instructions.md")
    
    try:
        with open(instructions_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️  Warning: Could not find instructions file {instructions_file}")
        return f"You are a {agent_name} agent in a PTO workflow system."

class MockEmployeeExecutor(Executor):
    """Mock employee executor that simulates HR assistant behavior."""
    
    def __init__(self, id="employee"):
        super().__init__(id=id)

    @handler
    async def request_time_off(self, message: str, ctx: WorkflowContext[list[ChatMessage]]) -> None:
        """Process time-off request and forward conversation to manager."""
        
        # Simulate employee's formatted request
        mock_response = f"""
TIME-OFF REQUEST FORM

Employee: John Smith
Request Type: Paid Time Off
Dates Requested: Next Friday (December 13, 2025)
Reason: Family event - extending weekend
Duration: 1 day
Total PTO Balance: 15 days available

Original Request: "{message}"

This request has been properly formatted and submitted for manager review.
        """.strip()
        
        print(f"🧑‍💼 Employee Request: {mock_response}")
        
        # Create conversation messages
        messages = [
            ChatMessage(role="user", text=message),
            ChatMessage(role="assistant", text=mock_response)
        ]
        
        await ctx.send_message(messages)

class MockManagerExecutor(Executor):
    """Mock manager executor that simulates approval/denial decisions."""
    
    def __init__(self, id="manager"):
        super().__init__(id=id)

    @handler
    async def approve_request(self, messages: list[ChatMessage], ctx: WorkflowContext[list[ChatMessage]]) -> None:
        """Review request and make approval decision."""
        
        mock_decision = """
MANAGEMENT REVIEW DECISION

Request Status: APPROVED ✅

Review Comments:
- Request submitted with adequate advance notice
- Employee has sufficient PTO balance (15 days available)
- Department coverage is adequate for the requested date
- Reason is appropriate for PTO usage

Approval Details:
- Approved by: Manager Sarah Johnson
- Date Reviewed: December 8, 2025
- Effective Date: December 13, 2025

Next Steps: Employee will receive official notification via email.
        """.strip()
        
        print(f"👔 Manager Decision: {mock_decision}")
        
        # Add manager's decision to the conversation
        decision_message = ChatMessage(role="assistant", text=mock_decision)
        messages.append(decision_message)
        
        await ctx.send_message(messages)

class MockNotificationExecutor(Executor):
    """Mock notification executor that generates employee notifications."""
    
    def __init__(self, id="notifier"):
        super().__init__(id=id)

    @handler
    async def notify_employee(self, messages: list[ChatMessage], ctx: WorkflowContext[Never, str]) -> None:
        """Generate and send notification to employee based on manager's decision."""
        
        final_notification = """
📧 TIME-OFF REQUEST NOTIFICATION

Dear John Smith,

Your time-off request has been processed with the following outcome:

✅ REQUEST APPROVED

Details:
• Date Requested: Friday, December 13, 2025
• Type: Paid Time Off (PTO)
• Duration: 1 day
• Remaining PTO Balance: 14 days (after this request)

Your manager, Sarah Johnson, has approved your request. Please ensure any pending work is completed or delegated before your time off.

If you have any questions, please contact HR or your direct supervisor.

Best regards,
HR Department
        """.strip()
        
        await ctx.yield_output(final_notification)

async def main():
    """Main function that creates mock agents and runs the workflow."""
    print("🚀 Starting Mock Time-Off Request Workflow")
    print("=" * 50)
    
    # Create executor instances
    employee_executor = MockEmployeeExecutor()
    manager_executor = MockManagerExecutor()
    notifier_executor = MockNotificationExecutor()

    # Build the workflow with proper edge connections
    workflow = (
        WorkflowBuilder()
        .add_edge(employee_executor, manager_executor)
        .add_edge(manager_executor, notifier_executor)
        .set_start_executor(employee_executor)
        .build()
    )

    # Run the workflow with streaming to observe events
    print("\n📝 Processing Request...")
    print("-" * 30)
    
    async for event in workflow.run_stream("I want to apply for paid time off next Friday to extend my weekend for a family event."):
        if isinstance(event, WorkflowOutputEvent):
            print(f"\n📧 Final Notification:")
            print("=" * 50)
            print(event.data)
            break

    print("\n✅ Workflow completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())