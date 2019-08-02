import pytest
from tests.helper import set_all, events_tester
from multievent import wait_for_multiple_events, MODE_COUNT


@pytest.mark.parametrize("n", [2, 5, 15])
def test_count_basic(n):
    with events_tester(n) as events:
        wait = wait_for_multiple_events(events, mode=MODE_COUNT, count=n)
        events[0].set()
        assert not wait(0.1)
        set_all(events)
        wait()


@pytest.mark.parametrize("n", [2, 5, 15])
def test_count_set(n):
    count = int(n / 2)
    with events_tester(n) as events:
        wait = wait_for_multiple_events(events, mode=MODE_COUNT, count=count)
        for i in range(0, count - 1):
            events[i].set()
        assert not wait(0.1)
        events[count - 1].set()
        wait()


@pytest.mark.parametrize("v", [(1, 0), (1, -1), (5, 6)])
def test_count_invalid_ranges(v):
    n, c = v
    with events_tester(n) as events:
        with pytest.raises(AssertionError):
            wait_for_multiple_events(events, mode=MODE_COUNT, count=c)
