import sgtk
from sgtk.platform.qt import QtCore, QtGui

import cPickle

logger = sgtk.platform.get_logger(__name__)


class MyTimeForm(QtGui.QListView):
    '''
    a listView of my time which can be moved
    '''
    def __init__(self, parent=None):
        super(MyTimeForm, self).__init__(parent)
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