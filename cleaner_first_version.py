import math

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

class State:
    def __init__(self):
        self.position = (0, 0)
        self.angle = 0
        self.clean_type = 'water'
        self.status = ''

actions = {
    'move': MoveAction(),
    'turn': TurnAction(),
    'set': SetAction(),
    'start': StartAction(),
    'stop': StopAction()
}

def main():
    commands = input('Введите команды: ').split(',')

    print(commands)

    state = State()

    for command in commands:
        command_with_args = build_command_with_args(command)

        action = actions[command_with_args[0]]
        state = action.apply(state, command_with_args[1])

def build_command_with_args(durty_command):
    command = durty_command.strip()
    command = command.replace("'", '')
    ind = command.find(' ')

    command_type = command[0 : ind] if ind >= 0 else command
    args = command[ind + 1 :] if ind >- 0 else None

    return command_type, args

if __name__ == '__main__':
    main()

