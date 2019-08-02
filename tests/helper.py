from threading import Event


def get_events(n):
    events = []
    for _ in range(0, n):
        events.append(Event())
    return events

def set_all(events):
    for e in events:
        e.set()


class events_tester(object):
    def __init__(self, n):
        self.events = get_events(n)
    def __enter__(self):
        return self.events
    def __exit__(self, type, value, traceback):
        set_all(self.events)
  