# Navsari → Mumbai: Best Time to Leave

Tracks live traffic-aware travel time between Navsari and Mumbai every 15
minutes using the TomTom Routing API, and builds a report showing which
hours/days are historically fastest to leave.

## Setup

```
pip install -r requirements.txt
cp .env.example .env   # then fill in TOMTOM_API_KEY
```

## Collecting data

Run once manually to test:

```
python poll.py
```

Then schedule it every 15 minutes with cron:

```
*/15 * * * * cd /path/to/word-saver && /path/to/python poll.py >> poll.log 2>&1
```

Each run appends a sample (timestamp, travel time, traffic delay) to
`data/travel.db` (SQLite).

## Generating the report

Once you've collected some data (a few days gives meaningful hour-of-day
patterns; a few weeks gives meaningful day-of-week patterns):

```
python report.py
```

This writes `report.html` — open it in a browser to see:
- Average travel time by hour of day
- Average travel time by day of week + hour
- The best and worst hour to leave overall

Re-run `report.py` any time (e.g. also via cron, daily) to refresh it with
the latest data.
