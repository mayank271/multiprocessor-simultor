#  Packet Class


class Packet:
    def __init__(self, pno, start, deadline, min_security, max_security, packet_size=10):
        """
        :param pno: Packet Number
        :param start: The time at which the packet arrives at the master node
        :param deadline: The absolute deadline of the packet
        :param min_security: Minimum security level (in terms of time) desired by the packet
        :param max_security: Maximum security level (in terms of time) desired by the packet
        :param packet_size: The length of the packet (Processing time)
        """
        self.id = pno
        self.packet_size = packet_size
        self.start = start
        self.deadline = deadline
        self.min_security = min_security
        self.max_security = max_security
        self.security = self.min_security
        self.dropped = False

    def __str__(self):
        if self.dropped is False:
            return "Packet ID: {} Security: {} Arrived At: {} Deadline: {}"\
                .format(self.id, self.security, self.start, self.deadline)
        else:
            return "[DROPPED] Packet ID: {} Details: {} {} {}".format(self.id, self.start, self.security, self.deadline)

    def __repr__(self):
        if self.dropped is False:
            return "Packet ID: {} Security: {} Arrived At: {} Deadline: {}" \
                .format(self.id, self.security, self.start, self.deadline)
        else:
            return "[DROPPED] Packet ID: {} Details: {} {} {}".format(self.id, self.start, self.security, self.deadline)

    def satisfies_prop1(self, time):
        """
        Checks whether the packet is valid or not, i.e. the deadline allows it execute with the minimum security level
        """
        if (self.packet_size + self.security + time) > self.deadline:
            return False
        else:
            return True
