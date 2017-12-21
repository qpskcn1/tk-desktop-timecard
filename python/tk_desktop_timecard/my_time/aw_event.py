class AWEvent(object):
    '''
    a custom data structure for AW data
    '''
    def __init__(self, name, timestamp, duration):
        self.name = name
        self.timestamp = timestamp
        self.duration = duration

    def __repr__(self):
        return "{name: %s, date: %s, duration: %s}" % (self.name, self.timestamp, self.duration)

    def subtract_logged_time(self, logged_time):
        self.duration = self.duration - self.logged_time