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
    def __init__(self, time_model, checkedin=False, parent=None):
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
        # filter_model = QtGui.QSortFilterProxyModel()
        # filter_model.setSourceModel(time_model)
        # filter_model.setDynamicSortFilter(True)
        self.time_tree.setModel(time_model)
        self._ui.verticalLayout.addWidget(self.time_tree)
        if not checkedin:
            self._ui.new_time_btn.setEnabled(False)
        else:
            self._ui.new_time_btn.setEnabled(True)
        self._ui.new_time_btn.clicked.connect(self._on_new_time)
        # connect up the filter controls:
        # self._ui.search_ctrl.search_changed.connect(self._on_search_changed)

    def update_ui(self, checkedin):
        view_model = self.time_tree.model()
        if not checkedin:
            # detach the filter model from the view:
            if view_model:
                self.prev_model = view_model
                self.time_tree.setModel(None)
            self._ui.new_time_btn.setEnabled(False)
        else:
            if view_model:
                self.time_tree.model().async_refresh()
            else:
                self.time_tree.setModel(self.prev_model)
            self._ui.new_time_btn.setEnabled(True)

    def _on_new_time(self):
        self.time_tree.model().addCustomTime()

    def _on_search_changed(self, search_text):
        try:
            filter_reg_exp = QtCore.QRegExp(search_text, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.FixedString)
            self.time_tree.model().setFilterRegExp(filter_reg_exp)
        except Exception as e:
            logger.error(e)
