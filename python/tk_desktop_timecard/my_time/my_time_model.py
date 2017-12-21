import os
from math import ceil

import sgtk
from datetime import datetime, timedelta, date
from sgtk.platform.qt import QtCore, QtGui

import aw_client
from aw_core.transforms import full_chunk

from .aw_event import AWEvent

logger = sgtk.platform.get_logger(__name__)


class MyTimeModel(QtCore.QAbstractListModel):

    def __init__(self, checkedin, parent=None):
        super(MyTimeModel, self).__init__(parent)
        self.list = []
        if checkedin:
            awdata = self._getAWdata()
            if awdata:
                filtered_data = self._eventFilter(awdata)
                for name in filtered_data:
                    duration = filtered_data[name]
                    self.list.append(AWEvent(name, date.today(), duration))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.list)

    def data(self, index, role=QtCore.Qt.UserRole):
        if role == QtCore.Qt.DisplayRole:  # show just the name
            awevent = self.list[index.row()]
            duration = ceil(awevent.duration.total_seconds() / 360) / 10
            if duration < 0:
                duration = "any "
            return "{0} {1}hrs".format(awevent.name, duration)
        elif role == QtCore.Qt.UserRole:  # return the whole python object
            awevent = self.list[index.row()]
            return awevent
        else:
            return

    def addCustomTime(self):
        self.list.append(AWEvent("Custom Time", date.today(), timedelta(-1)))
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def removeRow(self, position):
        event = self.data(position)
        logger.debug("Time left: {}".format(event.duration))
        if event.duration <= timedelta(0):
            self.list = self.list[:position] + self.list[position + 1:]
            self.reset()

    def async_refresh(self):
        self.list = []
        awdata = self._getAWdata()
        if awdata:
            filtered_data = self._eventFilter(awdata)
            for name in filtered_data:
                duration = filtered_data[name]
                self.list.append(AWEvent(name, date.today(), duration))
        QtGui.QApplication.processEvents()
        try:
            self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        except Exception as e:
            logger.error(e)

    def _getAWdata(self):
        try:
            client = aw_client.ActivityWatchClient()
            logger.debug("ActivityWatchClient Connected")
            starttime = datetime.now().replace(hour=0, minute=0)
            endtime = starttime.replace(hour=23, minute=59)
            hostname = os.environ.get("COMPUTERNAME", "unknown")
            windowevents = client.get_events("aw-watcher-window_%s" % hostname,
                                             start=starttime,
                                             end=endtime,
                                             limit=-1)
            chunk_result = full_chunk(windowevents, "app", False)
            return chunk_result.chunks
        except Exception as e:
            logger.error(e)
            return None

    def _eventFilter(self, data):
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
