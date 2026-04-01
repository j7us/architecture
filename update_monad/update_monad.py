from functools import wraps
from collections import namedtuple
import math
import random

class MoveResponse:
    OK = "MOVE_OK"
    BARRIER = "HIT_BARRIER"

class SetStateResponse:
    OK = "STATE_OK"
    NO_WATER = "OUT_OF_WATER"
    NO_SOAP = "OUT_OF_SOAP"

RobotState = namedtuple("RobotState", "x y angle state errors")

WATER = 1
SOAP = 2
BRUSH = 3


def check_position(x: float, y: float) -> tuple[float, float, str]:
    constrained_x = max(0, min(100, x))
    constrained_y = max(0, min(100, y))

    if x == constrained_x and y == constrained_y:
        return (x, y, MoveResponse.OK)
    return (constrained_x, constrained_y, MoveResponse.BARRIER)

def check_resources(new_mode: int) -> SetStateResponse:
    random_decision = random.randint(0, 1)
    if new_mode == WATER:
        if not random_decision:
            return SetStateResponse.NO_WATER
    elif new_mode == SOAP:
        if not random_decision:
            return SetStateResponse.NO_SOAP
    return SetStateResponse.OK


class StateMonad:
    def __init__(self, state, log=None):
        self.state = state
        self.log = log or []

    def bind(self, func):
        new_state, new_log = func(self.state, self.log)
        return StateMonad(new_state, new_log)


def move(dist):
    def inner(old_state, log):
        angle_rads = old_state.angle * (math.pi / 180.0)
        act_x = old_state.x + dist * math.cos(angle_rads),
        act_y = old_state.y + dist * math.sin(angle_rads)

        x, y, status = check_position(act_x, act_y)

        if not status == SetStateResponse.MOVE_OK:
            return

        new_state = RobotState(
            x,
            y,
            old_state.angle,
            old_state.state
        )
        return new_state, log + [f'POS({int(new_state.x)},{int(new_state.y)})']

    return inner

def turn(angle):
    def inner(old_state, log):
        new_state = RobotState(
            old_state.x,
            old_state.y,
            old_state.angle + angle,
            old_state.state
        )
        return new_state, log + [f'ANGLE {new_state.angle}']

    return inner


def set_state(new_mode):
    def inner(old_state, log):
        new_state = RobotState(
            old_state.x,
            old_state.y,
            old_state.angle,
            new_mode
        )
        return new_state, log + [f'STATE {new_mode}']

    return inner


def start(old_state, log):
    return old_state, log + ['START']


def stop(old_state, log):
    return old_state, log + ['STOP']


initial_state = StateMonad(RobotState(0.0, 0.0, 0, WATER))
result = (initial_state
          .bind(move(100))
          .bind(turn(-90))
          .bind(set_state(SOAP))
          .bind(start)
          .bind(move(50))
          .bind(stop))

print(f"Final state: {result.state}")
print(f"Log: {result.log}")