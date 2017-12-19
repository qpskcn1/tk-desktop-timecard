#impot sgtk
import json
import numbers
import logging
from datetime import datetime, timedelta
import iso8601
import pytz

# logger = sgtk.platform.get_logger(__name__)
logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter("%(levelname)s - %(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)


def _timestamp_parse(ts):
    """
    Takes something representing a timestamp and
    returns a timestamp in the representation we want.
    """
    if isinstance(ts, unicode):
        ts = str(ts)
    if isinstance(ts, str):
        ts = iso8601.parse_date(ts)
    # Set resolution to milliseconds instead of microseconds
    # (Fixes incompability with software based on unix time, for example mongodb)
    ts = ts.replace(microsecond=int(ts.microsecond / 1000) * 1000)
    # Add timezone if not set
    if not ts.tzinfo:
        # Needed? All timestamps should be iso8601 so ought to always contain timezone.
        # Yes, because it is optional in iso8601
        logger.warning("timestamp without timezone found, using UTC: {}".format(ts))
        ts = ts.replace(tzinfo=pytz.utc)
    return ts


class Event(dict):
    """
    Used to represents an events.
    """

    def __init__(self, id=None, timestamp=None, duration=0, data={}):
        self.id = id
        if timestamp is None:
            logger.warning("Event initializer did not receive a timestamp argument, using now as timestamp")
            self.timestamp = datetime.utcnow()
        else:
            self.timestamp = _timestamp_parse(timestamp)
        self.duration = duration
        self.data = data

    def __eq__(self, other):
        return self.timestamp == other.timestamp\
            and self.duration == other.duration\
            and self.data == other.data

    def to_json_dict(self):
        """
        Useful when sending data over the wire.
        Any mongodb interop should not use do this as it accepts datetimes."""
        json_data = self.copy()
        json_data["timestamp"] = self.timestamp.astimezone(pytz.utc).isoformat()
        json_data["duration"] = self.duration.total_seconds()
        return json_data

    def to_json_str(self):
        data = self.to_json_dict()
        return json.dumps(data)

    def _hasprop(self, propname):
        """Badly named, but basically checks if the underlying
        dict has a prop, and if it is a non-empty list"""
        return propname in self and self[propname] is not None

    @property
    def id(self):
        return self["id"] if self._hasprop("id") else None

    @id.setter
    def id(self, id):
        self["id"] = id

    @property
    def data(self):
        return self["data"] if self._hasprop("data") else {}

    @data.setter
    def data(self, data):
        self["data"] = data

    @property
    def timestamp(self):
        return self["timestamp"]

    @timestamp.setter
    def timestamp(self, timestamp):
        self["timestamp"] = _timestamp_parse(timestamp).astimezone(pytz.utc)

    @property
    def duration(self):
        return self["duration"] if self._hasprop("duration") else timedelta(0)

    @duration.setter
    def duration(self, duration):
        if type(duration) == timedelta:
            self["duration"] = duration
        elif isinstance(duration, numbers.Real):
            self["duration"] = timedelta(seconds=duration)  # type: ignore
        else:
            logger.error("Couldn't parse duration of invalid type {}".format(type(duration)))
