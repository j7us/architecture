import pure_robot
from collections import namedtuple
import math
from functools import reduce

RobotState = namedtuple("RobotState", "x y angle state")

# режимы работы устройства очистки
WATER = 1 # полив водой
SOAP  = 2 # полив мыльной пеной
BRUSH = 3 # чистка щётками

class Command:
    def execute(self, state, transfer):
        pass

class MoveCommand(Command):
    def __init__(self, dist):
        self.dist = dist

    def execute(self, state, transfer):
        angle_rads = state.angle * (math.pi / 180.0)
        new_state = RobotState(
            state.x + self.dist * math.cos(angle_rads),
            state.y + self.dist * math.sin(angle_rads),
            state.angle,
            state.state)
        transfer(('POS(', new_state.x, ',', new_state.y, ')'))
        return new_state

class TurnCommand(Command):
    def __init__(self, turn_angle):
        self.turn_angle = turn_angle

    def execute(self, state, transfer):
        new_state = RobotState(
            state.x,
            state.y,
            state.angle + self.turn_angle,
            state.state)
        transfer(('ANGLE', state.angle))
        return new_state

class SetStateCommand(Command):
    def __init__(self, state):
        self.new_internal_state = state

    def execute(self, state, transfer):
        if self.new_internal_state == 'water':
            self_state = WATER
        elif self.new_internal_state == 'soap':
            self_state = SOAP
        elif self.new_internal_state == 'brush':
            self_state = BRUSH
        else:
            return state
        new_state = RobotState(
            state.x,
            state.y,
            state.angle,
            self_state)
        transfer(('STATE', self_state))
        return new_state

class StartCommand(Command):
    def execute(self, state, transfer):
        transfer(('START WITH', state.state))
        return state

class StopCommand(Command):
    def execute(self, state, transfer):
        transfer(('STOP',))
        return state


def transfer_to_cleaner(message):
    print (message)


commands = [MoveCommand(100), TurnCommand(-90), SetStateCommand(SOAP), StartCommand(), MoveCommand(50), StopCommand()]

initial_state = RobotState(0, 0, 0, WATER)

final_state = reduce(
    lambda state, cmd: cmd.execute(state, transfer_to_cleaner),
    commands,
    initial_state
)
