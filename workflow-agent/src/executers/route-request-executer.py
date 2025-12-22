from agent_framework import (
    WorkflowContext,
    executor,
)

@executor(id="routing_executor")
async def route_request(message: str, ctx: WorkflowContext[str]) -> None:
    """Route the request to either PTO info agent or approval workflow."""
    
    # Debug: Inspect context for authentication information
    print("\n=== Context Authentication Check ===")
    
    # Check request_info method
    try:
        request_info = ctx.request_info()
        print(f"✅ request_info(): {type(request_info)}")
        print(f"   Content: {request_info}")
        
        # If request_info returns an object, examine it for auth info
        if request_info and hasattr(request_info, '__dict__'):
            print("   🔍 Examining request_info attributes:")
            for key, value in request_info.__dict__.items():
                print(f"     {key}: {value}")
                if any(auth_term in key.lower() for auth_term in ['auth', 'token', 'user', 'credential', 'bearer']):
                    print(f"     🔑 AUTH FOUND - {key}: {value}")
        
        # If request_info is dict-like
        elif isinstance(request_info, dict):
            print("   🔍 Examining request_info dictionary:")
            for key, value in request_info.items():
                print(f"     {key}: {value}")
                if any(auth_term in str(key).lower() for auth_term in ['auth', 'token', 'user', 'credential', 'bearer']):
                    print(f"     🔑 AUTH FOUND - {key}: {value}")
                    
    except Exception as e:
        print(f"❌ Error accessing request_info(): {e}")
    
    # Check if there are any source executor IDs that might contain user info
    try:
        source_ids = ctx.source_executor_ids
        print(f"📋 source_executor_ids: {source_ids}")
    except Exception as e:
        print(f"❌ Error accessing source_executor_ids: {e}")
    
    # Check other context properties
    try:
        shared_state_keys = []
        # Since get_shared_state needs a key, let's see if there's a way to list keys
        print("📦 shared_state: (method requires key)")
    except Exception as e:
        print(f"❌ Error with shared_state: {e}")
    
    print("=== End Auth Check ===\n")
    
    # Simple routing logic based on keywords
    question_keywords = [
        "how much", "how many", "what is", "when can", "policy", "rules", 
        "balance", "accrual", "rollover", "maximum", "minimum", "eligibility",
        "sick leave", "vacation", "holiday", "bereavement", "maternity", "paternity",
        "explain", "tell me", "what are", "info", "information"
    ]
    
    request_keywords = [
        "request", "apply for", "take time off", "need time", "want to take", 
        "schedule", "book", "reserve", "submit", "approve", "time off"
    ]
    
    message_lower = message.lower()
    
    # Check if this is a question about PTO policies/info
    is_question = any(keyword in message_lower for keyword in question_keywords)
    is_request = any(keyword in message_lower for keyword in request_keywords)
    
    if is_question and not is_request:
        # Route to PTO info agent - don't print routing info
        await ctx.send_message(f"INFO:{message}")
    else:
        # Route to approval workflow - don't print routing info  
        await ctx.send_message(f"REQUEST:{message}")