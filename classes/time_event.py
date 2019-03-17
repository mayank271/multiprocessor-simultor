# Time Event (triggered whenever a packet is removed/scheduled)


class TimeEvent:
    def __init__(self, time, category):
        """
        :param time: Time of the event
        :param category: Type of the event (arrival or completion)
        """
        self.time = time
        self.category = category
        self.node_id = None

    def __repr__(self):
        return "Time: {} [{}]".format(self.time, self.category)

    def __str__(self):
        return "Time: {} [{}]".format(self.time, self.category)
