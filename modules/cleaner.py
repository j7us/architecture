import math

class Cleaner:

    def __init__(self, transfer):
        self.transfer = transfer
        self.x = 0
        self.y = 0
        self.angle = 0
        self.clean_type = 1

    def move(self, dist):
        angle_rads = self.angle * (math.pi / 180.0)
        self.x += dist * math.cos(angle_rads)
        self.y += dist * math.sin(angle_rads)
        self.transfer(('POS(', self.x, ',', self.y, ')'))

    def turn(self, turn_angle):
        self.angle += turn_angle
        self.transfer(('ANGLE', self.angle))

    def set_state(self, new_state):
        global state
        if new_state == 'water':
            state = 1
        elif new_state == 'soap':
            state = 2
        elif new_state == 'brush':
            state = 3
        self.transfer(('STATE', state))

    def start(self):
        self.transfer(('START WITH', state))

    def stop(self):
        self.transfer(('STOP',))

    def execute(self, commands):
        for command in commands:
            cmd = command.split(' ')

            if cmd[0] == 'move':
                self.move(int(cmd[1]))

            elif cmd[0] == 'turn':
                self.turn(int(cmd[1]))

            elif cmd[0] == 'set':
                self.set_state(cmd[1])

            elif cmd[0] == 'start':
                self.start()

            elif cmd[0] == 'stop':
                self.stop()