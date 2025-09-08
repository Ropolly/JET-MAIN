"""
Timezone utilities for handling airport-specific time conversions.

This module provides functions to convert between local airport times and UTC,
properly handling daylight saving time transitions using IANA timezone identifiers.
"""

import pytz
from datetime import datetime, timezone
from typing import Optional, Tuple
from django.utils import timezone as django_timezone


def convert_local_to_utc(local_datetime: datetime, airport_timezone: str) -> datetime:
    """
    Convert a local datetime to UTC using the airport's timezone.
    
    Args:
        local_datetime: Datetime in the airport's local time (naive or aware)
        airport_timezone: IANA timezone identifier (e.g., 'America/New_York')
    
    Returns:
        UTC datetime with timezone info
    
    Raises:
        pytz.exceptions.UnknownTimeZoneError: If timezone is invalid
        pytz.exceptions.AmbiguousTimeError: For ambiguous DST transition times
        pytz.exceptions.NonExistentTimeError: For non-existent DST transition times
    """
    if not airport_timezone:
        raise ValueError("Airport timezone is required")
    
    # Get the timezone object
    tz = pytz.timezone(airport_timezone)
    
    # If datetime already has timezone info, convert directly to UTC
    if local_datetime.tzinfo is not None:
        # If it's already in UTC, return as is
        if local_datetime.tzinfo == pytz.UTC:
            return local_datetime
        # Otherwise, convert to UTC
        return local_datetime.astimezone(pytz.UTC)
    
    # Localize the naive datetime to the airport's timezone
    # This handles DST transitions automatically
    try:
        localized_dt = tz.localize(local_datetime, is_dst=None)
    except pytz.exceptions.AmbiguousTimeError:
        # During "fall back" DST transition, choose the first occurrence (before DST ends)
        localized_dt = tz.localize(local_datetime, is_dst=True)
    except pytz.exceptions.NonExistentTimeError:
        # During "spring forward" DST transition, move to the next valid time
        localized_dt = tz.localize(local_datetime, is_dst=False)
    
    # Convert to UTC
    return localized_dt.astimezone(pytz.UTC)


def convert_utc_to_local(utc_datetime: datetime, airport_timezone: str) -> datetime:
    """
    Convert a UTC datetime to local airport time.
    
    Args:
        utc_datetime: UTC datetime (with or without timezone info)
        airport_timezone: IANA timezone identifier (e.g., 'America/New_York')
    
    Returns:
        Naive datetime in the airport's local time
    
    Raises:
        pytz.exceptions.UnknownTimeZoneError: If timezone is invalid
    """
    if not airport_timezone:
        raise ValueError("Airport timezone is required")
    
    # Ensure UTC datetime is timezone-aware
    if utc_datetime.tzinfo is None:
        utc_datetime = utc_datetime.replace(tzinfo=pytz.UTC)
    elif utc_datetime.tzinfo != pytz.UTC:
        utc_datetime = utc_datetime.astimezone(pytz.UTC)
    
    # Get the timezone object and convert
    tz = pytz.timezone(airport_timezone)
    local_dt = utc_datetime.astimezone(tz)
    
    # Return naive datetime in local time
    return local_dt.replace(tzinfo=None)


def get_timezone_info(airport_timezone: str, dt: Optional[datetime] = None) -> dict:
    """
    Get timezone information for an airport at a specific datetime.
    
    Args:
        airport_timezone: IANA timezone identifier
        dt: Datetime to check (defaults to current time)
    
    Returns:
        Dict with timezone info: {
            'timezone': 'America/New_York',
            'abbreviation': 'EST' or 'EDT',
            'utc_offset': '-05:00',
            'is_dst': True/False,
            'dst_transition_next': datetime or None
        }
    """
    if not airport_timezone:
        raise ValueError("Airport timezone is required")
    
    if dt is None:
        dt = django_timezone.now()
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.UTC)
    
    tz = pytz.timezone(airport_timezone)
    localized_dt = dt.astimezone(tz)
    
    # Get timezone info
    tzinfo = {
        'timezone': airport_timezone,
        'abbreviation': localized_dt.strftime('%Z'),
        'utc_offset': localized_dt.strftime('%z'),
        'is_dst': bool(localized_dt.dst()),
    }
    
    # Find next DST transition (useful for warnings)
    try:
        # Use a safer approach to get DST transitions
        next_transition = None
        
        # Check if timezone has _utc_transition_times and it's iterable
        if hasattr(tz, '_utc_transition_times') and hasattr(tz._utc_transition_times, '__iter__'):
            try:
                # Get transitions for the current year and next year
                current_year = localized_dt.year
                transitions = []
                
                # Safely iterate through transition times
                transition_times = tz._utc_transition_times
                # Handle different pytz versions - some return tuples, some just datetimes
                for transition_item in transition_times:
                    if isinstance(transition_item, tuple) and len(transition_item) >= 3:
                        transition_dt, before_tz, after_tz = transition_item
                    elif hasattr(transition_item, 'year'):  # It's a datetime
                        transition_dt = transition_item
                    else:
                        continue
                        
                    if (hasattr(transition_dt, 'year') and 
                        transition_dt.year in [current_year, current_year + 1] and 
                        transition_dt > dt):
                        transitions.append(transition_dt)
                        
                next_transition = min(transitions) if transitions else None
            except (TypeError, ValueError, AttributeError):
                pass
        
        tzinfo['dst_transition_next'] = next_transition
    except Exception:
        # Fallback - don't include DST transition info if we can't determine it safely
        tzinfo['dst_transition_next'] = None
    
    return tzinfo


def validate_time_consistency(departure_local: datetime, departure_utc: datetime, 
                             departure_timezone: str) -> bool:
    """
    Validate that local and UTC times are consistent for a given timezone.
    
    Args:
        departure_local: Local departure time (naive or aware)
        departure_utc: UTC departure time (with timezone info)
        departure_timezone: IANA timezone identifier
    
    Returns:
        True if times are consistent, False otherwise
    """
    try:
        # Convert local to UTC and compare
        calculated_utc = convert_local_to_utc(departure_local, departure_timezone)
        
        # Ensure both datetimes are timezone-aware for comparison
        if departure_utc.tzinfo is None:
            departure_utc = departure_utc.replace(tzinfo=pytz.UTC)
        elif departure_utc.tzinfo != pytz.UTC:
            departure_utc = departure_utc.astimezone(pytz.UTC)
        
        # Allow for small differences (up to 1 second) due to rounding
        time_diff = abs((calculated_utc - departure_utc).total_seconds())
        return time_diff <= 1.0
        
    except Exception:
        return False


def calculate_flight_duration_with_timezones(
    departure_local: datetime, departure_timezone: str,
    arrival_local: datetime, arrival_timezone: str
) -> Tuple[float, dict]:
    """
    Calculate flight duration accounting for timezone differences.
    
    Args:
        departure_local: Local departure time (naive)
        departure_timezone: Departure airport timezone
        arrival_local: Local arrival time (naive)
        arrival_timezone: Arrival airport timezone
    
    Returns:
        Tuple of (duration_hours, info_dict)
        info_dict contains UTC times and timezone info
    """
    # Convert both times to UTC
    departure_utc = convert_local_to_utc(departure_local, departure_timezone)
    arrival_utc = convert_local_to_utc(arrival_local, arrival_timezone)
    
    # Calculate actual flight duration
    duration_seconds = (arrival_utc - departure_utc).total_seconds()
    duration_hours = duration_seconds / 3600.0
    
    # Prepare info
    info = {
        'departure_utc': departure_utc,
        'arrival_utc': arrival_utc,
        'departure_tz_info': get_timezone_info(departure_timezone, departure_utc),
        'arrival_tz_info': get_timezone_info(arrival_timezone, arrival_utc),
        'duration_seconds': duration_seconds,
        'duration_hours': duration_hours,
        'crosses_date_line': arrival_local.date() != departure_local.date(),
        'timezone_difference_hours': (
            arrival_utc.utcoffset().total_seconds() - departure_utc.utcoffset().total_seconds()
        ) / 3600.0 if arrival_utc.utcoffset() and departure_utc.utcoffset() else 0
    }
    
    return duration_hours, info


def format_time_with_timezone(dt: datetime, timezone_str: str, 
                              include_utc: bool = False) -> str:
    """
    Format a datetime with timezone information for display.
    
    Args:
        dt: Datetime to format (UTC or naive)
        timezone_str: Target timezone for display
        include_utc: Whether to include UTC time in parentheses
    
    Returns:
        Formatted string like "14:30 EST (19:30 UTC)" or "14:30 EST"
    """
    if not timezone_str:
        return dt.strftime('%H:%M')
    
    try:
        if dt.tzinfo is None:
            # Assume it's already in the target timezone
            local_dt = dt
            tz_info = get_timezone_info(timezone_str, 
                                       convert_local_to_utc(dt, timezone_str))
        else:
            # Convert to target timezone
            local_dt = convert_utc_to_local(dt, timezone_str)
            tz_info = get_timezone_info(timezone_str, dt)
        
        formatted = f"{local_dt.strftime('%H:%M')} {tz_info['abbreviation']}"
        
        if include_utc and dt.tzinfo:
            utc_dt = dt.astimezone(pytz.UTC) if dt.tzinfo != pytz.UTC else dt
            formatted += f" ({utc_dt.strftime('%H:%M')} UTC)"
        
        return formatted
        
    except Exception:
        return dt.strftime('%H:%M')


def check_dst_transition_warning(local_dt: datetime, timezone_str: str) -> Optional[dict]:
    """
    Check if a datetime is near a DST transition and return warning info.
    
    Args:
        local_dt: Local datetime to check
        timezone_str: IANA timezone identifier
    
    Returns:
        Dict with warning info or None if no issues
    """
    try:
        tz = pytz.timezone(timezone_str)
        
        # Check if the time is ambiguous (during "fall back")
        try:
            tz.localize(local_dt, is_dst=None)
        except pytz.exceptions.AmbiguousTimeError:
            return {
                'type': 'ambiguous',
                'message': 'This time occurs twice due to daylight saving transition. Using the first occurrence.',
                'suggestion': 'Consider specifying a different time to avoid confusion.'
            }
        except pytz.exceptions.NonExistentTimeError:
            return {
                'type': 'non_existent',
                'message': 'This time does not exist due to daylight saving transition.',
                'suggestion': 'Please choose a time after the DST transition.'
            }
        
        # Check if near a DST transition (within 24 hours)
        tz_info = get_timezone_info(timezone_str, 
                                   convert_local_to_utc(local_dt, timezone_str))
        
        if tz_info.get('dst_transition_next'):
            next_transition = tz_info['dst_transition_next']
            hours_until_transition = (next_transition - convert_local_to_utc(local_dt, timezone_str)).total_seconds() / 3600
            
            if 0 < hours_until_transition <= 24:
                return {
                    'type': 'near_transition',
                    'message': f'DST transition occurs in {hours_until_transition:.1f} hours.',
                    'suggestion': 'Double-check times if this flight crosses the transition.'
                }
        
        return None
        
    except Exception:
        return None