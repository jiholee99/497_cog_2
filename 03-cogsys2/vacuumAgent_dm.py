from AgentSupport import MotorModule, CleanSensorModule, MyCell
import AgentSupport
import python_actr
from python_actr.lib import grid
from python_actr.actr import *
from python_actr.actr.hdm import *
import random
import time

class VacuumAgent(python_actr.ACTR):
    goal = python_actr.Buffer()
    body = grid.Body()
    motorInst = MotorModule()
    cleanSensor = CleanSensorModule()
    retrieval = Buffer()
    DM_module = Memory(retrieval, finst_size=5, finst_time=10.0)

    def init():
        print("init called...")
        goal.set("start_recall_dirt")
        self.home = None

    def recall_dirty_spots_dm(goal="start_recall_dirt", DM_module="busy:False error:False"):
        print("recall dirty spots...")
        DM_module.request("square:dirty location_x:?x location_y:?y")

    def move_to_dirty_spot(goal="start_recall_dirt", retrieval="square:dirty location_x:?x location_y:?y"):
        print("Moving to dirty spot")
        motorInst.go_towards(x, y)
        goal.set("rsearch left 1 0 1")

    def clean_cell(cleanSensor="dirty:True", utility=0.6):
        print("cleaning dirty cells")
        x, y = body.x, body.y
        DM_module.add(f"square:dirty location_x:{x} location_y:{y}")
        motorInst.clean()
    def start_swirl(goal="start_recall_dirt"):
        print("Starting to swril...")
        goal.set("rsearch left 1 0 1")

    def forward_rsearch(goal="rsearch left ?dist ?num_turns ?curr_dist",
                        motorInst="busy:False", body="ahead_cell.wall:False"):
        motorInst.go_forward()
        print(f"is wall ahead {body.ahead_cell.wall}")
        curr_dist = str(int(curr_dist) - 1)
        goal.set("rsearch left ?dist ?num_turns ?curr_dist")

    def left_rsearch(goal="rsearch left ?dist ?num_turns 0", motorInst="busy:False",
                     utility=0.1):
        motorInst.turn_left(2)
        num_turns = str(int(num_turns) + 1)
        goal.set("rsearch left ?dist ?num_turns ?dist")

    def new_search(goal="rsearch left ?dist 4 ?dist"):
        dist = str(int(dist) + 1)
        print(f"Dist : {dist}")
        goal.set(f"rsearch left {dist} 0 {dist}")
        motorInset = "busy:False"
        body = "ahead_cell.wall:False"

    def handle_wall(goal="rsearch left ?dist ?num_turns ?curr_dist",
                    body="ahead_cell.wall:True"):
        motorInst.go_left()

        num_turns = str(int(num_turns) + 1)
        goal.set("rsearch left ?dist ?num_turns ?curr_dist")


world=grid.World(MyCell,map=AgentSupport.mymap)
agent=VacuumAgent()
agent.home=()
world.add(agent,5,5,dir=0,color="black")

python_actr.log_everything(agent, AgentSupport.my_log)
window = python_actr.display(world)
world.run()
time.sleep(1)
world.reset_map(MyCell,map=AgentSupport.mymap)
world.add(agent,5,5,dir=0,color="black")
world.run()
