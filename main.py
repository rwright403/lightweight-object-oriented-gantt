from core import *
from tasks_list import *
from tasks_list import tasks
import importlib
import plotly.io as pio
pio.renderers.default = 'browser'


from tasks_list import tasks, deadlines

def main():
    """
    #debug code
    for t in tasks:
        print(t)
    """
    gantt = Gantt(tasks, deadlines)


    user_input = 0
    while(user_input ==0):
        print("1 --> Color by project")
        print("2 --> Color by assignee")
        print("3 --> Color by completion status")
        print("4 --> Color by critical_rank")
        print("5 --> Select a task with dependencies and color all dependencies")

        user_input = input("Enter a number to select how to color the gantt chart: ")

    if user_input =='1': gantt.project_color_map()
    if user_input =='2': gantt.assignee_color_map()
    if user_input =='3': gantt.status_map()
    if user_input =='4': gantt.critical_rank_map()
    if user_input =='5': gantt.dependencies_map()
    
    gantt.plot()

if __name__ == "__main__":
    main()