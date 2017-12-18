import sgtk
import datetime
from sgtk.platform.qt import QtCore, QtGui
# from ..aw_core.models import Event

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
        for name, timestamp, duration in (
        ("Nuke", datetime.date(2017,12,9), datetime.timedelta(hours=1)),
        ("Maya", datetime.date(2017,5,3), datetime.timedelta(hours=2)),
        ("Nuke Studio", datetime.date(2017,4,6), datetime.timedelta(hours=2.2))):
            self.list.append(awevent(name, timestamp, duration))
        self.setSupportedDragActions(QtCore.Qt.MoveAction)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.list)

    def data(self, index, role=QtCore.Qt.UserRole):
        if role == QtCore.Qt.DisplayRole:  # show just the name
            awevent = self.list[index.row()]
            duration = awevent.duration.total_seconds() / 3600
            return "{} {}hrs".format(awevent.name, duration)
        elif role == QtCore.Qt.UserRole:  # return the whole python object
            awevent = self.list[index.row()]
            return awevent
        else:
            return

    def removeRow(self, position):
        event = self.data(position)
        logger.debug("Time left: {}".format(event.duration))
        if event.duration <= datetime.timedelta(0):
            self.list = self.list[:position] + self.list[position + 1:]
            self.reset()

    def getAWdata(self):
        # sampleEvent = Event(id=1,
        #                     timestamp=datetime.now,
        #                     duration=timedelta(hours=2),
        #                     data={})
        sampleEvent = {"timestamp": datetime.now, "duration": timedelta(hours=2)}
        self.list.append(sampleEvent)