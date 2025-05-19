import strcase
from datetime import date
from typing import Optional

class Task:
    def __init__(
            self, 
            task_name: str, 
            start_date: date, 
            end_date: date, 
            status: int, 
            critical_rank: Optional[int], 
            project: str,
            assignee: str,
            dependencies: Optional[list[str]] = None
            ):
        
        self.task_name = strcase.to_snake(task_name.strip())
        self.start_date = start_date
        self.end_date = end_date
        self.status = status  # 0=TODO, 1=Started, 2=Complete
        self.critical_rank = critical_rank
        self.project = strcase.to_snake(project.strip())
        self.assignee = strcase.to_snake(assignee.strip())
        
        self.dependencies = []
        if dependencies is not None: 
            for str in dependencies: self.dependencies.append(strcase.to_snake(str.strip()))
        
        self.check_dates()
        self.check_status()


    def check_dates(self):
        if self.end_date < self.start_date:
            raise ValueError(f"End date {self.end_date} cannot be before start date {self.start_date} for task '{self.task_name}'.")
        
    def check_status(self):
        if 1 > self.status and 2 < self.status:
            raise ValueError(f"Status {self.status} of task '{self.task_name}' does not correspond to a known Status:\n0=TODO\n1=Started\n2=Complete\n(for reference)")

    def __str__(self):
        return (f"Task('{self.task_name}', {self.start_date} to {self.end_date}, "
                f"status={self.status}, critical_rank={self.critical_rank}, "
                f"project='{self.project}', assignee='{self.assignee}')")



class Gantt:
    x=1