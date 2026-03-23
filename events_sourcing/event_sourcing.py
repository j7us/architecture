import pure_robot

class Event:
    def __init__(self, event_type, event_data):
        self.event_type = event_type
        self.event_data = event_data

class CommandHandler:

    def __init__(self):
        self.event_store = []

    def transfer_to_cleaner(self, message):
        print(message)

    def handle(self, command):
        state = self.build_state()

        cmd = command.split(' ')

        if cmd[0] == 'move':
            cleaner_state = pure_robot.move(self.transfer_to_cleaner, int(cmd[1]), state)
            self.event_store.append(Event('move', str(cleaner_state.x) + '_' + str(cleaner_state.y)))
        elif cmd[0] == 'turn':
            cleaner_state = pure_robot.turn(self.transfer_to_cleaner, int(cmd[1]), state)
            self.event_store.append(Event('turn', str(cleaner_state.angle)))
        elif cmd[0] == 'set':
            cleaner_state = pure_robot.set_state(self.transfer_to_cleaner, cmd[1], state)
            self.event_store.append(Event('set', str(cleaner_state.state)))
        elif cmd[0] == 'start':
            cleaner_state = pure_robot.start(self.transfer_to_cleaner, state)
            self.event_store.append(Event('start', None))
        elif cmd[0] == 'stop':
            cleaner_state = pure_robot.stop(self.transfer_to_cleaner, state)
            self.event_store.append(Event('stop', None))

    def build_state(self):
        cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

        for event in self.event_store:
            if event.event_type == 'move':
                x, y = event.event_data.split("_")
                cleaner_state.x = int(x)
                cleaner_state.y = int(y)
            elif event.event_type == 'turn':
                cleaner_state.angle = int(event.event_data)
            elif event.event_type == 'state':
                cleaner_state.state = event.event_data
