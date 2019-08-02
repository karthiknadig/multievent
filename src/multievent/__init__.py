import threading

MODE_ANY = 1
MODE_ALL = 2
MODE_COUNT = 3


def wait_for_multiple_events(events, mode=MODE_ANY, count=0, create_thread=threading.Thread):
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

    Return
    ------
    Returns a tuple of wait function and stop function. Waiter can be called multiple
    times when using timeout. Wait function throws TimeoutError when trigger is not
    set within the specified timeout. Stopper can be used to stop monitoring.
    """
    assert mode and mode in (MODE_ANY, MODE_ALL, MODE_COUNT)
    assert events and (len(events) > 0 and len(events) < 16)
    if mode == MODE_COUNT:
        assert count and count > 0 and count <= len(events)

    _events = list(events)
    _set_count_lock = threading.Lock()
    _set_count = 0
    _core_event = threading.Event()
    _core_event.clear()
    _threads = []

    def __check():
        with _set_count_lock:
            if mode == MODE_ANY:
                if _set_count > 0:
                    _core_event.set()
            elif mode == MODE_COUNT:
                if _set_count >= count:
                    _core_event.set()
            elif mode == MODE_ALL:
                if _set_count == len(_events):
                    _core_event.set()

    def __wait(timeout=None):
        return _core_event.wait(timeout)

    # force stop monitoring
    def __stop():
        _core_event.set()

    def __worker(e):
        while not (e.is_set() or _core_event.is_set()):
            if not e.wait(0.1):
                if _core_event.is_set():
                    return
        with _set_count_lock:
            nonlocal _set_count
            if e.is_set():
                _set_count = _set_count + 1
        __check()

    for e in _events:
        _threads.append(threading.Thread(target=__worker, args=(e,)))
    for t in _threads:
        t.start()

    return __wait, __stop
