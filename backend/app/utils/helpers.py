"""Utility functions — pagination helpers, date utilities."""

from datetime import date
from math import ceil
from typing import TypeVar, Generic, List

T = TypeVar("T")


def calculate_nights(check_in: date, check_out: date) -> int:
    """Return number of nights between two dates."""
    return max(0, (check_out - check_in).days)


def paginate(items: List, page: int, page_size: int) -> dict:
    """In-memory pagination helper (prefer DB-level pagination in production)."""
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": ceil(total / page_size) if total > 0 else 1,
    }
