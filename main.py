from core import *
from tasks_list import *
from tasks_list import tasks

import plotly.io as pio
pio.renderers.default = 'browser'


from tasks_list import tasks

def main():
    """
    #debug code
    for t in tasks:
        print(t)
    """

    gantt = Gantt(tasks)
    gantt.set_color_mode('project')  # or 'critical_rank', 'assignee', 'status'
    gantt.plot()

if __name__ == "__main__":
    main()