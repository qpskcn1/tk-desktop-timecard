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


# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog

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
        self._app = sgtk.platform.current_bundle()
        # first, call the base class and let it do its thing.
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

        # lastly, set up our very basic UI
        self.user = sgtk.util.get_current_user(self._app.sgtk)
        self.ui.textBrowser.setText("Hello, %s!" % self.user['firstname'])
        self.ui.CIBtn.clicked.connect(self.checkIn)
        self.ui.COBtn.clicked.connect(self.checkOut)

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