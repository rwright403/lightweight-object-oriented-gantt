# lightweight-object-oriented-gantt

This program is a lightweight object oriented gantt chart:

The GUI is vscode and the gantt chart versions are tracked through github.
- This was chosen for agility of both programming and for the user to use.

# User Guide:

There are three files:
- core.py --> contains all objects - abstractions the user of the program does not need to interact with (don't change)
- task_list.py --> is the input file for the user to enter the tasks (add tasks here)
- main.py --> this is the file that will ask for additional user input and create the gantt chart (run this file)

## Creating Tasks:
The tasks are added to the "tasks" list in task_list.py

copy the following template into the tasks list and replace the <> with text.
for fields with multiple <> below, they are interpreted by the program as lists, which can have a single entry as required. For multiple entries make sure to split them with commas

>        Task(
>            task_name="<str>",
>            start_date=date( <input year int>, <input month int>, <input day int>),
>            end_date=date( <input year int>, <input month int>, <input day int>),
>            status=<int>,  
>            critical_rank=<int>,                                      #can also set critical_rank to None, or add more fields if desired
>            project="str",
>            assignee="str",
>            dependencies="<str> ","<str>"                             #can also set critical_rank to None, or add more fields if desired
>        ),


## Setup:

You will need the following:
- python 
- vscode
- github desktop

once you have all 3 softwares:
1) use github desktop to "clone" this repository
2) download all the required python libraries

# Documentation: