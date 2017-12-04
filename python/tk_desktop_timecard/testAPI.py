import requests
import json
import re
from datetime import datetime
import os


# params = {'limit': 1000, 'start': None, 'end': datetime.utcnow()}
# r = requests.get(url, params=params)
# r_afk = requests.get(url, params=params)
# data = json.loads(r.text)

# develop_duration = 0
# chrome_duration = 0
# print len(data)
# for d in data:
#   if "2017-11-21" in d['timestamp']:
#       print d
#   if "sublime" in d['data']['app']:
#       develop_duration += d['duration']
#   if "chrome" in d['data']['app']:
#       chrome_duration += d['duration']
# print develop_duration
# print chrome_duration/3600


class parsingAWData(object):
    """
    class for parsing and analysing data from Active Watch
    """
    def __init__(self, app, log_file_path):
        """
        Constructor
        """
        self._app = app
        self._log_file_path = log_file_path
        # first, call the base class and let it do its thing.

        # # now load in the UI that was created in the UI designer
        # self.ui = Ui_Dialog()
        # self.ui.setupUi(self)

        # # create a background task manager
        # self._task_manager = task_manager.BackgroundTaskManager(
        #     self,
        #     start_processing=True,
        #     max_threads=1
        # )

        # # lastly, set up our very basic UI

    def getLastCheckInTime(self):
        """
        Read log file and get the last check in time
        """
        with open(self._log_file_path, 'r') as logfile:
            lineList = logfile.readlines()
            lastLine = lineList[len(lineList) - 1]
        timeMatch = re.match(".*checked in! UTC(.*)", lastLine.strip())
        if timeMatch:
            return datetime.strptime(timeMatch.group(1), "%Y-%m-%d %H:%M:%S.%f")
        else:
            return None

    def getAWData(self):
        """
        Retrive the data from AW server through REST API
        TODO: implement afk filter
        """
        startTime = self.getLastCheckInTime()
        hostname = os.environ.get("COMPUTERNAME", "unknown")
        url_window = "http://localhost:5600/api/0/buckets/aw-watcher-window_%s/events" % hostname
        url_afk = "http://localhost:5600/api/0/buckets/aw-watcher-afk_%s/events" % hostname
        params = {'limit': 1792, 'start': None, 'end': datetime.utcnow()}
        r_window = requests.get(url_window, params=params)
        r_afk = requests.get(url_afk, params=params)
        data_window = json.loads(r_window.text)
        data_afk = json.loads(r_afk.text)
        return data_window, data_afk

    def calculate(self, data_window, data_afk):
        """
        Aggregate windows and calculate time
        """
        duration = {}
        develop_duration = 0
        for window in data_window:
            if "sublime" in window['data']['app']:
                develop_duration += window['duration']
        print "development duration: {} minutes".format(develop_duration/60)

p = parsingAWData("tk-desktop-timecard", r"C:\Users\testclient\AppData\Roaming\Shotgun\Logs\tk-desktop-timecard.log")
data_window, data_afk = p.getAWData()
p.calculate(data_window, data_afk)