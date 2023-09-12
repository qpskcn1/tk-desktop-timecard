import sgtk
from sgtk.platform.qt import QtCore, QtGui

import pickle

from ..ui.my_time_form import Ui_MyTimeForm

logger = sgtk.platform.get_logger(__name__)


class MyTimeTree(QtGui.QListView):
    """
    a listView whose items can be moved
    """

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
        bstream = pickle.dumps(selected)
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
    """
    a listView of my time which can be moved
    """

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

    def update_ui(self):
        """
        Update the UI to reflect logged in time, etc.
        """
        pass

    def _on_addnew(self):
        pass
