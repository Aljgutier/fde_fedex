from collections import defaultdict


def events_per_user(events):
    counts = defaultdict(int)
    for event in events:
        counts[event.user_id] += 1
    return dict(counts)


def total_value_per_user(events):
    totals = defaultdict(float)
    for event in events:
        totals[event.user_id] += event.value
    return dict(totals)
