import pure_robot

# класс Чистильщик API
class CleanerApi:

    # конструктор
    def __init__(self, robot):
        self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
        self.robot = robot

    # взаимодействие с роботом вынесено в отдельную функцию
    def transfer_to_cleaner(self,message):
        print (message)

    def get_x(self):
        return self.cleaner_state.x

    def get_y(self):
        return self.cleaner_state.y

    def get_angle(self):
        return self.cleaner_state.angle

    def get_state(self):
        return self.cleaner_state.state

    def activate_cleaner(self,code):
        for command in code:
            cmd = command.split(' ')
            if cmd[0]=='move':
                self.cleaner_state = self.robot.move(int(cmd[1]),self.cleaner_state)
            elif cmd[0]=='turn':
                self.cleaner_state = self.robot.turn(int(cmd[1]),self.cleaner_state)
            elif cmd[0]=='set':
                self.cleaner_state = self.robot.set_state(cmd[1],self.cleaner_state)
            elif cmd[0]=='start':
                self.cleaner_state = self.robot.start(self.cleaner_state)
            elif cmd[0]=='stop':
                self.cleaner_state = self.robot.stop(self.cleaner_state)

class Robot:
    def move(self, dist, state):
        pass

    def turn(self, turn_angle, state):
        pass

    def set_state(self, new_internal_state, state):
        pass

    def start(self, state):
        pass

    def stop(self, state):
        pass

class PureRobot(Robot):

    def __init__(self, transfer):
        self.transfer = transfer

    def move(self, dist, state):
        angle_rads = state.angle * (math.pi / 180.0)
        new_state = RobotState(
            state.x + dist * math.cos(angle_rads),
            state.y + dist * math.sin(angle_rads),
            state.angle,
            state.state)
        self.transfer(('POS(', new_state.x, ',', new_state.y, ')'))
        return new_state

    def turn(self, turn_angle, state):
        new_state = RobotState(
            state.x,
            state.y,
            state.angle + turn_angle,
            state.state)
        self.transfer(('ANGLE', state.angle))
        return new_state

    def set_state(self, new_internal_state, state):
        if new_internal_state == 'water':
            self_state = WATER
        elif new_internal_state == 'soap':
            self_state = SOAP
        elif new_internal_state == 'brush':
            self_state = BRUSH
        else:
            return state
        new_state = RobotState(
            state.x,
            state.y,
            state.angle,
            self_state)
        self.transfer(('STATE', self_state))
        return new_state

    def start(self, state):
        self.transfer(('START WITH', state.state))
        return state

    # конец чистки
    def stop(self, state):
        self.transfer(('STOP',))
        return state