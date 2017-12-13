from sgtk.platform.qt import QtCore, QtGui
from ..ui.new_timelog import Ui_NewTimeLogForm


class NewTimeLogForm(QtGui.QDialog):

    def __init__(self, data, parent=None):
        super(NewTimeLogForm, self).__init__(parent)
        # load in the UI that was created in the UI designer
        self.updateFromSpinbox = False
        self.hours = data.duration.total_seconds() / 3600
        self.date = data.timestamp
        self.ui = Ui_NewTimeLogForm()
        self.ui.setupUi(self)
        self.ui.doubleSpinBox.setRange(0.00, self.hours)
        self.ui.doubleSpinBox.setValue(self.hours)
        self.ui.dateEdit.setDate(self.date)
        self.ui.horizontalSlider.setRange(0, self.hours * 100)
        self.ui.horizontalSlider.setValue(self.hours * 100)

        self.ui.horizontalSlider.valueChanged[int].connect(self.update_spinbox)
        self.ui.doubleSpinBox.editingFinished.connect(self.update_slider_position)
