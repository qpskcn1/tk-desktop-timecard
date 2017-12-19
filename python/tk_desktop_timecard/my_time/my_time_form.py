import sgtk
from sgtk.platform.qt import QtCore, QtGui

import cPickle

from ..ui.my_time_form import Ui_MyTimeForm

logger = sgtk.platform.get_logger(__name__)


class MyTimeTree(QtGui.QListView):
    '''
    a listView whose items can be moved
    '''
    def __init__(self, parent=None):
        QtGui.QListView.__init__(self, parent)
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

        # selected is the relevant person object
        selected = self.model().data(index, QtCore.Qt.UserRole)
        logger.debug("Drag data: %s" % selected)
        # convert to a bytestream
        bstream = cPickle.dumps(selected)
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/x-awevent", bstream)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)

        # the object itself
        pixmap = QtGui.QPixmap()
        pixmap = pixmap.grabWidget(self, self.rectForIndex(index))
        drag.setPixmap(pixmap)

        drag.setHotSpot(QtCore.QPoint(pixmap.width() / 2, pixmap.height() / 2))
        drag.setPixmap(pixmap)
        result = drag.start(QtCore.Qt.MoveAction)
        if result:  # == QtCore.Qt.MoveAction:
            self.model().removeRow(index.row())

    def mouseMoveEvent(self, event):
        self.startDrag(event)


class MyTimeForm(QtGui.QWidget):
    '''
    a listView of my time which can be moved
    '''
    def __init__(self, time_model, parent=None):
        """
        Construction

        :param model:   The Shotgun Model this widget should connect to
        :param parent:  The parent QWidget for this control
        """
        QtGui.QWidget.__init__(self, parent)
        # set up the UI
        self._ui = Ui_MyTimeForm()
        self._ui.setupUi(self)

        search_label = "My Time"
        self._ui.search_ctrl.set_placeholder_text("Search %s" % search_label)
        self._ui.search_ctrl.setToolTip("Press enter to complete the search")
        self.time_tree = MyTimeTree(self)
        self.time_tree.setModel(time_model)
        self._ui.verticalLayout.addWidget(self.time_tree)