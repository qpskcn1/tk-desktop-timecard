"""
Implementation of the 'My Timelog' data model
"""
from ..framework_qtwidgets import shotgun_model

ShotgunModel = shotgun_model.ShotgunModel


class MyTimelogModel(ShotgunModel):
    """
    Specialisation of Shotgun model that represents a single users timelogs
    """
    def __init__(self, parent, bg_task_manager):
        # create a SG model to retrieve our data
        ShotgunModel.__init__(
            self,
            parent=parent,
            download_thumbs=False,
            bg_load_thumbs=False,
            bg_task_manager=bg_task_manager
        )
        self.parent = parent

    def _before_data_processing(self, data):
        """
        Called after data has been retrieved from Shotgun but before any
        processing takes place
        """
        self._bundle.logger.debug("My Timelog Model {}".format(data))
        for timelog in data:
            if "duration" in timelog:
                unit = "hrs"
                hour = timelog["duration"] / 60.0
                if hour == 1 or hour == 0:
                    unit = "hr"
                timelog["duration"] = "{} {}".format(hour, unit)
        return data
