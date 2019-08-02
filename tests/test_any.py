import pytest
import threading
from tests.helper import events_tester
from multievent import wait_for_multiple_events, MODE_ANY


@pytest.mark.parametrize("n", [1, 5])
def test_any_basic(n):
    with events_tester(n) as events:
        wait, _ = wait_for_multiple_events(events, mode=MODE_ANY)
        events[0].set()
        wait()


@pytest.mark.parametrize("n", [1, 5])
def test_any_with_timeout(n):
    with events_tester(n) as events:
        wait, _ = wait_for_multiple_events(events, mode=MODE_ANY)
        assert not wait(0.01)
        events[0].set()
        wait()


def test_any_stopper():
    with events_tester(5) as events:
        wait, stop = wait_for_multiple_events(events, mode=MODE_ANY)
        t = threading.Thread(target=stop)
        t.start()
        wait()
        t.join()


@pytest.mark.parametrize("n", [0, 16, 17, 100])
def test_any_invalid(n):
    with events_tester(n) as events:
        with pytest.raises(AssertionError):
            wait_for_multiple_events(events, mode=MODE_ANY)
