import pytest
from tests.helper import events_tester
from multievent import wait_for_multiple_events, MODE_ANY, MODE_ALL, MODE_COUNT


@pytest.mark.parametrize("mode", [None, 12345])
def test_bad_mode(mode):
    with pytest.raises(AssertionError):
        wait = wait_for_multiple_events([], mode=mode)


@pytest.mark.parametrize("mode", [MODE_ANY, MODE_ALL, MODE_COUNT])
@pytest.mark.parametrize("n", [0, 16, 17, 100])
def test_any_invalid(mode, n):
    with events_tester(n) as events:
        with pytest.raises(AssertionError):
            wait_for_multiple_events(events, mode=mode, count=n)


@pytest.mark.parametrize("mode", [MODE_ANY, MODE_ALL, MODE_COUNT])
@pytest.mark.parametrize("e", [None, []])
def test_bad_event(mode, e):
    with pytest.raises(AssertionError):
        wait_for_multiple_events(e, mode=mode)
