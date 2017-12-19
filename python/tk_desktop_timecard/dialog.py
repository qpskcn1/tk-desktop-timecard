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
import subprocess
import re
import os
import sys
import logging
import signal
from datetime import datetime
import traceback

from .my_tasks.my_tasks_form import MyTasksForm
from .my_tasks.my_tasks_model import MyTasksModel
from .my_time.my_time_form import MyTimeForm
from .my_time.my_time_model import MyTimeModel
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
AWPROCESS = ['aw-qt.exe',
             'aw-server.exe',
             'aw-watcher-afk.exe',
             'aw-watcher-window.exe']


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

        # Set up our own logger (other than shotgun looger) for storing timestamp
        self.set_logger(logging.INFO)

        # now load in the UI that was created in the UI designer
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # create a background task manager
        self._task_manager = task_manager.BackgroundTaskManager(
            self,
            start_processing=True,
            max_threads=1
        )
        monitor_qobject_lifetime(self._task_manager, "Main task manager")
        self._task_manager.start_processing()

        # lastly, set up our very basic UI
        self.user = sgtk.util.get_current_user(self._app.sgtk)
        self.ui.textBrowser.setText("Hello, %s!" % self.user['firstname'])
        self.ui.CIBtn.clicked.connect(self.checkIn)
        self.ui.COBtn.clicked.connect(self.checkOut)
        # create my tasks form and my time form:
        self.createTasksFrom()
        self.createTimeForm()

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

    def checkIn(self):
        """
        Callback when 'Check In' button is clicked
        Open aw-qt, aw-server, aw-watcher if 'aw-qt.exe' is not existed
        otherwise, report to console
        """
        try:
            procs = self.checkAWProcess("aw-*")
            if len(procs) > 0:
                self.ui.textBrowser.setText("You've already checked in before!")
            else:
                for app in AWPROCESS[1:]:
                    appPath = os.path.join("Y:\\studio\\dev\\work\\yi\\timelog\\activitywatch", app)
                    subprocess.Popen(app, executable=appPath)
                QtGui.QApplication.processEvents()
                self.ui.textBrowser.setText("You have successfully checked in!")
                self._logger.info("%s checked in! UTC%s"
                                  % (self.user['firstname'], datetime.utcnow()))
        except Exception as e:
            self.ui.textBrowser.setText("Failed to Check In, because %s" % e)
            logger.exception("Failed to Check In, because %s \n %s"
                             % (e, traceback.format_exc()))

    def checkOut(self):
        try:
            self.killAllAW()
        except Exception as e:
            self.ui.textBrowser.setText("Failed to Check Out, because %s" % e)
            logger.exception("Failed to Check Out, because %s" % e)

    def killAllAW(self):
        """
        Kill all processes related to active watch in Windows
        """
        procs = self.checkAWProcess("aw-*")
        if len(procs) > 0:
            for proc in procs:
                # make sure to kill the correct proc
                if proc['name'] in AWPROCESS:
                    os.kill(int(proc['pid']), signal.SIGTERM)
                else:
                    logger.exception("Failed to kill %s" % proc['name'])
            QtGui.QApplication.processEvents()
            self.ui.textBrowser.setText("You have successfully checked out!")
            self._logger.info("%s checked out! UTC%s"
                              % (self.user['firstname'], datetime.utcnow()))
        else:
            self.ui.textBrowser.setText("You haven't checked in yet!")

    def checkAWProcess(self, processname):
        """
        Check tasklist in Windows and return a list of processes that contains
        'processname'
        List example:
        [{'pid': 1001, 'name': 'aw-qt.exe'},
         {'pid': 10002, 'name': 'aw-server.exe'},
         ...
        ]
        """
        tlcall = 'TASKLIST', '/FI', 'imagename eq %s' % processname
        # shell=True hides the shell window, stdout to PIPE enables
        # communicate() to get the tasklist command result
        tlproc = subprocess.Popen(tlcall, shell=True, stdout=subprocess.PIPE)
        # trimming it to the actual lines with information
        tlout = tlproc.communicate()[0].strip().split('\r\n')
        procs = []
        # For each task, append task name and pid to list
        for line in tlout[2:]:
            proc = re.match("(.+?) +(\d+)", line)
            procs.append({'name': proc.group(1), 'pid': proc.group(2)})
        return procs

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
            # shut down main threadpool
            self._task_manager.shut_down()
        except Exception as e:
            logger.exception("Error running Shotgun Panel App closeEvent() %s" % e)

    def set_logger(self, level=logging.INFO):
        """
        Setup the logger

        :param level: Required logging level
        """
        self._logger = logging.getLogger(self._app.name)
        # Copied over from tk-desktop
        if sys.platform == "darwin":
            self._log_file_path = os.path.join(os.path.expanduser("~"), "Library", "Logs", "Shotgun", "%s.log" % self._app.name)
        elif sys.platform == "win32":
            self._log_file_path = os.path.join(os.environ.get("APPDATA", "APPDATA_NOT_SET"), "Shotgun", "Logs", "%s.log" % self._app.name)
        elif sys.platform.startswith("linux"):
            self._log_file_path = os.path.join(os.path.expanduser("~"), ".shotgun", "logs", "%s.log" % self._app.name)
        else:
            raise NotImplementedError("Unknown platform: %s" % sys.platform)
        handler = logging.FileHandler(self._log_file_path)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s"
        ))
        self._logger.addHandler(handler)
        self._logger.setLevel(level)

    @QtCore.Slot(int, str)
    def new_message(self, level, message):
        # This is required for the logger
        pass

    def createTasksFrom(self):
        try:
            self._my_tasks_model = self._build_my_tasks_model(self._app.context.project)
            self._my_tasks_form = MyTasksForm(self._my_tasks_model,
                                              allow_task_creation=False,
                                              parent=self)
            # self._my_tasks_form.entity_selected.connect(self._on_entity_selected)
            self.ui.taskTabWidget.addTab(self._my_tasks_form, "My Tasks")
            facility_project_ctx = {'type': 'Project', 'id': 143, 'name': 'Facility'}
            self._facility_tasks_model = self._build_my_tasks_model(facility_project_ctx)
            self._facility_tasks_form = MyTasksForm(self._facility_tasks_model,
                                                    allow_task_creation=False,
                                                    parent=self)
            self.ui.taskTabWidget.addTab(self._facility_tasks_form, "Facility")
            # self._my_tasks_form.create_new_task.connect(self.create_new_task)
        except Exception as e:
            logger.exception("Failed to Load my tasks, because %s \n %s"
                             % (e, traceback.format_exc()))

    def _build_my_tasks_model(self, project):
        if not self.user:
            # can't show my tasks if we don't know who 'my' is!
            logger.debug("There is no tasks because user is not defined")
            return None
        # get any extra display fields we'll need to retrieve:
        extra_display_fields = self._app.get_setting("my_tasks_extra_display_fields")
        # get the my task filters from the config.
        my_tasks_filters = self._app.get_setting("my_tasks_filters")
        model = MyTasksModel(project,
                             self.user,
                             extra_display_fields,
                             my_tasks_filters,
                             parent=self,
                             bg_task_manager=self._task_manager)
        monitor_qobject_lifetime(model, "My Tasks Model")
        model.async_refresh()
        logger.debug("Tasks Model Build Finished")
        return model

    def _on_refresh_triggered(self, checked=False):
        """
        Slot triggered when a refresh is requested via the refresh keyboard shortcut

        :param checked:    True if the refresh action is checked - ignored
        """
        self._app.log_debug("Synchronizing remote path cache...")
        self._app.sgtk.synchronize_filesystem_structure()
        self._app.log_debug("Path cache up to date!")
        if self._my_tasks_model:
            self._my_tasks_model.async_refresh()

    def createTimeForm(self):
        try:
            self._my_time_model = MyTimeModel()
            self._my_time_form = MyTimeForm()
            self._my_time_form.setModel(self._my_time_model)
            self.ui.timeTabWidget.addTab(self._my_time_form, "My Time")
        except Exception as e:
            logger.exception("Failed to Load my tasks, because %s \n %s"
                             % (e, traceback.format_exc()))
