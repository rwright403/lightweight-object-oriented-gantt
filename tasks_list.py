from core import *

from core import Task
from datetime import date

tasks = [
    Task(
        task_name="buying_eggs_flour_butter_chocolate_and_sugar",
        start_date=date(2025, 5, 1),
        end_date=date(2025, 5, 3),
        status=0,  # TODO
        critical_rank=1,
        project="baking_cake",
        assignee="gordon",
        dependencies=None
    ),
    Task(
        task_name="mixing_ingredients",
        start_date=date(2025, 5, 4),
        end_date=date(2025, 5, 5),
        status=0,
        critical_rank=2,
        project="baking_cake",
        assignee="gordon",
        dependencies=["buying_eggs_flour_butter_chocolate_and_sugar"]
    ),
    Task(
        task_name="baking_in_the_oven",
        start_date=date(2025, 5, 6),
        end_date=date(2025, 5, 7),
        status=0,
        critical_rank=3,
        project="baking_cake",
        assignee="gordon",
        dependencies=["mixing_ingredients"]
    ),
    Task(
        task_name="eating_cake",
        start_date=date(2025, 5, 8),
        end_date=date(2025, 5, 8),
        status=0,
        critical_rank=None,
        project="baking_cake",
        assignee="ryan",
        dependencies=["baking_cake"]
    ),
]