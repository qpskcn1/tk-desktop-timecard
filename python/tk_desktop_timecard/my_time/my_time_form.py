import sgtk
from sgtk.platform.qt import QtCore, QtGui

import cPickle
import datetime

from ..ui.my_time_form import Ui_MyTimeForm

logger = sgtk.platform.get_logger(__name__)


class MyTimeTree(QtGui.QListView):
    '''
    a listView whose items can be moved
    '''
    def __init__(self, parent=None):
        QtGui.QListView.__init__(self, parent)
        self.setSpacing(1)
        self.setStyleSheet("font-size: 12pt;")
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-timelogevent"):
            event.setDropAction(QtCore.Qt.QMoveAction)
            event.accept()
        else:
            event.ignore()

    def startDrag(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return

        # selected is the relevant person object
        selected = self.model().data(index, QtCore.Qt.UserRole)
        logger.debug("Drag data: %s" % selected)
        # convert to a bytestream
        bstream = cPickle.dumps(selected)
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/x-timelogevent", bstream)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)

        # the object itself
        pixmap = QtGui.QPixmap()
        pixmap = pixmap.grabWidget(self, self.rectForIndex(index))
        drag.setPixmap(pixmap)

        drag.setHotSpot(QtCore.QPoint(pixmap.width() / 2, pixmap.height() / 2))
        drag.setPixmap(pixmap)
        # pixmap = QtGui.QPixmap(100, self.height()/2)
        # pixmap.fill(QtGui.QColor("orange"))
        # drag.setPixmap(pixmap)

        result = drag.start(QtCore.Qt.MoveAction)
        if result:  # == QtCore.Qt.MoveAction:
            self.model().removeRow(index.row())

    def mouseMoveEvent(self, event):
        self.startDrag(event)


class MyTimeForm(QtGui.QWidget):
    '''
    a listView of my time which can be moved
    '''
    def __init__(self, time_model, user, parent=None):
        """
        Construction

        :param model:   The Shotgun Model this widget should connect to
        :param parent:  The parent QWidget for this control
        """
        QtGui.QWidget.__init__(self, parent)
        # set up the UI
        self._ui = Ui_MyTimeForm()
        self._ui.setupUi(self)
        self._app = sgtk.platform.current_bundle()
        self.user = user
        self.time_tree = MyTimeTree(self)
        self.time_tree.setModel(time_model)
        self._ui.verticalLayout.addWidget(self.time_tree)
        self._ui.addnew_btn.clicked.connect(self._on_addnew)
        self.get_time_sum()

    def update_ui(self):
        self.get_time_sum()

    def _on_addnew(self):
        pass

    def get_time_sum(self):
        sg = self._app.context.tank.shotgun
        filters = [
            ["user", "is", self.user],
            ["date", "is", datetime.datetime.today().strftime("%Y-%m-%d")],
        ]
        result = sg.find("TimeLog", filters, ["duration"])
        timelog_sum = 0
        for timelog in result:
            timelog_sum += timelog.get("duration", 0)
        timelog_sum_hr = timelog_sum / 60.0
        unit = "hrs"
        if timelog_sum_hr == 1:
            unit = "hr"
        self._ui.result_label.setText("<b>{} {}</b> today"
                                      .format(timelog_sum_hr, unit))