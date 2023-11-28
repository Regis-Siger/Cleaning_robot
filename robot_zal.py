import random
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from robot import Robot


def update():
    # if robot is cleaning, follow the cleaning sequence
    if robot.isCleaning():
        robot.clean_area()
    else:
        # if it's not, operate as usual - go around the walls
        robot.operate()
    # display score and modus operandi
    remaining_info.text = f"Remaining dirt: {amounf_of_dirt - robot.score}"
    cleaning_text.text = f"Cleaning mode: {robot.isCleaning()}"
    basic_info.text = f"'ESC' - Quit\n'c' - toggle mode"
    counter_info.text = f"Counter: {robot.counter}"


def input(key):
    if key == "escape":
        print(f"Final counter: {robot.counter}")
        quit()
    if key == "c":
        # change mode between usual and cleaning
        robot.changeCleaning()


# initialize stuff
app = Ursina()
camera = FirstPersonController(position=(1, 2, 5))

# info texts
remaining_info = Text("Remaining", scale=2, origin=(1, -8), color=color.white)
cleaning_text = Text("Cleaning mode: ", scale=2, origin=(1, -7), color=color.white)
basic_info = Text("Basic info", scale=2, origin=(-1.2, -4), color=color.white)
counter_info = Text("Counter", scale=2, origin=(0, -2), color=color.white)

level = 20
dirties = []
walls = []

# building floor and walls
for x in range(level):
    for z in range(level):
        # walls
        if (x == 0) or (x == (level - 1)) or (z == 0) or (z == (level - 1)):
            wall = Entity(
                model="cube",
                collider="box",
                texture="mercury",
                color=color.dark_gray,
                ignore=True,
                position=(x, 0, z),
                scale_y=6,
            )
            walls.append(wall)
        else:
            # floor
            Entity(
                model="cube",
                collider="box",
                texture="wood",
                color=color.dark_gray,
                ignore=True,
                position=(x, 0, z),
            )

dirties = []
# spawning dirt
amounf_of_dirt = int(level * level / 2)
for i in range(amounf_of_dirt):
    dirt = Entity(
        model="cube",
        collider="box",
        texture="texture",
        position=(random.uniform(1, 18), 0.5, random.uniform(1, 18)),
        scale=0.2,
        color=color.yellow,
    )
    dirties.append(dirt)

# initiating cleaning robot
robot = Robot()
# loading information about the map
robot.set_dirties(dirties)
robot.set_walls(walls)


app.run()
