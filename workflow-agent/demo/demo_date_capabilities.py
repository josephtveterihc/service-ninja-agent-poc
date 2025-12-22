#!/usr/bin/env python3
"""
Demo showing how date tools work with relative date expressions.
This simulates what the agents will be able to do.
"""

import sys
import os
# Add the src directory to the path so we can import date_tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.tools.date_tools import get_current_date, calculate_relative_date

def demo_date_capabilities():
    """Demonstrate how agents can handle relative dates."""
    
    print("🤖 AI Agent Date Capabilities Demo")
    print("="*50)
    
    # Get current date context
    current = get_current_date()
    print(f"📅 Current Date: {current['current_date']} ({current['day_of_week']})")
    print()
    
    # Example user requests with relative dates
    user_requests = [
        "I want to take vacation next Thursday",
        "Can I request time off next Friday?", 
        "I need 3 days off starting tomorrow",
        "I'd like to schedule PTO for next Monday and Tuesday",
        "Can I take time off in 2 weeks?",
        "I want to request vacation this Friday"
    ]
    
    print("🗣️  Sample User Requests and AI Responses:")
    print("-" * 50)
    
    for request in user_requests:
        print(f"\n👤 User: \"{request}\"")
        
        # Extract date expressions (simplified - real AI would be smarter)
        relative_dates = []
        if "next thursday" in request.lower():
            relative_dates.append("next Thursday")
        elif "next friday" in request.lower():
            relative_dates.append("next Friday")
        elif "tomorrow" in request.lower():
            relative_dates.append("tomorrow")
        elif "next monday" in request.lower():
            relative_dates.append("next Monday")
        elif "in 2 weeks" in request.lower():
            relative_dates.append("in 2 weeks")
        elif "this friday" in request.lower():
            relative_dates.append("this Friday")
        
        # Calculate specific dates
        if relative_dates:
            for rel_date in relative_dates:
                result = calculate_relative_date(rel_date)
                specific_date = result['target_date']
                day_name = result['day_of_week']
                days_away = result['days_from_today']
                
                print(f"🤖 AI Agent: I understand you want time off on {rel_date}.")
                print(f"    That would be {specific_date} ({day_name}), which is {days_away} days from today.")
                
                if result['is_weekend']:
                    print(f"    ⚠️  Note: This falls on a weekend.")
                elif result['is_business_day']:
                    print(f"    ✅ This is a business day.")
        else:
            print(f"🤖 AI Agent: I can help with your time-off request. Please specify the exact dates.")
    
    print(f"\n" + "="*50)
    print("✨ Key Benefits:")
    print("  • Converts 'next Friday' to specific dates (2025-12-12)")
    print("  • Validates business days vs weekends")
    print("  • Calculates advance notice periods")
    print("  • Handles complex date expressions automatically")
    print("  • Always uses current date for accurate calculations")

if __name__ == "__main__":
    demo_date_capabilities()