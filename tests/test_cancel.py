import pytest
from tests.helper import set_all, events_tester
from multievent import (
    wait_for_multiple_events,
    MODE_ANY,
    MODE_ALL,
    MODE_COUNT,
    CancelWait,
    ReuseCancelWaitError,
)


def test_any_with_cancel():
    with events_tester(5) as events:
        cancel = CancelWait()
        wait = wait_for_multiple_events(events, mode=MODE_ANY, cancel=cancel)
        cancel()
        wait()


def test_all_with_cancel():
    with events_tester(5) as events:
        cancel = CancelWait()
        wait = wait_for_multiple_events(events, mode=MODE_ALL, cancel=cancel)
        cancel()
        wait()


def test_count_with_cancel():
    with events_tester(5) as events:
        cancel = CancelWait()
        wait = wait_for_multiple_events(events, mode=MODE_COUNT, count=3, cancel=cancel)
        cancel()
        wait()


def test_cancel_reuse():
    cancel = CancelWait()
    with events_tester(5) as events:
        wait = wait_for_multiple_events(events, mode=MODE_ANY, cancel=cancel)
        set_all(events)
        wait()
        with events_tester(5) as events2:
            with pytest.raises(ReuseCancelWaitError):
                wait_for_multiple_events(events2, mode=MODE_ANY, cancel=cancel)
