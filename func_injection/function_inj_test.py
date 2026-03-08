import pure_robot

# класс Чистильщик API
class CleanerApi:

    # конструктор
    def __init__(self):
        self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
        self.move = pure_robot.move
        self.turn = pure_robot.turn
        self.set_state = pure_robot.set_state
        self.start = pure_robot.start
        self.stop = pure_robot.stop

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
                self.cleaner_state = self.move(self.transfer_to_cleaner,
                    int(cmd[1]),self.cleaner_state)
            elif cmd[0]=='turn':
                self.cleaner_state = self.turn(self.transfer_to_cleaner,
                    int(cmd[1]),self.cleaner_state)
            elif cmd[0]=='set':
                self.cleaner_state = self.set_state(self.transfer_to_cleaner,
                    cmd[1],self.cleaner_state)
            elif cmd[0]=='start':
                self.cleaner_state = self.start(self.transfer_to_cleaner,
                    self.cleaner_state)
            elif cmd[0]=='stop':
                self.cleaner_state = self.stop(self.transfer_to_cleaner,
                    self.cleaner_state)