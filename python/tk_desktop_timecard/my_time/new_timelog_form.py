import sgtk
from sgtk.platform.qt import QtGui
from ..ui.new_timelog import Ui_NewTimeLogForm

logger = sgtk.platform.get_logger(__name__)


class NewTimeLogForm(QtGui.QDialog):

    def __init__(self, data, task, parent=None):
        super(NewTimeLogForm, self).__init__(parent)

        self._app = sgtk.platform.current_bundle()
        # load in the UI that was created in the UI designer
        self.updateFromSpinbox = False
        self.awname = data.name
        self.hours = data.duration.total_seconds() / 3600
        self.date = data.timestamp
        self.ui = Ui_NewTimeLogForm()
        self.ui.setupUi(self)
        self.ui.comboBox.addItem("%s %s, %s" %
                                 (task['entity']['type'], task['entity']['name'], task['content']),
                                 userData=task)
        self.ui.doubleSpinBox.setRange(0.00, self.hours)
        self.ui.doubleSpinBox.setValue(self.hours)
        self.ui.dateEdit.setDate(self.date)
        self.ui.horizontalSlider.setRange(0, self.hours * 100)
        self.ui.horizontalSlider.setValue(self.hours * 100)

        self.ui.horizontalSlider.valueChanged[int].connect(self.update_spinbox)
        self.ui.doubleSpinBox.editingFinished.connect(self.update_slider_position)

        self.ui.buttonBox.accepted.connect(self.submitTimeLog)

    def update_spinbox(self, value):
        if not self.updateFromSpinbox:
            self.ui.doubleSpinBox.setValue(float(value) / 100)

    def update_slider_position(self):
        self.updateFromSpinbox = True
        self.ui.horizontalSlider.setSliderPosition(self.ui.doubleSpinBox.value() * 100)
        self.updateFromSpinbox = False

    def submitTimeLog(self):
        try:
            task = self.ui.comboBox.itemData(self.ui.comboBox.currentIndex())
            # duration value is expressed in minutes
            duration = float(self.ui.doubleSpinBox.value()) * 60
            description = self.ui.textEdit.toPlainText()
            extra_description = "\n{}, logged by Timecard".format(self.awname)
            if description:
                extra_description = "," + extra_description
            sg = self._app.context.tank.shotgun
            logger.debug("submit task {}, duration {}".format(task, duration))
            result = sg.create("TimeLog", {"duration": duration,
                                           "project": self._app.context.project,
                                           "entity": task,
                                           "description": description + extra_description})
            logger.debug("create result: {}".format(result))
            # then subtract logged time from model

        except Exception as e:
            logger.error(e)
