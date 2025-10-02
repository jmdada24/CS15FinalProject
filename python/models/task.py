"""Task model matching Flutter Task class"""
from datetime import datetime
from typing import Optional

class Task:
    def __init__(
        self,
        title: str,
        notes: str = "",
        date: Optional[datetime] = None,
        time: Optional[str] = None,
        category: str = "Other",
        is_done: bool = False
    ):
        self.title = title
        self.notes = notes
        self.date = date
        self.time = time
        self.category = category
        self.is_done = is_done
    
    def toggle_done(self):
        """Toggle task completion status"""
        self.is_done = not self.is_done
    
    def get_datetime_str(self) -> str:
        """Format date and time for display"""
        parts = []
        if self.date:
            parts.append(self.date.strftime("%b %d"))
        if self.time:
            parts.append(self.time)
        return " · ".join(parts) if parts else ""
    
    def __repr__(self):
        return f"Task(title='{self.title}', category='{self.category}', is_done={self.is_done})"
