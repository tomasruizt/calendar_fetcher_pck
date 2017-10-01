# calendar_fetcher_pck
Fetch information from your Google Calendar

## Installation
```
git clone https://github.com/tomasruizt/calendar_fetcher_pckg
cd calendar_fetcher_pckg
pip install .
```

## Getting Started
Minimal Python example:
```python
from calendar_fetcher_pckg import GoogleCalendarService
import datetime

secrets_path = "/usr/secrets.json"
cal = GoogleCalendarService(secrets_path)

today = datetime.datetime.today()
events = cal.get_events(
    start_date=today - datetime.timedelta(days=7),
    end_date=today)

for e in events:
    print(e['summary'])

```
## Uninstalling
```
calendar_fetcher_pckg
```
