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

        self.time_tree = MyTimeTree(self)
        # filter_model = QtGui.QSortFilterProxyModel()
        # filter_model.setSourceModel(time_model)
        # filter_model.setDynamicSortFilter(True)
        self.time_tree.setModel(time_model)
        self._ui.verticalLayout.addWidget(self.time_tree)
        self._ui.addnew_btn.clicked.connect(self._on_addnew)
        # connect up the filter controls:

    def update_ui(self, checkedin):
        view_model = self.time_tree.model()
        if not checkedin:
            # detach the filter model from the view:
            if view_model:
                self.prev_model = view_model
                self.time_tree.setModel(None)
            self._ui.refresh_btn.setEnabled(False)
        else:
            if view_model:
                self.time_tree.model().async_refresh()
            else:
                self.time_tree.setModel(self.prev_model)
            self._ui.refresh_btn.setEnabled(True)

    def _on_addnew(self):
        pass
