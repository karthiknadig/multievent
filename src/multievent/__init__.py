import threading
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


MODE_ANY = 1
MODE_ALL = 2
MODE_COUNT = 3


class ReuseCancelWaitError(Exception):
    pass


class CancelWait(object):
    def __init__(self):
        self._event = None

    def cancel(self):
        if self._event:
            self._event.set()

    def _setup(self, e):
        if self._event is not None:
            raise ReuseCancelWaitError()
        self._event = e

    def __call__(self):
        self.cancel()


def wait_for_multiple_events(events, mode=MODE_ANY, count=0, cancel=None):
    """Helper to wait for multiple events based on a trigger criteria.
    Parameters
    ----------
    events : iterable
        An iterable object containing the events to monitor

    mode : enum(MODE_ANY, MODE_ALL, MODE_COUNT)
        MODE_ANY - waiter returns when any event in the collection is set.
        MODE_ALL - waiter returns when all events in the collection are set.
        MODE_COUNT - waiter returns when a specified number of events are set.

    count : integer
        Number of events to wait on when using MODE_COUNT.

    cancel : CancelWait
        Allows cancelling the wait.

    Return
    ------
    Returns a wait function. Waiter can be called multiple times when using timeout.
    The wait functions behaves same as the threading.Event.wait(). You can cancel wait,
    using the CancelWait instance passed to wait_for_multiple_events.
    """
    assert mode and mode in (MODE_ANY, MODE_ALL, MODE_COUNT)
    assert events and (len(events) > 0 and len(events) < 16)
    if mode == MODE_COUNT:
        assert count and count > 0 and count <= len(events)

    class Counter():
        def __init__(self):
            self._value = 0

        def increment(self):
            self._value += 1
        
        @property
        def value(self):
            return self._value

    _events = list(events)
    _counter_lock = threading.Lock()
    _counter = Counter()
    _core_event = threading.Event()
    _core_event.clear()
    _threads = []
    if cancel is not None:
        cancel._setup(_core_event)

    def __check():
        with _counter_lock:
            if mode == MODE_ANY:
                if _counter.value > 0:
                    _core_event.set()
            elif mode == MODE_COUNT:
                if _counter.value >= count:
                    _core_event.set()
            elif mode == MODE_ALL:
                if _counter.value == len(_events):
                    _core_event.set()

    def __wait(timeout=None):
        return _core_event.wait(timeout)

    def __worker(e):
        while not (e.is_set() or _core_event.is_set()):
            e.wait(0.1)
        with _counter_lock:
            if e.is_set():
                _counter.increment()
        __check()

    for e in _events:
        _threads.append(threading.Thread(target=__worker, args=(e,)))
    for t in _threads:
        t.start()

    return __wait
