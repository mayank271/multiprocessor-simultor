# Master-Node Class


from classes import node


class MasterNode:
    def __init__(self, number_of_processors):
        """
        MasterNode controls n number of nodes
        :param number_of_processors: # Nodes in the grid
        """
        self.dropped_packets = []
        self.node_heap = list()
        for i in range(number_of_processors):
            temp = node.Node(i)
            self.node_heap.append(temp)
        self.total_security = 0
        self.total_wait_time = 0

    def heapify(self, time):
        """
        :param time: Time when the heapify is called
        """
        # Simple sort; Not exact heap
        self.node_heap = sorted(self.node_heap, key=lambda x: x.util_val(time))

    def process_event(self, event, pkt=None):
        """
        :param event: Time Event
        :param pkt: Packet if the Event is of "arrival" type
        :return: Completion event (if created) other None
        """
        new_event = None
        if event.category == "arrival":
            # TODO: ASSIGNMENT PROBLEM
            best_node = self.node_heap[0]
            if pkt.satisfies_prop1(best_node.start_time(event.time)):
                new_event = best_node.schedule_packet(pkt, event.time)
            else:
                best_node.adjust_security_level(pkt, event.time, False, 5)
                if pkt.satisfies_prop1(best_node.start_time(event.time)):
                    new_event = best_node.schedule_packet(pkt, event.time)
                else:
                    pkt.dropped = True
                    self.dropped_packets.append(pkt.id)
            # print(pkt)
        else:
            for n in self.node_heap:
                if event.node_id == n.id:
                    # print("[COMPLETED at NODE {}] {}".format(n.id, n.current_packet))
                    self.total_security += n.current_packet.security
                    self.total_wait_time += event.time - n.current_packet.packet_size - n.current_packet.start - n.current_packet.security
                    n.current_packet = None
                    new_event = n.run_packet(event.time)
        self.heapify(event.time)
        return new_event
