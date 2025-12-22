#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for date calculation tools
"""

import sys
import os
# Add the src directory to the path so we can import date_tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.tools.date_tools import (
    get_current_date,
    calculate_relative_date,
    get_business_days_between,
    format_date_range
)

def test_date_tools():
    """Test various date calculation functions."""
    
    print("Date Tools Test")
    print("="*50)
    
    # Test current date
    print("\n1. Current Date Information:")
    current = get_current_date()
    print(f"   Today: {current['current_date']} ({current['day_of_week']})")
    print(f"   Time: {current['current_time']}")
    
    # Test relative date calculations
    print("\n2. Relative Date Calculations:")
    test_expressions = [
        "tomorrow",
        "next Friday",
        "next Monday", 
        "in 2 weeks",
        "in 5 days",
        "this Thursday"
    ]
    
    for expr in test_expressions:
        try:
            result = calculate_relative_date(expr)
            print(f"   '{expr}' → {result['target_date']} ({result['day_of_week']})")
            print(f"      Days from today: {result['days_from_today']}")
        except Exception as e:
            print(f"   '{expr}' → Error: {e}")
    
    # Test business days calculation
    print("\n3. Business Days Calculation:")
    try:
        result = get_business_days_between("2025-12-09", "2025-12-20")
        print(f"   Dec 9-20, 2025: {result['business_days']} business days")
        print(f"   Total days: {result['total_days']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test date range formatting
    print("\n4. Date Range Formatting:")
    try:
        result = format_date_range("2025-12-09", "2025-12-13")
        print(f"   Short: {result['short_format']}")
        print(f"   Medium: {result['medium_format']}")
        print(f"   Duration: {result['duration_text']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n✅ Date tools test completed!")

if __name__ == "__main__":
    test_date_tools()