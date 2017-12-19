from math import ceil

import sgtk
from datetime import datetime, timedelta, date
from sgtk.platform.qt import QtCore, QtGui

import aw_client
from aw_core.transforms import full_chunk, filter_keyvals

logger = sgtk.platform.get_logger(__name__)


class awevent(object):
    '''
    a custom data structure for AW data
    '''
    def __init__(self, name, timestamp, duration):
        self.name = name
        self.timestamp = timestamp
        self.duration = duration
    def __repr__(self):
        return "{name: %s, date: %s, duration: %s}"% (self.name, self.timestamp, self.duration)

    def subtract_logged_time(self, logged_time):
        self.duration = self.duration - self.logged_time

class MyTimeModel(QtCore.QAbstractListModel):

    # def __init__(self, parent=None):
    #     super(MyTimeModel, self).__init__(parent)
    #     self.list = []
    #     self.getAWdata()
    #     self.setSupportedDragActions(QtCore.Qt.MoveAction)
    def __init__(self, parent=None):
        super(MyTimeModel, self).__init__(parent)
        self.list = []
        awdata = self._getAWdata()
        filtered_data = self.eventFilter(awdata)
        for name in filtered_data:
            duration = filtered_data[name]
            self.list.append(awevent(name, date.today(), duration))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.list)

    def data(self, index, role=QtCore.Qt.UserRole):
        if role == QtCore.Qt.DisplayRole:  # show just the name
            awevent = self.list[index.row()]
            duration = ceil(awevent.duration.total_seconds() / 360) / 10
            return "{0} {1:.1f}hrs".format(awevent.name, duration)
        elif role == QtCore.Qt.UserRole:  # return the whole python object
            awevent = self.list[index.row()]
            return awevent
        else:
            return

    def removeRow(self, position):
        event = self.data(position)
        logger.debug("Time left: {}".format(event.duration))
        if event.duration <= timedelta(0):
            self.list = self.list[:position] + self.list[position + 1:]
            self.reset()

    def _getAWdata(self):
        try:
            client = aw_client.ActivityWatchClient()
            logger.debug("ActivityWatchClient Connected")
            starttime = datetime.now().replace(hour=0, minute=0)
            endtime = starttime.replace(hour=23, minute=59)
            windowevents = client.get_events("aw-watcher-window_OFG-TESTBENCH",
                                             start=starttime,
                                             end=endtime,
                                             limit=-1)
            chunk_result = full_chunk(windowevents, "app", False)
            return chunk_result.chunks
        except Exception as e:
            logger.error(e)
            return None

    def eventFilter(self, data):
        filtered_event = {"other": timedelta(0)}
        for event in data:
            duration = data[event]['duration']
            if duration < timedelta(0, 360, 0):
                filtered_event["other"] += duration
            else:
                name = event
                if ".exe" in event:
                    name = event.replace(".exe", "")
                filtered_event[name] = duration

        return filtered_event