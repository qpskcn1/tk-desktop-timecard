import logging
from copy import deepcopy
from timeperiod import TimePeriod

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def filter_keyvals(events, key, vals, exclude=False):
    def p(e):
        # The xor here is a bit tricky, but works nicely
        return exclude ^ any(map(lambda v: e[key] == v, vals))

    return list(filter(p, events))


def filter_short(events, threshold=1):
    # TODO: Try to fill hole in timeline where events have been removed
    #       (if events before and after where are the same)
    #       Useful for filtering AFK data and to make data look "smoother".
    #       Might be something for another function
    return [e for e in events if e.duration.total_seconds() > threshold]


def filter_datafields(events, fields):
    """Filters away specific datafield from every event in a list"""
    for e in events:
        for field in fields:
            if field in e.data:
                e.data.pop(field)
    return events


def _get_event_period(event):
    # TODO: Better parsing of event duration
    start = event.timestamp
    end = start + event.duration
    return TimePeriod(start, end)


def _replace_event_period(event, period):
    e = deepcopy(event)
    e.timestamp = period.start
    e.duration = period.duration
    return e


def filter_period_intersect(events, filterevents):
    """
    Filters away all events or time periods of events in which a
    filterevent does not have an intersecting time period.

    Useful for example when you want to filter away events or
    part of events during which a user was AFK.

    Example:
      windowevents_notafk = filter_period_intersect(windowevents, notafkevents)
    """

    events = sorted(events, key=lambda e: e.timestamp)
    filterevents = sorted(filterevents, key=lambda e: e.timestamp)
    filtered_events = []

    e_i = 0
    f_i = 0
    while e_i < len(events) and f_i < len(filterevents):
        event = events[e_i]
        filterevent = filterevents[f_i]
        ep = _get_event_period(event)
        fp = _get_event_period(filterevent)

        ip = ep.intersection(fp)
        if ip:
            # If events itersected, add event with intersected duration and try next event
            filtered_events.append(_replace_event_period(event, ip))
            e_i += 1
        else:
            # No intersection, check if event is before/after filterevent
            if ep.end <= fp.start:
                # Event ended before filter event started
                e_i += 1
            elif fp.end <= ep.start:
                # Event started after filter event ended
                f_i += 1
            else:
                logger.warning("Unclear if/how this could be reachable, skipping period")
                e_i += 1
                f_i += 1

    return filtered_events
