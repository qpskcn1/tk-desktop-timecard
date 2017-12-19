import datetime
import cPickle
import pickle
import sys
from ui.new_timelog import Ui_NewTimeLogForm

from PySide import QtGui, QtCore

class awevent(object):
    '''
    a custom data structure, for example purposes
    '''
    def __init__(self, name, timestamp, duration):
        self.name = name
        self.timestamp = timestamp
        self.duration = duration
    def __repr__(self):
        return "%s\n%s\n%s"% (self.name, self.timestamp, self.duration)

class simple_model(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(simple_model, self).__init__(parent)
        self.list = []
        for name, timestamp, duration in (
        ("Nuke 1 hour", datetime.date(2017,12,9), datetime.timedelta(hours=1)),
        ("Maya 2 hours", datetime.date(2017,5,3), datetime.timedelta(hours=2)),
        ("Nuke Studio 2.2 hours", datetime.date(2017,4,6), datetime.timedelta(hours=2.2))):
            self.list.append(awevent(name, timestamp, duration))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.list)

    def data(self, index, role = QtCore.Qt.UserRole):
        if role == QtCore.Qt.DisplayRole: #show just the name
            awevent = self.list[index.row()]
            return awevent.name
        elif role == QtCore.Qt.UserRole:  #return the whole python object
            awevent = self.list[index.row()]
            return awevent
        else:
            return

    def removeRow(self, position):
        self.list = self.list[:position] + self.list[position+1:]
        self.reset()

# class dropZone(QtGui.QLabel):
#     def __init__(self, parent=None):
#         super(dropZone, self).__init__(parent)
#         self.setMinimumSize(200,200)
#         self.set_bg()
#         self.setText("Drop Here")
#         self.setAlignment(QtCore.Qt.AlignCenter)
#         self.setAcceptDrops(True)

#     def dragEnterEvent(self, event):
#         if event.mimeData().hasFormat("application/x-awevent"):
#             self.set_bg(True)
#             event.accept()
#         else:
#             event.ignore()

#     def dragMoveEvent(self, event):
#         if event.mimeData().hasFormat("application/x-awevent"):
#             event.setDropAction(QtCore.Qt.MoveAction)
#             event.accept()
#         else:
#             event.ignore()

#     def dragLeaveEvent(self, event):
#         self.set_bg()

#     def dropEvent(self, event):
#         data = event.mimeData()
#         bstream = data.retrieveData("application/x-awevent", bytearray)
#         selected = pickle.loads(bstream)
#         self.setText(str(selected))
#         self.set_bg()
#         timelog_dl = newLogDialog(selected)
#         timelog_dl.exec_()
#         event.accept()

#     def set_bg(self, active=False):
#         if active:
#             val = "background:yellow;"
#         else:
#             val = "background:green;"
#         self.setStyleSheet(val)
class task_model(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(task_model, self).__init__(parent)
        self.list = []
        for name, timestamp, duration in (
        ("task1", datetime.date(2017,12,9), datetime.timedelta(hours=1)),
        ("task2", datetime.date(2017,5,3), datetime.timedelta(hours=2)),
        ("task3", datetime.date(2017,4,6), datetime.timedelta(hours=2.2))):
            self.list.append(awevent(name, timestamp, duration))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.list)

    def data(self, index, role = QtCore.Qt.UserRole):
        if role == QtCore.Qt.DisplayRole: #show just the name
            awevent = self.list[index.row()]
            return awevent.name
        elif role == QtCore.Qt.UserRole:  #return the whole python object
            awevent = self.list[index.row()]
            return awevent
        else:
            return

class dropZone(QtGui.QTreeView):

    def __init__(self, parent=None):
        super(dropZone, self).__init__(parent)
        self.setMinimumSize(200, 200)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-awevent"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-awevent"):
            dropIndex = self.indexAt(event.pos())
            self.selectionModel().select(dropIndex, QtGui.QItemSelectionModel.SelectCurrent)
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        pass

    def dropEvent(self, event):
        dropIndex = self.indexAt(event.pos())
        droppedOn = self.model().data(dropIndex, QtCore.Qt.UserRole)
        data = event.mimeData()
        bstream = data.retrieveData("application/x-awevent", bytearray)
        selected = pickle.loads(bstream)
        timelog_dl = newLogDialog(selected, droppedOn)
        timelog_dl.exec_()
        event.accept()


class draggableList(QtGui.QListView):
    '''
    a listView whose items can be moved
    '''
    def __init__(self, parent=None):
        super(draggableList, self).__init__(parent)
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-awevent"):
            event.setDropAction(QtCore.Qt.QMoveAction)
            event.accept()
        else:
            event.ignore()

    def startDrag(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return

        ## selected is the relevant awevent object
        selected = self.model().data(index, QtCore.Qt.UserRole)

        ## convert to  a bytestream
        bstream = cPickle.dumps(selected)
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/x-awevent", bstream)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)

        # example 1 - the object itself

        pixmap = QtGui.QPixmap()
        pixmap = pixmap.grabWidget(self, self.rectForIndex(index))

        # example 2 -  a plain pixmap
        #pixmap = QtGui.QPixmap(100, self.height()/2)
        #pixmap.fill(QtGui.QColor("orange"))
        drag.setPixmap(pixmap)

        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)
        result = drag.start(QtCore.Qt.MoveAction)
        # if result: # == QtCore.Qt.MoveAction:
        #     self.model().removeRow(index.row())

    def mouseMoveEvent(self, event):
        self.startDrag(event)

class testDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(testDialog, self).__init__(parent)
        self.setWindowTitle("Drag Drop Test")
        layout = QtGui.QGridLayout(self)

        label = QtGui.QLabel("Drag Time From This List")
        taskLabel = QtGui.QLabel("Drag Time To Task")

        self.model = simple_model()
        self.listView = draggableList()
        self.listView.setModel(self.model)
        self.task_model = task_model()
        self.dz = dropZone()
        self.dz.setModel(self.task_model)

        layout.addWidget(label,0,0)
        layout.addWidget(self.listView,1,0)
        layout.addWidget(taskLabel,0,1)
        layout.addWidget(self.dz,1,1)

class newLogDialog(QtGui.QDialog):
    def __init__(self, selected, droppedOn, parent=None):
        super(newLogDialog, self).__init__(parent)
        # load in the UI that was created in the UI designer
        self.updateFromSpinbox = False
        self.hours = selected.duration.total_seconds() / 3600
        self.date = selected.timestamp
        self.task = droppedOn.name
        self.ui = Ui_NewTimeLogForm()
        self.ui.setupUi(self)
        self.ui.comboBox.addItem("%s" % self.task, userData=self.task)
        self.ui.doubleSpinBox.setRange(0.00, self.hours)
        self.ui.doubleSpinBox.setValue(self.hours)
        self.ui.dateEdit.setDate(self.date)
        self.ui.horizontalSlider.setRange(0, self.hours * 100)
        self.ui.horizontalSlider.setValue(self.hours * 100)
        self.ui.dateEdit.setCalendarPopup(True)

        self.ui.horizontalSlider.valueChanged[int].connect(self.update_spinbox)
        self.ui.doubleSpinBox.editingFinished.connect(self.update_slider_position)

    def update_spinbox(self, value):
        if not self.updateFromSpinbox:
            self.ui.doubleSpinBox.setValue(float(value)/100)

    def update_slider_position(self):
        self.updateFromSpinbox = True
        self.ui.horizontalSlider.setSliderPosition(self.ui.doubleSpinBox.value()*100)
        self.updateFromSpinbox = False
    

if __name__ == "__main__":
    '''
    the try catch here is to ensure that the app exits cleanly no matter what
    makes life better for SPE
    '''
    try:
        app = QtGui.QApplication([])
        dl = testDialog()
        dl.exec_()
    except Exception, e:  #could use as e for python 2.6...
        print e
    sys.exit(app.closeAllWindows())