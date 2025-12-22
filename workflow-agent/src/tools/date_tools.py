"""
Date calculation tools for PTO workflow agents.
Provides functions for calculating dates, handling relative date expressions,
and working with business days and holidays.
"""

from datetime import datetime, timedelta, date
from typing import Optional, List, Dict, Any
import calendar


"""
  Method: get_current_date
  Description: Get the current date and time information
  Args:
    None
  Returns:
    Dict[str, Any]: Current date information including formatted strings, day of week, etc.
"""
def get_current_date() -> Dict[str, Any]:
    now = datetime.now()
    return {
        "current_date": now.strftime("%Y-%m-%d"),
        "current_time": now.strftime("%H:%M:%S"),
        "current_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "day_of_week": now.strftime("%A"),
        "month_name": now.strftime("%B"),
        "year": now.year,
        "iso_week": now.isocalendar()[1],
        "day_of_year": now.timetuple().tm_yday
    }

"""
  Method: calculate_relative_date
  Description: Calculate a date based on relative expressions like 'next Thursday', 'in 2 weeks', etc
  Args:
    relative_expression (str): Natural language date expression
    reference_date (Optional[str]): Reference date in YYYY-MM-DD format (defaults to today)
  Returns:
    Dict[str, Any]: Calculated date information with formatted strings and metadata
"""
def calculate_relative_date(relative_expression: str, reference_date: Optional[str] = None) -> Dict[str, Any]:
    if reference_date:
        ref_date = datetime.strptime(reference_date, "%Y-%m-%d").date()
    else:
        ref_date = date.today()
    
    expression = relative_expression.lower().strip()
    
    # Handle "today", "tomorrow", "yesterday"
    if expression == "today":
        target_date = ref_date
    elif expression == "tomorrow":
        target_date = ref_date + timedelta(days=1)
    elif expression == "yesterday":
        target_date = ref_date - timedelta(days=1)
    
    # Handle "next [day of week]"
    elif expression.startswith("next "):
        day_name = expression[5:]
        target_date = get_next_weekday(ref_date, day_name)
    
    # Handle "this [day of week]" 
    elif expression.startswith("this "):
        day_name = expression[5:]
        target_date = get_this_weekday(ref_date, day_name)
    
    # Handle "in X days/weeks/months"
    elif expression.startswith("in "):
        target_date = parse_in_expression(expression, ref_date)
    
    # Handle "X days/weeks ago"
    elif " ago" in expression:
        target_date = parse_ago_expression(expression, ref_date)
    
    else:
        # Try to parse as a specific date
        target_date = parse_specific_date(expression, ref_date)
    
    return {
        "target_date": target_date.strftime("%Y-%m-%d"),
        "day_of_week": target_date.strftime("%A"),
        "formatted_date": target_date.strftime("%B %d, %Y"),
        "days_from_today": (target_date - date.today()).days,
        "is_weekend": target_date.weekday() >= 5,
        "is_business_day": target_date.weekday() < 5
    }

"""
  Method: get_next_weekday
  Description: Get the next occurrence of a specific weekday
  Args:
    ref_date (date): Reference date to calculate from
    day_name (str): Name of the weekday (e.g., 'monday', 'tuesday')
  Returns:
    date: Date of the next occurrence of the specified weekday
"""
def get_next_weekday(ref_date: date, day_name: str) -> date:
    weekdays = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }
    
    if day_name not in weekdays:
        raise ValueError(f"Invalid day name: {day_name}")
    
    target_weekday = weekdays[day_name]
    current_weekday = ref_date.weekday()
    
    # Calculate days until next occurrence
    days_ahead = (target_weekday - current_weekday) % 7
    if days_ahead == 0:  # If it's the same day, get next week
        days_ahead = 7
    
    return ref_date + timedelta(days=days_ahead)

"""
  Method: get_this_weekday
  Description: Get the occurrence of a specific weekday in the current week
  Args:
    ref_date (date): Reference date to calculate from
    day_name (str): Name of the weekday (e.g., 'monday', 'tuesday')
  Returns:
    date: Date of the specified weekday in the current week
"""
def get_this_weekday(ref_date: date, day_name: str) -> date:
    weekdays = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }
    
    if day_name not in weekdays:
        raise ValueError(f"Invalid day name: {day_name}")
    
    target_weekday = weekdays[day_name]
    current_weekday = ref_date.weekday()
    
    days_diff = target_weekday - current_weekday
    return ref_date + timedelta(days=days_diff)

"""
  Method: parse_in_expression
  Description: Parse expressions like 'in 3 days', 'in 2 weeks', 'in 1 month'
  Args:
    expression (str): Time expression to parse (e.g., 'in 3 days')
    ref_date (date): Reference date to calculate from
  Returns:
    date: Calculated date based on the expression
"""
def parse_in_expression(expression: str, ref_date: date) -> date:
    parts = expression.split()
    if len(parts) < 3:
        raise ValueError(f"Invalid expression: {expression}")
    
    try:
        number = int(parts[1])
        unit = parts[2].lower()
        
        if unit.startswith('day'):
            return ref_date + timedelta(days=number)
        elif unit.startswith('week'):
            return ref_date + timedelta(weeks=number)
        elif unit.startswith('month'):
            # Approximate month calculation
            return ref_date + timedelta(days=number * 30)
        else:
            raise ValueError(f"Unknown time unit: {unit}")
    except (ValueError, IndexError):
        raise ValueError(f"Could not parse expression: {expression}")

"""
  Method: parse_ago_expression
  Description: Parse expressions like '3 days ago', '2 weeks ago'
  Args:
    expression (str): Time expression to parse (e.g., '3 days ago')
    ref_date (date): Reference date to calculate from
  Returns:
    date: Calculated date based on the expression
"""
def parse_ago_expression(expression: str, ref_date: date) -> date:
    parts = expression.replace(" ago", "").split()
    if len(parts) < 2:
        raise ValueError(f"Invalid expression: {expression}")
    
    try:
        number = int(parts[0])
        unit = parts[1].lower()
        
        if unit.startswith('day'):
            return ref_date - timedelta(days=number)
        elif unit.startswith('week'):
            return ref_date - timedelta(weeks=number)
        elif unit.startswith('month'):
            return ref_date - timedelta(days=number * 30)
        else:
            raise ValueError(f"Unknown time unit: {unit}")
    except (ValueError, IndexError):
        raise ValueError(f"Could not parse expression: {expression}")

"""
  Method: parse_specific_date
  Description: Parse specific date expressions like 'December 25', 'Dec 25'
  Args:
    expression (str): Date expression to parse (e.g., 'December 25')
    ref_date (date): Reference date for year context
  Returns:
    date: Parsed date or reference date if parsing fails
"""
def parse_specific_date(expression: str, ref_date: date) -> date:
    # This is a simplified parser - you could expand it for more formats
    current_year = ref_date.year
    
    # Try common date formats
    formats_to_try = [
        "%B %d",      # December 25
        "%b %d",      # Dec 25
        "%m/%d",      # 12/25
        "%m-%d",      # 12-25
    ]
    
    for fmt in formats_to_try:
        try:
            parsed_date = datetime.strptime(expression, fmt).date()
            # Add current year
            return parsed_date.replace(year=current_year)
        except ValueError:
            continue
    
    # If no format worked, default to today
    return ref_date

"""
  Method: get_business_days_between
  Description: Calculate business days between two dates
  Args:
    start_date (str): Start date in YYYY-MM-DD format
    end_date (str): End date in YYYY-MM-DD format
    exclude_holidays (bool): Whether to exclude common holidays (defaults to True)
  Returns:
    Dict[str, Any]: Business day calculation results including count and date range
"""
def get_business_days_between(start_date: str, end_date: str, exclude_holidays: bool = True) -> Dict[str, Any]:
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    if start > end:
        start, end = end, start
    
    business_days = 0
    current_date = start
    
    while current_date <= end:
        # Check if it's a weekday (Monday = 0, Sunday = 6)
        if current_date.weekday() < 5:
            if exclude_holidays and not is_holiday(current_date):
                business_days += 1
            elif not exclude_holidays:
                business_days += 1
        current_date += timedelta(days=1)
    
    return {
        "business_days": business_days,
        "total_days": (end - start).days + 1,
        "weekend_days": (end - start).days + 1 - business_days,
        "start_date": start_date,
        "end_date": end_date
    }

"""
  Method: is_holiday
  Description: Check if a date is a common US holiday
  Args:
    check_date (date): Date to check for holiday status
  Returns:
    bool: True if the date is a recognized holiday, False otherwise
"""
def is_holiday(check_date: date) -> bool:
    year = check_date.year
    
    # Common US holidays (simplified)
    holidays = [
        date(year, 1, 1),   # New Year's Day
        date(year, 7, 4),   # Independence Day
        date(year, 12, 25), # Christmas Day
    ]
    
    # Add Labor Day (first Monday in September)
    labor_day = get_first_monday_of_month(year, 9)
    holidays.append(labor_day)
    
    # Add Thanksgiving (fourth Thursday in November)
    thanksgiving = get_fourth_thursday_of_month(year, 11)
    holidays.append(thanksgiving)
    
    return check_date in holidays

"""
  Method: get_first_monday_of_month
  Description: Get the first Monday of a given month
  Args:
    year (int): Year of the target month
    month (int): Month number (1-12)
  Returns:
    date: Date of the first Monday in the specified month
"""
def get_first_monday_of_month(year: int, month: int) -> date:
    first_day = date(year, month, 1)
    days_until_monday = (7 - first_day.weekday()) % 7
    return first_day + timedelta(days=days_until_monday)

"""
  Method: get_fourth_thursday_of_month
  Description: Get the fourth Thursday of a given month
  Args:
    year (int): Year of the target month
    month (int): Month number (1-12)
  Returns:
    date: Date of the fourth Thursday in the specified month
"""
def get_fourth_thursday_of_month(year: int, month: int) -> date:
    first_day = date(year, month, 1)
    first_thursday = first_day + timedelta(days=(3 - first_day.weekday()) % 7)
    return first_thursday + timedelta(days=21)  # Add 3 weeks

"""
  Method: format_date_range
  Description: Format a date range in various human-readable formats
  Args:
    start_date (str): Start date in YYYY-MM-DD format
    end_date (str): End date in YYYY-MM-DD format
  Returns:
    Dict[str, str]: Various formatted representations of the date range
"""
def format_date_range(start_date: str, end_date: str) -> Dict[str, str]:
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    return {
        "short_format": f"{start.strftime('%m/%d')} - {end.strftime('%m/%d/%Y')}",
        "medium_format": f"{start.strftime('%b %d')} - {end.strftime('%b %d, %Y')}",
        "long_format": f"{start.strftime('%B %d')} - {end.strftime('%B %d, %Y')}",
        "duration_days": (end - start).days + 1,
        "duration_text": get_duration_text((end - start).days + 1)
    }

"""
  Method: get_duration_text
  Description: Convert number of days to human-readable duration
  Args:
    days (int): Number of days to convert
  Returns:
    str: Human-readable duration text (e.g., '1 week', '2 months and 3 days')
"""
def get_duration_text(days: int) -> str:
    if days == 1:
        return "1 day"
    elif days < 7:
        return f"{days} days"
    elif days == 7:
        return "1 week"
    elif days < 30:
        weeks = days // 7
        remaining_days = days % 7
        if remaining_days == 0:
            return f"{weeks} weeks"
        else:
            return f"{weeks} weeks and {remaining_days} days"
    else:
        months = days // 30
        remaining_days = days % 30
        if remaining_days == 0:
            return f"{months} months"
        else:
            return f"{months} months and {remaining_days} days"


# Tool definitions for the agent framework
DATE_TOOLS = [
    {
        "name": "get_current_date",
        "description": "Get the current date and time information",
        "function": get_current_date
    },
    {
        "name": "calculate_relative_date", 
        "description": "Calculate dates from relative expressions like 'next Friday', 'tomorrow', 'in 2 weeks'",
        "function": calculate_relative_date
    },
    {
        "name": "get_business_days_between",
        "description": "Calculate business days between two dates",
        "function": get_business_days_between
    },
    {
        "name": "format_date_range",
        "description": "Format date ranges in human-readable formats",
        "function": format_date_range
    }
]