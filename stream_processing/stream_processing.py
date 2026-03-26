import threading


@dataclass
class RobotState:
    x: float
    y: float
    angle: float
    state: int


class CleaningMode(Enum):
    WATER = 1
    SOAP = 2
    BRUSH = 3


class Event(ABC):
    @abstractmethod
    def apply(self, state: RobotState) -> RobotState:
        pass

    @abstractmethod
    def get_event_type(self) -> str:
        pass

class RqEvent(Event):
    @abstractmethod
    def getRqBody(self) -> Dict[str, Any]:
        pass

@dataclass
class RobotMovedEventRq(RqEvent):
    distance: float

    def getRqBody(self) -> Dict[str, Any]:
        return {'distance': self.distance}

    def apply(self, state: RobotState) -> RobotState:
        pass

    def get_event_type(self) -> str:
        return 'ROBOT_MOVED_RQ'

@dataclass
class RobotMovedEvent(Event):
    distance: float

    def apply(self, state: RobotState) -> RobotState:
        angle_rads = state.angle * (math.pi / 180.0)
        return RobotState(
            x=state.x + self.distance * math.cos(angle_rads),
            y=state.y + self.distance * math.sin(angle_rads),
            angle=state.angle,
            state=state.state
        )

    def get_event_type(self) -> str:
        return f'ROBOT_MOVED {self.distance}'

@dataclass
class RobotTurnedEventRq(RqEvent):
    angle: float

    def getRqBody(self) -> Dict[str, Any]:
        return {'angle': self.angle}

    def apply(self, state: RobotState) -> RobotState:
        pass

    def get_event_type(self) -> str:
        return 'ROBOT_TURNED_RQ'

@dataclass
class RobotTurnedEvent(Event):
    angle: float

    def apply(self, state: RobotState) -> RobotState:
        return RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle + self.angle,
            state=state.state
        )

    def get_event_type(self) -> str:
        return f'ROBOT_TURNED {self.angle}'

@dataclass
class RobotStateChangedEventRq(RqEvent):
    new_state: CleaningMode

    def getRqBody(self) -> Dict[str, Any]:
        return {'new state': self.new_state.value}

    def apply(self, state: RobotState) -> RobotState:
        pass

    def get_event_type(self) -> str:
        return 'ROBOT_STATE_CHANGED_RQ'


@dataclass
class RobotStateChangedEvent(Event):
    new_state: CleaningMode

    def apply(self, state: RobotState) -> RobotState:
        return RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle,
            state=self.new_state.value
        )

    def get_event_type(self) -> str:
        return f'ROBOT_STATE_CHANGED {self.new_state.name}'

@dataclass
class RobotStartedEventRq(RqEvent):
    def getRqBody(self) -> Dict[str, Any]:
        return {}

    def apply(self, state: RobotState) -> RobotState:
        pass

    def get_event_type(self) -> str:
        return 'ROBOT_STARTED_RQ'

@dataclass
class RobotStartedEvent(Event):
    def apply(self, state: RobotState) -> RobotState:
        return state

    def get_event_type(self) -> str:
        return 'ROBOT_STARTED'


@dataclass
class RobotStoppedEventRq(RqEvent):
    def getRqBody(self) -> Dict[str, Any]:
        return {}

    def apply(self, state: RobotState) -> RobotState:
        return state

    def get_event_type(self) -> str:
        return 'ROBOT_STOPPED_RQ'

@dataclass
class RobotStoppedEvent(Event):
    def apply(self, state: RobotState) -> RobotState:
        pass

    def get_event_type(self) -> str:
        return 'ROBOT_STOPPED'


class Command(Protocol):
    def handle(self, current_state: RobotState) -> List[RqEvent]:
        pass

    def get_command_type(self) -> str:
        pass


@dataclass
class MoveCommand:
    distance: float

    def handle(self, current_state: RobotState) -> List[RqEvent]:
        return [RobotMovedEventRq(self.distance)]

    def get_command_type(self) -> str:
        return f'MOVE {self.distance}'


@dataclass
class TurnCommand:
    angle: float

    def handle(self, current_state: RobotState) -> List[RqEvent]:
        return [RobotTurnedEventRq(self.angle)]

    def get_command_type(self) -> str:
        return f'TURN {self.angle}'


@dataclass
class SetStateCommand:
    new_state: CleaningMode

    def handle(self, current_state: RobotState) -> List[RqEvent]:
        return [RobotStateChangedEventRq(self.new_state)]

    def get_command_type(self) -> str:
        return f'SET_STATE {self.new_state.name}'


@dataclass
class StartCommand:
    def handle(self, current_state: RobotState) -> List[RqEvent]:
        return [RobotStartedEventRq()]

    def get_command_type(self) -> str:
        return 'START'


@dataclass
class StopCommand:
    def handle(self, current_state: RobotState) -> List[RqEvent]:
        return [RobotStoppedEventRq()]

    def get_command_type(self) -> str:
        return 'STOP'


class EventStore:
    def __init__(self, move_q, turn_q, state_q, start_q, stop_q, out_q):
        self._events: Dict[str, List[Event]] = {}
        self.queues = {
            'ROBOT_MOVED_RQ': move_q,
            'ROBOT_TURN_RQ': turn_q,
            'ROBOT_STARTED_RQ': start_q,
            'ROBOT_STOPPED_RQ': stop_q,
            'ROBOT_STATE_CHANGED_RQ': state_q
        }

        self.out_q = out_q

    def append_events(self, robot_id: str, events: List[RqEvent]) -> None:
        if robot_id not in self._events:
            self._events[robot_id] = []

        for event in events:
            queue = self.queues[event.get_event_type()]
            queue.put(event)
            res_event = self.out_q.get()
            self.out_q.task_done()
            self._events[robot_id].append(res_event)

    def get_events(self, robot_id: str) -> List[Event]:
        return self._events.get(robot_id, [])

    def get_events_from_version(self, robot_id: str, from_version: int) -> List[Event]:
        events = self.get_events(robot_id)
        return events[from_version:] if from_version < len(events) else []


class StateProjector:
    def __init__(self, initial_state: RobotState):
        self._initial_state = initial_state

    def project_state(self, events: List[Event]) -> RobotState:
        current_state = self._initial_state
        for event in events:
            current_state = event.apply(current_state)
        return current_state


class CommandHandler:
    def __init__(self, event_store: EventStore, state_projector: StateProjector):
        self._event_store = event_store
        self._state_projector = state_projector

    def handle_command(self, robot_id: str, command: Command):
        new_events = command.handle(current_state)

        if new_events:
            self._event_store.append_events(robot_id, new_events)

    def get_result(self, robot_id: str) -> RobotState:
        all_events = self._event_store.get_events(robot_id)
        return self._state_projector.project_state(all_events)

class MoveEventProcessor(threading.Thread):
    def __init__(self, queue, out_queue):
        threading.Thread.__init__(self)
        self._queue = queue
        self._out_queue = out_queue

    def run(self):
        while True:
            event = self._queue.get()
            self._out_queue.put(RobotMovedEvent(event.distance))
            self._queue.task_done()

class TurnEventProcessor(threading.Thread):
    def __init__(self, queue, out_queue):
        threading.Thread.__init__(self)
        self._queue = queue
        self._out_queue = out_queue

    def run(self):
        while True:
            event = self._queue.get()
            self._out_queue.put(RobotTurnedEvent(event.angle))
            self._queue.task_done()

class StateEventProcessor(threading.Thread):
    def __init__(self, queue, out_queue):
        threading.Thread.__init__(self)
        self._queue = queue
        self._out_queue = out_queue

    def run(self):
        while True:
            event = self._queue.get()
            self._out_queue.put(RobotStateChangedEvent(event.state))
            self._queue.task_done()

class StartEventProcessor(threading.Thread):
    def __init__(self, queue, out_queue):
        threading.Thread.__init__(self)
        self._queue = queue
        self._out_queue = out_queue

    def run(self):
        while True:
            event = self._queue.get()
            self._out_queue.put(RobotStartedEvent())
            self._queue.task_done()

class StopEventProcessor(threading.Thread):
    def __init__(self, queue, out_queue):
        threading.Thread.__init__(self)
        self._queue = queue
        self._out_queue = out_queue

    def run(self):
        while True:
            event = self._queue.get()
            self._out_queue.put(RobotStoppedEvent())
            self._queue.task_done()


