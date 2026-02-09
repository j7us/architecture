import math

code = (
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
)

class State:
    def __init__(self):
        self.position_x = 0.0
        self.position_y = 0.0
        self.angle = 0
        self.clean_type = 1
        self.status = ''

clean_types = {
    'water': 1,
    'soap': 2,
    'brush': 3
}

def main():
    state = State()

    for command in code:
        cmd = command.split(' ')

        if cmd[0] == 'move':
            move(state, int(cmd[1]))
        elif cmd[0] == 'turn':
            turn(state, int(cmd[1]))
        elif cmd[0] == 'set':
            switch_clean_type(state, cmd[1])
        elif cmd[0] == 'start':
            start(state)
        else:
            stop()


def move(state, dist):
    angle_rads = state.angle * (math.pi / 180.0)
    state.position_x += dist * math.cos(angle_rads)
    state.position_y += dist * math.sin(angle_rads)
    print('POS(', state.position_x, ',', state.position_y, ')')

def turn(state, angle):
    state.angle += angle
    print('ANGLE', state.angle)

def switch_clean_type(state, clean_type):
    state.clean_type = clean_types[clean_type]
    print('STATE', state.clean_type)

def start(state):
    print('START WITH', state.clean_type)

def stop():
    print('STOP')

if __name__ == '__main__':
    main()

