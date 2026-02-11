import math

code = (
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
)

class CleanerAction:
    def apply(self, state, action_info):
        pass

class MoveAction(CleanerAction):
    def apply(self, state, action_info):
        distance = int(action_info)

        angle_rad = math.radians(state.angle)

        dx = math.sin(angle_rad) * distance
        dy = math.cos(angle_rad) * distance

        current_position = state.position

        new_x = current_position[0] + dx
        new_y = current_position[1] + dy

        state.position = (new_x, new_y)

        print(f'POS {new_x}, {new_y}')

        return state

class TurnAction(CleanerAction):
    def apply(self, state, action_info):
        angle = int(action_info)
        state.angle += angle

        print(f'ANG {state.angle}')
        return state

class SetAction(CleanerAction):
    def apply(self, state, action_info):
        state.clean_type = action_info

        print(f'STATE {state.clean_type}')
        return state

class StartAction(CleanerAction):
    def apply(self, state, action_info):
        print(f'START WITH {state.clean_type}')

        state.status = 'START'

        return state

class StopAction(CleanerAction):
    def apply(self, state, action_info):
        print('STOP')

        state.status = 'STOP'

        return state

class CleanerActionsFactory:
    def __init__(self):
        self.actions = {
            'move': MoveAction(),
            'turn': TurnAction(),
            'set': SetAction(),
            'start': StartAction(),
            'stop': StopAction()
        }

    def get_action(self, action_type):
        return self.actions[action_type]

class State:
    def __init__(self):
        self.position = (0, 0)
        self.angle = 0
        self.clean_type = 1
        self.status = ''

class CleanerPlanExecutor:

    def __init__(self, actions_factory, cleaner_state):
        self.actions_factory = actions_factory
        self.cleaner_state = cleaner_state

    def execute(self, commands):
        for command in commands:
            cmd = command.split(' ')
            action = self.actions_factory.get_action(cmd[0])

            action.apply(self.cleaner_state, cmd[1] if len(cmd) > 1 else None)

plan_executor = CleanerPlanExecutor(CleanerActionsFactory(), State())

plan_executor.execute(code)
