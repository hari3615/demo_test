# app/utils/datetime_utils.py
from datetime import datetime, timezone, timedelta

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

def format_datetime(dt: datetime) -> str:
    return dt.isoformat()
