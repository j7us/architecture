import pure_robot

class RobotApi:

    def setup(self, command_function):
        self.command_function = command_function

    def make(self, command):
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

        cmd = command.split(' ')

        self.cleaner_state = self.command_function(cmd)

        return self.cleaner_state

    def __call__(self, command):
        return self.make(command)


def transfer_to_cleaner(message):
    print (message)

def double_move(transfer,dist,state):
    return pure_robot.move(transfer,dist*2,state)




def test_func(cmd, f_transfer, cleaner_state):
    if cmd[0] == 'move':
        cleaner_state = f_move(f_transfer, int(cmd[1]), cleaner_state)
    elif cmd[0] == 'turn':
        cleaner_state = f_turn(f_transfer, int(cmd[1]), cleaner_state)
    elif cmd[0] == 'set':
        cleaner_state = f_set_state(self.f_transfer, cmd[1], cleaner_state)
    elif cmd[0] == 'start':
        cleaner_state = f_start(f_transfer, cleaner_state)
    elif cmd[0] == 'stop':
        cleaner_state = f_stop(f_transfer, cleaner_state)
    return cleaner_state

api = RobotApi()
api.setup(test_func)
