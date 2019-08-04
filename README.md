# multievent


|     |   |
|-----|---|
|License |[![GitHub](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://raw.githubusercontent.com/karthiknadig/multievent/master/LICENSE)|
|Info |[![PyPI](https://img.shields.io/pypi/v/multievent.svg)](https://pypi.org/project/multievent/) [![PyPI](https://img.shields.io/pypi/pyversions/multievent.svg)](https://pypi.org/project/multievent/)|
|Tests|[![Build Status](https://dev.azure.com/c0d3r/multievent/_apis/build/status/multievent-CI?branchName=master)](https://dev.azure.com/c0d3r/multievent/_build/latest?definitionId=2&branchName=master) [![PyPI](https://img.shields.io/azure-devops/coverage/c0d3r/multievent/4.svg)](https://pypi.org/project/multievent/)|

`multievent` provides a easy API to wait on multiple events.

### Installtion
```console
python -m pip install git+https://github.com/karthiknadig/multievent
```

### Usage
```py
events = [threading.Event() for _ in range(0, 5)]

# Default is ANY
wait = wait_for_multiple_events(events) 

# wait blocks until one of the events is set.
wait()
```

#### Wait for all events
```py
events = [threading.Event() for _ in range(0, 5)]

# Default is ANY
wait = wait_for_multiple_events(events, mode=MODE_ALL) 

# wait blocks until all of the events are set.
wait()
```

#### Cancel wait
```py
events = [threading.Event() for _ in range(0, 5)]

cancel = CancelWait()
# Default is ANY
wait = wait_for_multiple_events(events, cancel=cancel) 

def _run_this():
    time.sleep(5)
    cancel()  # see NOTE below.

t = threading.Thread(target=_run_this)
t.start()

# wait is blocked until either one of the events is set or
# cancel is called
wait()
# NOTE: Cancellation ends all monitoring. You have to call
# wait_for_multiple_events, and get a new wait function.
```

#### Wait for specified count of events

```py
events = [threading.Event() for _ in range(0, 5)]

# Default is ANY
wait = wait_for_multiple_events(events, mode=MODE_COUNT, count=3) 

# wait blocks until three events are set.
wait()
```