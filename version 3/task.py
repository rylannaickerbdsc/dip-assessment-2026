class Task:
    """Blueprint for a study task object."""

    def __init__(self, name, subject, duration, priority="Med"):
        self.name = name
        self.subject = subject
        self.duration = duration
        self.priority = priority

    def get_priority_rank(self):
        """Helper method to rank priorities for sorting (High=1, Med=2, Low=3)."""
        ranks = {"High": 1, "Med": 2, "Low": 3}
        return ranks.get(self.priority, 4)

    def get_details(self):
        """Formats the task display string for the listbox."""
        return f"[{self.priority}] [{self.subject}] {self.name} - {self.duration} mins"

    def to_file_line(self):
        """Formats data into a single line for external file storage (CSV format)."""
        return f"{self.name},{self.subject},{self.duration},{self.priority}\n"