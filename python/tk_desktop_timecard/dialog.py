# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
import sys
import traceback
import datetime

from .my_tasks.my_tasks_form import MyTasksForm
from .my_tasks.my_tasks_model import MyTasksModel
from .my_time.my_time_form import MyTimeForm
from .my_time.my_time_model import MyTimeModel
from .my_timelog.my_timelog_table import MyTimelogTable
from .util import monitor_qobject_lifetime
# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog

# There are two loggers
# logger is shotgun logger
# _logger is a independet logger
logger = sgtk.platform.get_logger(__name__)
task_manager = sgtk.platform.import_framework("tk-framework-shotgunutils", "task_manager")
shotgun_globals = sgtk.platform.import_framework("tk-framework-shotgunutils", "shotgun_globals")


class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """

    def __init__(self):
        """
        Constructor
        """
        # get app bundle
        self._app = sgtk.platform.current_bundle()
        # call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)

        # # Set up our own logger (other than shotgun logger) for storing timestamp
        # self.set_logger(logging.INFO)
        # now load in the UI that was created in the UI designer
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # create a background task manager
        self._task_manager = task_manager.BackgroundTaskManager(
            self,
            start_processing=True,
            max_threads=4
        )
        monitor_qobject_lifetime(self._task_manager, "Main task manager")
        self._task_manager.start_processing()

        # lastly, set up our very basic UI
        self.user = sgtk.util.get_current_user(self._app.sgtk)
        # self.ui.textBrowser.setText("Hello, %s!" % self.user['firstname'])
        # create my tasks form and my time form:
        self.createTasksForm()
        self.createTimeForm()
        self.createTimelogTable()
        # time summary labels
        self._get_time_sum()
        self.ui.time_sum_label.setFont(QtGui.QFont("Arial", 80))

        # add refresh action with appropriate keyboard shortcut:
        refresh_action = QtGui.QAction("Refresh", self)
        refresh_action.setShortcut(QtGui.QKeySequence(QtGui.QKeySequence.Refresh))
        refresh_action.triggered.connect(self._on_refresh_triggered)
        self.addAction(refresh_action)
        # on OSX, also add support for F5 (the default for OSX is Cmd+R)
        if sys.platform == "darwin":
            osx_f5_refresh_action = QtGui.QAction("Refresh (F5)", self)
            osx_f5_refresh_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F5))
            osx_f5_refresh_action.triggered.connect(self._on_refresh_triggered)
            self.addAction(osx_f5_refresh_action)

    def closeEvent(self, event):
        """
        Executed when the main dialog is closed.
        All worker threads and other things which need a proper shutdown
        need to be called here.
        """
        logger.debug("CloseEvent Received. Begin shutting down UI.")

        # register the data fetcher with the global schema manager
        shotgun_globals.unregister_bg_task_manager(self._task_manager)

        try:
            if self._my_tasks_model:
                self._my_tasks_model.destroy()
            # if self._facility_tasks_model:
            #     self._facility_tasks_model.destroy()
            if self._my_time_model:
                self._my_time_model.destroy()
            # shut down main threadpool
            self._task_manager.shut_down()
        except Exception as e:
            logger.exception("Error running Shotgun Panel App closeEvent() %s" % e)

    # def set_logger(self, level=logging.INFO):
    #     """
    #     Setup the logger

    #     :param level: Required logging level
    #     """
    #     self._logger = logging.getLogger(self._app.name)
    #     # Copied over from tk-desktop
    #     if sys.platform == "darwin":
    #         self._log_file_path = os.path.join(os.path.expanduser("~"), "Library", "Logs", "Shotgun", "%s.log" % self._app.name)
    #     elif sys.platform == "win32":
    #         self._log_file_path = os.path.join(os.environ.get("APPDATA", "APPDATA_NOT_SET"), "Shotgun", "Logs", "%s.log" % self._app.name)
    #     elif sys.platform.startswith("linux"):
    #         self._log_file_path = os.path.join(os.path.expanduser("~"), ".shotgun", "logs", "%s.log" % self._app.name)
    #     else:
    #         raise NotImplementedError("Unknown platform: %s" % sys.platform)
    #     handler = logging.FileHandler(self._log_file_path)
    #     handler.setFormatter(logging.Formatter(
    #         "%(asctime)s %(levelname)s %(message)s"
    #     ))
    #     self._logger.addHandler(handler)
    #     self._logger.setLevel(level)


    @QtCore.Slot(int, str)
    def new_message(self, level, message):
        # This is required for the logger
        pass

    def createTasksForm(self, UI_filters_action=None):
        """
        Create my task form and facility task form icluding model and view.
        :param UI_filter_action: QAction contains shotgun filter selected in UI
        """
        try:
            self._my_tasks_model = self._build_my_tasks_model(
                self._app.context.project, UI_filters_action)
            self._my_tasks_form = MyTasksForm(self._my_tasks_model,
                                              UI_filters_action,
                                              allow_task_creation=False,
                                              parent=self)
            # refresh tab
            if UI_filters_action is not None:
                self.ui.taskTabWidget.clear()
            self.ui.taskTabWidget.addTab(self._my_tasks_form, "My Tasks")
        except Exception as e:
            logger.exception("Failed to Load my tasks, because %s \n %s"
                             % (e, traceback.format_exc()))

    def createTimeForm(self):
        """
        Create my time form icluding model and view.
        """
        try:
            self._my_time_model = MyTimeModel()
            self._my_time_form = MyTimeForm(self._my_time_model, self.user)
            self.ui.timeTabWidget.addTab(self._my_time_form, "My Time")
        except Exception as e:
            logger.exception("Failed to Load my time, because %s \n %s"
                             % (e, traceback.format_exc()))

    def createTimelogTable(self):
        """
        create a table for timelog activities
        """
        try:
            self.my_timelog_table = MyTimelogTable(self, self._task_manager)
            self.my_timelog_table.setMaximumHeight(200)
            self.ui.tableLayout.addWidget(self.my_timelog_table)
        except Exception as e:
            logger.exception("Failed to Load timelog because %s \n %s"
                             % (e, traceback.format_exc()))

    def _build_my_tasks_model(self, project, UI_filters_action=None):
        """
        Get settings from config file and append those settings default
        Then create task model
        :param project: dict
                        sg project context
        :UI_filter action: QAction contains shotgun filter selected in UI
        """
        if not self.user:
            # can't show my tasks if we don't know who 'my' is!
            logger.debug("There is no tasks because user is not defined")
            return None
        # get any extra display fields we'll need to retrieve:
        extra_display_fields = self._app.get_setting("my_tasks_extra_display_fields")
        # get the my task filters from the config.
        UI_filters = []
        if UI_filters_action is None:
            UI_filters = [['project', 'is', '{context.project}']]
        else:
            UI_filters = UI_filters_action.data()
        my_tasks_filters = self._app.get_setting("my_tasks_filters")
        model = MyTasksModel(project,
                             self.user,
                             extra_display_fields,
                             my_tasks_filters,
                             UI_filters,
                             parent=self,
                             bg_task_manager=self._task_manager)
        monitor_qobject_lifetime(model, "My Tasks Model")
        model.async_refresh()
        logger.debug("Tasks Model Build Finished")
        return model

    def _get_time_sum(self):
        """
        Get today's timelog for current user and return the sum of
        all queried timelog
        """
        sg = self._app.context.tank.shotgun
        today = datetime.datetime.today()
        this_week = self.__get_week(today)
        filters = [
            ["user", "is", self.user],
            ["date", "in", this_week],
        ]
        result = sg.find("TimeLog", filters, ["date", "duration"])
        timelog_sum_today = 0
        timelog_sum_week = 0
        for timelog in result:
            if timelog.get("date", 0) == today.strftime("%Y-%m-%d"):
                timelog_sum_today += timelog.get("duration", 0)
            timelog_sum_week += timelog.get("duration", 0)
        self._display_hours(timelog_sum_today, "today")
        self._display_hours(timelog_sum_week, "this week")

    def __get_week(self, today):
        week = []
        for i in range(0 - today.weekday(), 7 - today.weekday()):
            week.append(
                (today + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            )
        return week

    def _display_hours(self, timelog_sum, day_or_week):
        timelog_sum_hr = timelog_sum / 60.0
        unit = "hours"
        if timelog_sum_hr == 1 or timelog_sum_hr == 0:
            unit = "hour"
        label_ui = self.ui.time_sum_today_label
        text_color = "LightGray"
        if day_or_week == "today":
            label_ui = self.ui.time_sum_today_label
            if timelog_sum_hr < 2:
                text_color = "Tomato"
            elif timelog_sum_hr < 6:
                text_color = "Orange"
            else:
                text_color = "MediumSeaGreen"
        else:
            label_ui = self.ui.time_sum_week_label
            if timelog_sum_hr < 10:
                text_color = "Tomato"
            elif timelog_sum_hr < 30:
                text_color = "Orange"
            else:
                text_color = "MediumSeaGreen"
        text = """
        <b style=\"color:{color};\">{hours} {unit}</b>
        {day_or_week}
        """.format(
            color=text_color,
            hours=timelog_sum_hr,
            unit=unit,
            day_or_week=day_or_week
        )
        label_ui.setText(text)

    def _on_refresh_triggered(self):
        """
        Slot triggered when a refresh is requested via the refresh keyboard shortcut
        """
        self._app.log_debug("Synchronizing remote path cache...")
        self._app.sgtk.synchronize_filesystem_structure()
        self._app.log_debug("Path cache up to date!")
        self._get_time_sum()
        if self._my_tasks_model:
            self._my_tasks_model.async_refresh()
        # if self._facility_tasks_model:
        #     self._facility_tasks_model.async_refresh()
        if self._my_time_form:
            self._my_time_form.update_ui()
        if self._my_time_model:
            self._my_time_model.async_refresh()
        if self.my_timelog_table._model:
            self.my_timelog_table._model._refresh_data()
