import sgtk
from sgtk.platform.qt import QtCore, QtGui
from datetime import datetime
import re

LOG_PATH = r"C:\Users\testclient\AppData\Roaming\Shotgun\Logs\tk-desktop-timecard.log"
logger = sgtk.platform.get_logger(__name__)


class MyTimeBar(QtGui.QWidget):

    def __init__(self):
        super(MyTimeBar, self).__init__()
        self.start = start = datetime.now().replace(hour=0, minute=0)
        self.checkedIn, self.checkedOut = self.getTimeInfo()

    def paintEvent(self, e):
        width = float(self.frameGeometry().width())
        height = float(self.frameGeometry().height())
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectangles(qp, width, height)
        self.drawScale(qp, width, height)
        qp.end()

    def drawScale(self, qp, width, height):
        unit = width / 24
        color = QtGui.QColor(255, 255, 255)
        qp.setPen(color)
        # drawing axis
        qp.drawLine(0, height * 0.65, width, height * 0.65)
        for i in range(24):
            qp.drawLine(i * unit, height * 0.65, i * unit, height * 0.6)
        # drawing text
        for i in range(9, 19, 3):
            qp.drawText(i * unit - 15,
                        height * 0.65,
                        30,
                        height * 0.3,
                        QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop,
                        "{}:00".format(i))

    def drawRectangles(self, qp, width, height):
        unit = width / 3600 / 24
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#BEF781')
        qp.setPen(color)
        qp.setBrush(color)
        for i in range(len(self.checkedIn)):
            inTime = self.checkedIn[i] - self.start
            outTime = self.checkedOut[i] - self.checkedIn[i]
            qp.drawRect(inTime.total_seconds() * unit,
                        height * 0.05,
                        outTime.total_seconds() * unit,
                        height * 0.6)

    def getTimeInfo(self):
        """
        Read log file and get the last check in time
        """
        checkedIn = []
        checkedOut = []
        today = str(datetime.now().date())
        with open(LOG_PATH, 'r') as logfile:
            lineList = logfile.readlines()
            recentLines = lineList[len(lineList) - 20:len(lineList)]
        for line in recentLines:
            timeMatch = re.match("(%s.*)\sINFO.*checked in" % today, line.strip())
            if timeMatch:
                dt = datetime.strptime(timeMatch.group(1), "%Y-%m-%d %H:%M:%S,%f")
                if dt not in checkedIn:
                    checkedIn.append(dt)
            else:
                timeMatch = re.match("(%s.*)\sINFO.*checked out" % today, line.strip())
                if timeMatch:
                    dt = datetime.strptime(timeMatch.group(1), "%Y-%m-%d %H:%M:%S,%f")
                    if dt not in checkedOut:
                        checkedOut.append(dt)
        logger.debug("in %s" % checkedIn)
        logger.debug("out %s" % checkedOut)
        # add "now" as last checked out time
        checkedOut.append(datetime.now())
        if len(checkedIn) == len(checkedOut):
            return checkedIn, checkedOut
        else:
            return None, None
