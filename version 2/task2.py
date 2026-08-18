class Task:

    def __init__(self, name, duration, priority="Med"):
        self.name = name
        self.duration = duration
        self.priority = priority

    def get_details(self):
        return f"{self.name} - {self.duration} mins [{self.priority}]"