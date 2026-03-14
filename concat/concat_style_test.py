import pure_robot

class Concat:
    def __init__(self):
        self.commands = {
            'move': pure_robot.move,
            'turn': pure_robot.turn,
            'set_state': pure_robot.set_state,
            'start': pure_robot.start,
            'stop': pure_robot.stop
        }

        self.command_parts = Stack()
        self.command_vars = Stack()

    def transfer_to_cleaner(message):
        print(message)

    def execute(self, command):
        postf_list = command.split(' ')
        postf_list.reverse()

        for i in postf_list:
            self.command_parts.push(i)

        cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

        while self.command_parts.size() > 0:
            sym = self.command_parts.pop()

            com = self.commands[sym]

            if com is None:
                self.command_vars.push(sym)
                continue

            com_var = self.command_vars.pop()

            cleaner_state = com(self.transfer_to_cleaner, cleaner_state) if com_var is None else com(self.transfer_to_cleaner, com_var, cleaner_state)

        return cleaner_state

class Stack:
    def __init__(self):
        self.stack = []
        self.count = 0

    def size(self):
        return len(self.stack)

    def pop(self):
        if self.count == 0:
            return None

        deleted_element = self.stack.pop(0)
        self.count -= 1
        return deleted_element

    def push(self, value):
        self.stack.insert(0, value)
        self.count += 1

    def peek(self):
        return self.stack[0] if self.count > 0 else None


