
import datetime as dt
from dataclasses import dataclass

@dataclass
class ReviewItem:
    key: str
    ease: float
    interval_days: int
    due_date: dt.date

def sm2(ease: float, quality: int, interval_days: int) -> (float, int):
    """
    Very small SM-2 like update.
    quality: 0..5
    """
    ease = max(1.3, ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
    if quality < 3:
        interval_days = 1
    else:
        if interval_days == 0:
            interval_days = 1
        elif interval_days == 1:
            interval_days = 6
        else:
            interval_days = int(round(interval_days * ease))
    return ease, interval_days

def next_due_date(interval_days: int, today=None):
    today = today or dt.date.today()
    return today + dt.timedelta(days=interval_days)
