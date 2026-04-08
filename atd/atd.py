from collections import namedtuple
import math

RobotState = namedtuple("RobotState", "x y angle state")

WATER = 1
SOAP = 2
BRUSH = 3

class Robot:

    def move(self, old_state):
        angle_rads = old_state.angle * (math.pi / 180.0)
        new_x = old_state.x + self.dist * math.cos(angle_rads)
        new_y = old_state.y + self.dist * math.sin(angle_rads)

        new_state = RobotState(
            new_x,
            new_y,
            old_state.angle,
            old_state.state
        )

        return new_state

    def set_state(self, new_mode, old_state):
        new_state = RobotState(
            old_state.x,
            old_state.y,
            old_state.angle,
            new_mode
        )
        return new_state

    def turn(self, angle, old_state):
        new_state = RobotState(
            old_state.x,
            old_state.y,
            old_state.angle + angle,
            old_state.state
        )
        return new_state

    def start(self, old_state):
        print('Starting Robot')
        return old_state

    def stop(self, old_state):
        print('Stopping Robot')
        return old_state