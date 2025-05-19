import pandas as pd
import plotly.express as px
import strcase
import re
from datetime import date, timedelta
from typing import Optional

class Deadline:
    def __init__(self, deadline_name: str, deadline_date: date):
        self.deadline_name = deadline_name
        self.deadline_date = deadline_date

class Task:
    def __init__(
            self, 
            project: str,
            task_name: str, 

            start_date: date, 
            end_date: date, 
            status: int, 
            critical_rank: Optional[int], 
            assignee: str,
            dependencies: Optional[list[str]] = None
            ):
        
        self.project = strcase.to_snake(re.sub(r'\s+', ' ', project).strip().lower())
        self.task_name = strcase.to_snake(re.sub(r'\s+', ' ', task_name).strip().lower())

        self.start_date = start_date
        self.end_date = end_date
        self.status = status  # 0=TODO, 1=Started, 2=Complete
        self.critical_rank = critical_rank
        self.assignee = strcase.to_snake(re.sub(r'\s+', ' ', assignee).strip().lower())
        
        self.dependencies = []
        if dependencies is not None: 
            for str in dependencies: self.dependencies.append(strcase.to_snake(re.sub(r'\s+', ' ', str).strip().lower()))
        
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



class Gantt:
    def __init__(self, tasks, deadlines):
        # tasks is a list of Task objects
        self.df = self._tasks_to_df(tasks)
        self.deadlines = deadlines

        self.color_map = None
        self.color_col = None
        self.title_str = None


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
    

    def project_color_map(self):
        unique_vals = self.df['project'].unique()
        colors = px.colors.qualitative.Alphabet  #NOTE: 26 default colors
        self.color_map = {val: colors[i % len(colors)] for i, val in enumerate(unique_vals)}
        self.color_col = 'project'
        self.title_str = "Gantt colored based on project"


    def assignee_color_map(self):
        unique_vals = self.df['assignee'].unique()
        colors = px.colors.qualitative.Alphabet  #NOTE: 26 default colors
        self.color_map = {val: colors[i % len(colors)] for i, val in enumerate(unique_vals)}
        self.color_col = 'assignee'
        self.title_str = "Gantt colored based on assignee"


    def status_map(self):
        # Base project color map
        unique_projects = self.df['project'].unique()
        base_colors = px.colors.qualitative.Alphabet
        self.color_map = {project: base_colors[i % len(base_colors)] for i, project in enumerate(unique_projects)}

        # Status-based override colors
        status_colors = {
            0: 'red',     # Unstarted
            1: 'yellow',  # Started
            2: 'green'    # Complete
        }

        # Override colors for each task based on its status
        for _, row in self.df.iterrows():
            project = row['project']
            status = row['status']
            if status in status_colors:
                self.color_map[project] = status_colors[status]  # override project color

        self.color_col = 'project'
        self.title_str = "Gantt colored by project, overridden by status"


    def critical_rank_map(self):
        # Base project colors
        unique_projects = self.df['project'].unique()
        base_colors = px.colors.qualitative.Light24
        self.color_map = {project: base_colors[i % len(base_colors)] for i, project in enumerate(unique_projects)}

        # Loop over rows to assign colors per task
        for _, row in self.df.iterrows():
            project = row['project']
            critical_rank = row['critical_rank']

            if critical_rank == "1":
                self.color_map[critical_rank] = 'red'   # override critical tasks with red


        self.color_col = 'critical_rank'  # Color by task to apply per-task colors
        self.title_str = "Gantt colored by critical path"


    def dependencies_map(self):
        # Repeatedly prompt the user until they enter a valid task
        while True:
            task_with_dependencies = input("Enter a task with dependencies: ")
            task_with_dependencies = strcase.to_snake(re.sub(r'\s+', ' ', task_with_dependencies).strip().lower())

            if task_with_dependencies in self.df['task_name'].values:
                break
            else:
                print(f"Task '{task_with_dependencies}' not found. Please try again.")

        # Base colors for projects
        unique_projects = self.df['task_name'].unique()
        project_color_map = {proj: '#808080'  for i, proj in enumerate(unique_projects)}

        # Initialize color_map keyed by task ID (assumes 'task' column uniquely identifies tasks)
        self.color_map = {}

        # Collect all dependency tasks in a set
        dep_tasks = set()
        
        # Assign default color per project to all tasks
        for _, row in self.df.iterrows():
            self.color_map[row['task_name']] = project_color_map.get(row['project'], 'gray')

        # Find the target task row
        task_row = self.df[self.df['task_name'] == task_with_dependencies]
        self.color_map[task_with_dependencies] = 'blue'  # Override task color

        if not task_row.empty:
            dependencies = task_row.iloc[0]['dependencies']
            if dependencies:
                for dep_task in dependencies:
                    if dep_task in self.df['task_name'].values:
                        self.color_map[dep_task] = 'red'  # Override dependent task color

        self.color_col = 'task_name'  # Color by task to apply per-task colors
        self.title_str = "Gantt colored based on dependencies"  


    def plot(self):
        ### create figure
        self.df["end_date"] = self.df["end_date"] + timedelta(days=1) # Need to add one to the end day for the task to appear as if it finishes on the end day

        fig = px.timeline(
            self.df,
            x_start='start_date',
            x_end='end_date',
            y='task_name',
            title=self.title_str,
            color=self.color_col,
            color_discrete_map=self.color_map,
            hover_data=['assignee', 'status', 'critical_rank', 'project']
        )

        ### plot deadlines
        for deadline in self.deadlines:
            
            fig.add_shape(
                type="line",
                x0=pd.to_datetime(deadline.deadline_date),
                x1=pd.to_datetime(deadline.deadline_date),
                y0=0,
                y1=1,
                yref='paper',  # makes y span entire plot height
                line=dict(color="red", width=2, dash="dash")
            )

            fig.add_annotation(
                x=pd.to_datetime(deadline.deadline_date),  # same x as line
                y=1,  # top of the plot area
                yref='paper',
                text=f"{deadline.deadline_date}, {deadline.deadline_name}",  # label text
                showarrow=False,
                xanchor='left',  # controls horizontal alignment relative to x
                yanchor='bottom',  # controls vertical alignment relative to y
                font=dict(color="red", size=12),
                bgcolor='rgba(255,255,255,0.7)',  # optional: white background with some transparency
                bordercolor='red',
                borderwidth=1,
                borderpad=2,
                opacity=0.9,
            )
        
        fig.update_yaxes(autorange="reversed")  # tasks from top to bottom
        fig.update_layout(legend_title_text=self.color_col.capitalize())
        fig.show()
