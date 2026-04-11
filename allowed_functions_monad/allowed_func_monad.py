from functools import wraps
from collections import namedtuple
import math
from typing import Tuple, List, Optional, Dict


class MoveResponse:
    OK = "MOVE_OK"
    BARRIER = "HIT_BARRIER"


class SetStateResponse:
    OK = "STATE_OK"
    NO_WATER = "OUT_OF_WATER"
    NO_SOAP = "OUT_OF_SOAP"


RobotState = namedtuple("RobotState", "x y angle state")

WATER = 1
SOAP = 2
BRUSH = 3


class StateMonad:
    def __init__(self, state: RobotState, log: List[str] = None, allowed_actions: Dict[str, bool] = None):
        self.state = state
        self.log = log or []
        self.allowed_actions = allowed_actions

    def bind(self, func):
        if not self.allowed_actions[func.__name__]:
            return StateMonad(self.state, self.log, self.allowed_actions)
        new_state, new_log, new_allowed_actions = func(self.state, self.log)
        return StateMonad(new_state, new_log, {**self.allowed_actions, **new_allowed_actions})


def check_position(x: float, y: float) -> tuple[float, float, str]:
    constrained_x = max(0, min(100, x))
    constrained_y = max(0, min(100, y))

    if x == constrained_x and y == constrained_y:
        return (x, y, MoveResponse.OK)
    return (constrained_x, constrained_y, MoveResponse.BARRIER)


def check_resources(new_mode: int) -> SetStateResponse:
    if new_mode == WATER:
        # ....
        return SetStateResponse.NO_WATER
    elif new_mode == SOAP:
        # ....
        return SetStateResponse.NO_SOAP
    return SetStateResponse.OK


def move(dist, old_state, log):
    angle_rads = old_state.angle * (math.pi / 180.0)
    new_x = old_state.x + dist * math.cos(angle_rads)
    new_y = old_state.y + dist * math.sin(angle_rads)

    constrained_x, constrained_y, move_result = check_position(new_x, new_y)

    new_state = RobotState(
        constrained_x,
        constrained_y,
        old_state.angle,
        old_state.state
    )

    message = (f'POS({int(constrained_x)},{int(constrained_y)})'
               if move_result == MoveResponse.OK
               else f'HIT_BARRIER at ({int(constrained_x)},{int(constrained_y)})')

    return new_state, log + [message], move_result


def turn(angle, old_state, log):
    new_state = RobotState(
        old_state.x,
        old_state.y,
        old_state.angle + angle,
        old_state.state
    )
    return new_state, log + [f'ANGLE {new_state.angle}'], MoveResponse.OK


def set_state(new_mode, old_state, log):
    resource_check = check_resources(new_mode)

    if resource_check != SetStateResponse.OK:
        message = f'RESOURCE ERROR: {resource_check} for mode {new_mode}'
        return old_state, log + [message], resource_check

    new_state = RobotState(
        old_state.x,
        old_state.y,
        old_state.angle,
        new_mode
    )
    return new_state, log + [f'STATE {new_mode}'], SetStateResponse.OK

actions_to_allow = {
            'move': True,
            'turn': True,
            'set_state': True,
            'start': True,
            'stop': True
        }

initial_state = StateMonad(RobotState(0.0, 0.0, 0, WATER), None, actions_to_allow)
result = (initial_state
          .bind(lambda state, log: move(150, state, log))
          .bind(lambda state, log: set_state(SOAP, state, log))
          .bind(lambda state, log: turn(-90, state, log))
          .bind(lambda state, log: move(50, state, log)))

print(f"Final state: {result.state}")
print(f"Log: {result.log}")