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
        ("Nuke 1 Hour", datetime.date(2017,12,9), datetime.timedelta(hours=1)),
        ("Maya 2 Hour", datetime.date(2017,5,3), datetime.timedelta(hours=2)),
        ("Nuke Studio 2.2 Hour", datetime.date(2017,4,6), datetime.timedelta(hours=2.2))):
            self.list.append(awevent(name, timestamp, duration))
        self.setSupportedDragActions(QtCore.Qt.MoveAction)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.list)

    def data(self, index, role=QtCore.Qt.UserRole):
        if role == QtCore.Qt.DisplayRole:  # show just the name
            awevent = self.list[index.row()]
            return awevent.name
        elif role == QtCore.Qt.UserRole:  # return the whole python object
            awevent = self.list[index.row()]
            return awevent
        else:
            return

    def removeRow(self, position):
        self.list = self.list[:position] + self.list[position + 1:]
        self.reset()

    def getAWdata(self):
        # sampleEvent = Event(id=1,
        #                     timestamp=datetime.now,
        #                     duration=timedelta(hours=2),
        #                     data={})
        sampleEvent = {"timestamp": datetime.now, "duration": timedelta(hours=2)}
        self.list.append(sampleEvent)