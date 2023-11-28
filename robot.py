from ursina import Entity, scene, Vec3, distance, time, raycast, destroy


class Robot(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="cube",
            collider="box",
            texture="vacuum.jpg",
            position=(3, 0.6, 3),
            scale_y=0.2,
            scale_x=0.9,
            scale_z=0.9,
        )
        self.can_move = True
        self.speed = 5
        self.score = 0
        self.counter = 0
        self.directions = [
            Vec3(0, 0, 1),  # NORTH
            Vec3(1, 0, 0),  # EAST
            Vec3(0, 0, -1),  # SOUTH
            Vec3(-1, 0, 0),  # WEST
        ]
        self.choice = 0
        self.direction = self.directions[self.choice]
        self.dirties = (
            []
        )  # list for keepieng track of all the dirt that spawns on a map
        self.walls = []  # for keeping track of all the walls on the map
        self.cleaning = False  # mode flag
        self.step = 7  # step counter for cleaning mode
        self.temp_z = 0  # temporarily stores the starting position when initiating the cleaning process
        self.temp_x = 0  # as above so below

    def set_direction(self, choice):
        self.choice = choice
        self.direction = self.directions[self.choice]

    def get_direction(self):
        return self.direction

    def set_temp_z(self, z):
        self.temp_z = z

    def set_temp_x(self, x):
        self.temp_x = x

    def changeCleaning(self):
        if self.cleaning == False:
            self.cleaning = True
            self.temp_x = self.X
            self.temp_z = self.Z
            # increase the counter - the fewer the better to clean the whole map
            self.counter += 1
            # set direction to NORTH, which is starting direction for the sequence
            if self.choice != 0:
                self.set_direction(0)
        else:
            self.cleaning = False

    def isCleaning(self):
        return self.cleaning

    def set_dirties(self, dirties):
        self.dirties = dirties

    def set_walls(self, walls):
        self.walls = walls

    def turn(self):
        self.choice = (self.choice + 1) % 4
        self.direction = self.directions[self.choice]

    def move(self):
        self.position += self.direction * self.speed * time.dt

    def operate(self):
        # start by cleaning
        self.suck_dirt()
        # check if there is a wall
        self.detect_collision()
        # if possible move forward
        if self.can_move:
            self.move()
        else:
            # if not, turn right
            self.turn()
            # if you're cleaning right now, skip to the next step (they're decrimental)
            if self.cleaning:
                self.step -= 1

    def suck_dirt(self):
        # if what you touch is dirt, destroy
        if self.intersects().entity in self.dirties:
            self.score += 1
            dirt = self.intersects().entity
            destroy(dirt)

    def detect_collision(self):
        hit_info = raycast(
            self.world_position,
            self.direction,
            0.6,
            ignore=(self,),
        )
        # if there is a wall, approach a little and stop
        if hit_info.entity in self.walls:
            if distance(self, hit_info.entity) > 1:
                self.position += self.direction * self.speed * time.dt
            self.can_move = False
        # if no collision, you can move on
        if not hit_info.hit:
            self.can_move = True

    def clean_area(self):
        # cleaning sequence - to clean area of 3x3 where robot starts in the middle of that area
        if self.step == 7:
            # move one unit forward (direction is already NORTH)
            if self.z < self.temp_z + 1:
                self.operate()
            else:
                # turn to EAST
                self.turn()
                self.step -= 1
        elif self.step == 6:
            # move one unit EAST direction
            if self.x < self.temp_x + 1:
                self.operate()
            else:
                # turn to SOUTH
                self.turn()
                self.step -= 1
        elif self.step == 5:
            # move two units SOUTH direction
            if self.z > self.temp_z - 1:
                self.operate()
            else:
                # turn to WEST
                self.turn()
                self.step -= 1
        elif self.step == 4:
            # move two units WEST direction
            if self.x > self.temp_x - 1:
                self.operate()
            else:
                # turn to NORTH
                self.turn()
                self.step -= 1
        elif self.step == 3:
            # move two units NORTH direction
            if self.z < self.temp_z + 1:
                self.operate()
            else:
                # turn to EAST
                self.turn()
                self.step -= 1
        elif self.step == 2:
            # move one unit EAST direction
            if self.x < self.temp_x:
                self.operate()
            else:
                # turn to SOUTH
                self.turn()
                self.step -= 1
        elif self.step == 1:
            print("Finished cleaning")
            self.cleaning = False
            # set direction to NORTH
            self.choice = 0
            self.direction = self.directions[self.choice]
            # reset steps counter
            self.step = 7
            print(f"Counter: {self.counter}")
