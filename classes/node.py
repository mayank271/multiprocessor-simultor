# Node Class


from classes import time_event


class Node:
    def __init__(self, node_no):
        """
        Node is the basic unit which processes a packet assigned to it by
        the MasterNode. It also has an accepted queue for the packet waiting to be
        processed at this node.
        :param node_no: Node ID
        """
        self.id = node_no
        self.accepted_queue = list()
        self.current_packet = None
        self.packets_scheduled = []
        self.completion_time = 0

    def schedule_packet(self, packet, time):
        """
        Append the packet to Accepted Queue if Property-1 is satisfied, and then run a packet
        if no packet is currently being run on the node
        :param packet: Packet scheduled on this node by the master node
        :param time: Time of arrival
        :return: Completion event if another packet gets to run on the node
        """
        self.accepted_queue.append(packet)
        self.accepted_queue = sorted(self.accepted_queue, key=lambda x: x.deadline)
        self.adjust_security_level(packet, time, True)
        # TODO: SCHEDULING PROBLEM
        return self.run_packet(time)

    def run_packet(self, time):
        """
        :param time: Time (associated with an event (arrival/ completion)
        :return: Completion event if another packet gets to run on the node
        """
        completion_event = time_event.TimeEvent(time, "completion")
        if len(self.accepted_queue) > 0:
            if self.current_packet is None:
                self.current_packet = self.accepted_queue[0]
                self.accepted_queue = self.accepted_queue[1:]
                self.packets_scheduled.append(self.current_packet.id)
                completion_event.time += self.current_packet.security + self.current_packet.packet_size
                completion_event.node_id = self.id
        if completion_event.time == time:
            return None
        else:
            self.completion_time = completion_event.time
            return completion_event

    def start_time(self, time):
        """
        :param time: Time when this is called
        :return: The time at the which all the packets in the accepted queue of this node will get completed
        """
        if self.current_packet is not None:
            time += self.completion_time - time
        for pkt in self.accepted_queue:
            time += pkt.security + pkt.packet_size
        return time

    def adjust_security_level(self, packet, time, prop1, iterations=0):
        """
        :param packet: Packet scheduled on this node by the master node
        :param time: Time when called
        :param prop1: True or False depending on whether the packet satisfies property-1 or not
        :param iterations: Number of times we adjust the security level if the packet does not satisfy property 1
        """
        s_time = self.start_time(time)
        if prop1 is True:
            while packet.satisfies_prop1(s_time) and packet.security < 10:
                packet.security += 0.1
            packet.security -= 0.1
        else:
            while packet.satisfies_prop1(s_time) is False and iterations > 0:
                for pkt in self.accepted_queue:
                    if pkt.security >= pkt.min_security + 0.1:
                        pkt.security -= 0.1
                s_time = self.start_time(time)
                iterations -= 1

    def util_val(self, time):
        """
        :param time: Time when called
        :return: Utilization value of this node
        """
        if len(self.accepted_queue) == 0:
            return 0
        else:
            return self.start_time(time)/self.accepted_queue[len(self.accepted_queue)-1].deadline
