from collections import defaultdict
from datetime import datetime

from db import fetch_all_samples

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def load_samples():
    samples = []
    for fetched_at, travel_time, delay, length in fetch_all_samples():
        dt = datetime.fromisoformat(fetched_at)
        samples.append(
            {
                "datetime": dt,
                "hour": dt.hour,
                "weekday": dt.weekday(),
                "travel_time_min": travel_time / 60,
                "delay_min": delay / 60,
            }
        )
    return samples


def aggregate_by_hour(samples):
    buckets = defaultdict(list)
    for s in samples:
        buckets[s["hour"]].append(s["travel_time_min"])
    return {hour: sum(times) / len(times) for hour, times in buckets.items()}


def aggregate_by_weekday_hour(samples):
    buckets = defaultdict(list)
    for s in samples:
        buckets[(s["weekday"], s["hour"])].append(s["travel_time_min"])
    return {key: sum(times) / len(times) for key, times in buckets.items()}


def build_report_html(samples):
    if not samples:
        return "<html><body><h1>No data yet</h1><p>Run poll.py a few times first.</p></body></html>"

    by_hour = aggregate_by_hour(samples)
    by_weekday_hour = aggregate_by_weekday_hour(samples)

    best_hour, best_hour_avg = min(by_hour.items(), key=lambda kv: kv[1])
    worst_hour, worst_hour_avg = max(by_hour.items(), key=lambda kv: kv[1])

    hour_rows = "".join(
        f"<tr><td>{hour:02d}:00</td><td>{avg:.1f} min</td></tr>"
        for hour, avg in sorted(by_hour.items())
    )

    weekday_hour_rows = "".join(
        f"<tr><td>{DAY_NAMES[weekday]}</td><td>{hour:02d}:00</td><td>{avg:.1f} min</td></tr>"
        for (weekday, hour), avg in sorted(by_weekday_hour.items())
    )

    latest = max(samples, key=lambda s: s["datetime"])

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Navsari to Mumbai - Best Time to Leave</title>
<style>
body {{ font-family: sans-serif; max-width: 700px; margin: 40px auto; color: #222; }}
h1 {{ font-size: 22px; }}
table {{ border-collapse: collapse; width: 100%; margin-bottom: 30px; }}
th, td {{ border: 1px solid #ddd; padding: 6px 10px; text-align: left; }}
th {{ background: #f5f5f5; }}
.highlight {{ background: #e6ffed; font-weight: bold; }}
.samples {{ color: #666; font-size: 13px; }}
</style>
</head>
<body>
<h1>Navsari &rarr; Mumbai: Best Time to Leave</h1>
<p class="samples">Based on {len(samples)} samples. Latest sample: {latest['datetime'].isoformat()},
travel time {latest['travel_time_min']:.1f} min.</p>

<p><strong>Best hour to leave (avg across all days):</strong> {best_hour:02d}:00 &mdash; {best_hour_avg:.1f} min<br>
<strong>Worst hour to leave:</strong> {worst_hour:02d}:00 &mdash; {worst_hour_avg:.1f} min</p>

<h2>Average travel time by hour of day</h2>
<table>
<tr><th>Hour</th><th>Avg travel time</th></tr>
{hour_rows}
</table>

<h2>Average travel time by day of week and hour</h2>
<table>
<tr><th>Day</th><th>Hour</th><th>Avg travel time</th></tr>
{weekday_hour_rows}
</table>
</body>
</html>
"""


def main():
    samples = load_samples()
    html = build_report_html(samples)
    with open("report.html", "w") as f:
        f.write(html)
    print(f"Report written to report.html ({len(samples)} samples used)")


if __name__ == "__main__":
    main()
