import pytest
import threading
from tests.helper import set_all, events_tester
from multievent import wait_for_multiple_events, MODE_ALL


@pytest.mark.parametrize("n", [2, 5, 15])
def test_all_basic(n):
    with events_tester(n) as events:
        wait, _ = wait_for_multiple_events(events, mode=MODE_ALL)
        events[0].set()
        assert not wait(0.1)
        set_all(events)
        wait()


@pytest.mark.parametrize("n", [2, 5, 15])
def test_all_set_few(n):
    with events_tester(n) as events:
        wait, _ = wait_for_multiple_events(events, mode=MODE_ALL)
        for i in range(0, n - 1):
            events[i].set()
        assert not wait(0.1)
        set_all(events)
        wait()


def test_any_stopper():
    with events_tester(5) as events:
        wait, stop = wait_for_multiple_events(events, mode=MODE_ALL)
        t = threading.Thread(target=stop)
        t.start()
        wait()
        t.join()
