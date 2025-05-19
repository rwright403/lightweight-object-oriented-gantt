from core import *

from core import Task, Deadline
from datetime import date

deadlines = [
    Deadline(
        deadline_name="design review",
        deadline_date=date(2025, 5, 7),
    ),
]

tasks = [
    Task(
        project="baking_cake",
        task_name="buying_eggs_flour_butter_chocolate_and_sugar",

        start_date=date(2025, 5, 1),
        end_date=date(2025, 5, 3),
        status=0,  # TODO
        critical_rank="1",
        assignee="gordon",
        dependencies=None
    ),
    Task(
        project="baKING CAKE",
        task_name="mixing_ingredients",

        start_date=date(2025, 5, 4),
        end_date=date(2025, 5, 5),
        status=0,
        critical_rank="2",
        assignee="gordon",
        dependencies=["buying_eggs_flour_butter_chocolate_and_sugar"]
    ),
    Task(
        project="baking_cake",
        task_name="baking_in_the_oven",

        start_date=date(2025, 5, 6),
        end_date=date(2025, 5, 7),
        status=0,
        critical_rank="3",
        assignee="gordon",
        dependencies=["mixing_ingredients"]
    ),
    Task(
        project="baking_cake",
        task_name="eating_cake",

        start_date=date(2025, 5, 8),
        end_date=date(2025, 5, 8),
        status=0,
        critical_rank="2",
        assignee="ryan",
        dependencies=["baking_cake"]
    ),

        Task(
        project="intern_task",
        task_name="make me a coffee",

        start_date=date(2025, 5, 4),
        end_date=date(2025, 5, 8),
        status=1,
        critical_rank=None,
        assignee="gordon",
        dependencies=None
    ),
]