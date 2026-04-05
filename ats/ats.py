from dataclasses import dataclass
from typing import List, Protocol, Any
from enum import Enum
import math
from collections import namedtuple

RobotState = namedtuple("RobotState", "x y angle state")


# Режимы работы
class CleaningMode(Enum):
    WATER = 1
    SOAP = 2
    BRUSH = 3


class MoveResponseStatus:
    OK = "MOVE_OK"
    BARRIER = "HIT_BARRIER"


class TurnResponseStatus:
    OK = "TURN_OK"


class SetStateResponseStatus:
    OK = "STATE_OK"
    NO_WATER = "OUT_OF_WATER"
    NO_SOAP = "OUT_OF_SOAP"


class MoveResponse:
    distance: float
    move_status: MoveResponseStatus

    def __init__(self, distance, move_status):
        self.distance = distance
        self.move_status = move_status


class TurnResponse:
    angle: float
    turn_status: TurnResponseStatus

    def __init__(self, angle, turn_status):
        self.angle = angle
        self.turn_status = turn_status


class SetStateResponse:
    state: str
    state_status: SetStateResponseStatus

    def __init__(self, state, state_status):
        self.state = state
        self.state_status = state_status


def check_position(x, y):
    constrained_x = max(0, min(100, x))
    constrained_y = max(0, min(100, y))

    if x == constrained_x and y == constrained_y:
        return (x, y, MoveResponseStatus.OK)
    return (constrained_x, constrained_y, MoveResponseStatus.BARRIER)


def check_resources(new_mode):
    if new_mode == CleaningMode.WATER.value:
        # ....
        return SetStateResponseStatus.NO_WATER
    elif new_mode == CleaningMode.SOAP.value:
        # ....
        return SetStateResponseStatus.NO_SOAP
    return SetStateResponseStatus.OK


class Node:
    def interpret(self, state):
        pass


class MoveNode(Node):
    distance: float

    def __init__(self, distance, next_node):
        self.distance = distance
        self.next_node = next_node

    def interpret(self, state):
        new_state, move_result = self.__execute(state)

        next_chosen_node = self.next_node(MoveResponse(self.distance, move_result))

        return new_state, next_chosen_node

    def __execute(self, state):
        angle_rads = state.angle * (math.pi / 180.0)
        new_x = state.x + self.distance * math.cos(angle_rads)
        new_y = state.y + self.distance * math.sin(angle_rads)

        constrained_x, constrained_y, move_result = check_position(new_x, new_y)

        new_state = RobotState(
            constrained_x,
            constrained_y,
            state.angle,
            state.state
        )

        return new_state, move_result


class TurnNode(Node):
    angle: float

    def __init__(self, angle, next_node):
        self.angle = angle
        self.next_node = next_node

    def interpret(self, state):
        new_state, move_result = self.__execute(state)
        next_chosen_node = self.next_node(TurnResponse(self.angle, move_result))

        return new_state, next_chosen_node

    def __execute(self, state):
        new_state = RobotState(
            state.x,
            state.y,
            state.angle + self.angle,
            state.state
        )

        return new_state, TurnResponseStatus.OK


class SetStateNode(Node):
    state: CleaningMode

    def __init__(self, new_state, next_node):
        self.new_state = new_state
        self.next_node = next_node

    def interpret(self, state):
        updated_state, state_result = self.__execute(state)
        next_chosen_node = self.next_node(SetStateResponse(self.new_state, state_result))

        return updated_state, next_chosen_node

    def __execute(self, state):
        resource_check = check_resources(self.new_state)

        if resource_check != SetStateResponse.OK:
            return state, resource_check

        new_state = RobotState(
            state.x,
            state.y,
            state.angle,
            self.new_state
        )

        return new_state, SetStateResponseStatus.OK


class StopNode(Node):

    def interpret(self, state):
        return state, None


class Interpreter:

    def __init__(self, start_node):
        self.start_node = start_node
        self.start_state = RobotState(0.0, 0.0, 0, CleaningMode.WATER.value)

    def start_interpreter(self):
        next_node = self.start_node
        state = self.start_state

        while next_node != None:
            state, next_node = next_node.interpret(state)

        return state


stopNode = StopNode()
moveNode = MoveNode(50, lambda x: stopNode)
turnNode = TurnNode(-90, lambda x: moveNode)
setStateNode = SetStateNode(CleaningMode.SOAP.value, lambda x: turnNode)
moveNodeFirst = MoveNode(150, lambda x: setStateNode)

interpreter = Interpreter(moveNodeFirst)

result = interpreter.start_interpreter()

