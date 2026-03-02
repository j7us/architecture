import pure_robot

# класс Чистильщик API
class CleanerApi:

    # конструктор
    def __init__(self, state_repository):
        self.state_repository = state_repository

    # взаимодействие с роботом вынесено в отдельную функцию
    def transfer_to_cleaner(self,message):
        print (message)

    def get_x(self, user_id):
        return self.state_repository.get_state(user_id).x

    def get_y(self, user_id):
        return self.state_repository.get_state(user_id).y

    def get_angle(self, user_id):
        return self.state_repository.get_state(user_id).angle

    def get_state(self, user_id):
        return self.state_repository.get_state(user_id).state

    def activate_cleaner(self,code, user_id):
        start_state = self.state_repository.get_state(user_id)

        for command in code:
            cmd = command.split(' ')
            if cmd[0]=='move':
                cleaner_state = pure_robot.move(self.transfer_to_cleaner,
                    int(cmd[1]),start_state)
            elif cmd[0]=='turn':
                cleaner_state = pure_robot.turn(self.transfer_to_cleaner,
                    int(cmd[1]),start_state)
            elif cmd[0]=='set':
                cleaner_state = pure_robot.set_state(self.transfer_to_cleaner,
                    cmd[1],start_state)
            elif cmd[0]=='start':
                cleaner_state = pure_robot.start(self.transfer_to_cleaner,
                    start_state)
            elif cmd[0]=='stop':
                cleaner_state = pure_robot.stop(self.transfer_to_cleaner,
                    start_state)

            self.state_repository.save(cleaner_state, user_id)