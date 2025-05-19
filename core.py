import pandas as pd
import plotly.express as px
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

    def check_dependencies(self):
        for str in self.dependencies:
            if str == self.task_name:
                raise ValueError(f"Task '{self.task_name}' given itself as a dependency.")


    def __str__(self):
        return (f"Task('{self.task_name}', {self.start_date} to {self.end_date}, "
                f"status={self.status}, critical_rank={self.critical_rank}, "
                f"project='{self.project}', assignee='{self.assignee}')")



import pandas as pd
import plotly.express as px

class Gantt:
    def __init__(self, tasks):
        # tasks is a list of Task objects
        self.df = self._tasks_to_df(tasks)
        self.color_mode = None  # e.g. 'project', 'assignee', 'critical_rank', 'status'
        self.date_range = None  # tuple (start_date, end_date)

    def _tasks_to_df(self, tasks):
        # Convert list of Task objects into pandas DataFrame
        data = []
        for t in tasks:
            data.append({
                'task_name': t.task_name,
                'start_date': t.start_date,
                'end_date': t.end_date,
                'status': t.status,
                'critical_rank': t.critical_rank if t.critical_rank is not None else 9999,
                'project': t.project,
                'assignee': t.assignee,
                'dependencies': t.dependencies
            })
        df = pd.DataFrame(data)
        return df

    def filter_date_range(self, start_date, end_date):
        self.date_range = (start_date, end_date)
        self.df = self.df[
            (self.df['start_date'] <= end_date) &
            (self.df['end_date'] >= start_date)
        ]

    def filter_critical_tasks(self, top_n=3):
        # Keep only tasks with critical rank 1 to top_n
        self.df = self.df[self.df['critical_rank'].notnull()]
        self.df = self.df[self.df['critical_rank'] <= top_n]

    def set_color_mode(self, mode):
        # mode in ['project', 'assignee', 'critical_rank', 'status']
        self.color_mode = mode

    def _get_color_discrete_map(self):
        # Map each category to a color for plotly
        unique_vals = self.df[self.color_mode].unique()
        colors = px.colors.qualitative.Plotly  # default qualitative colors
        color_map = {val: colors[i % len(colors)] for i, val in enumerate(unique_vals)}
        return color_map

    def highlight_dependencies(self, base_color_map):
        # Color all dependencies red in addition to base coloring
        dep_tasks = set()
        for deps in self.df['dependencies']:
            if deps:
                dep_tasks.update(deps)
        # We'll override the color_map here:
        color_map = base_color_map.copy()
        for task in dep_tasks:
            color_map[task] = 'red'
        return color_map

    def plot(self):
        if self.color_mode is None:
            color_col = 'project'
        else:
            color_col = self.color_mode

        color_map = self._get_color_discrete_map()
        color_map = self.highlight_dependencies(color_map)

        fig = px.timeline(
            self.df,
            x_start='start_date',
            x_end='end_date',
            y='task_name',
            color=color_col,
            color_discrete_map=color_map,
            hover_data=['assignee', 'status', 'critical_rank', 'project']
        )
        fig.update_yaxes(autorange="reversed")  # tasks from top to bottom

        fig.show()
