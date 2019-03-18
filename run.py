from classes import master_node, packet, time_event
import random
import json


def get_config():
    """
    Initializes the parameter from 'config.json'
    """
    with open("config.json") as f:
        data = json.load(f)
    number_of_packets = 0
    number_of_nodes = 0
    start_time = 0
    end_time = 0
    minimum_security = 0
    packet_size = 0
    for item in data:
        number_of_packets = item['number_of_packets']
        number_of_nodes = item['number_of_nodes']
        start_time = item['simulation_start_time']
        end_time = item['simulation_end_time']
        packet_size = item['packet_size']
        is_set_min_security = item['set_minimum_security_level']
        if is_set_min_security:
            minimum_security = item['minimum_security_level_value']
    return number_of_packets, number_of_nodes, start_time, end_time, packet_size, minimum_security


def output(file, parameters):
    f = open(file, "w+")
    f.write("# Simulation Summary\n")
    f.write("Number of packets: {}\n".format(parameters['number_of_packets']))
    f.write("Number of nodes: {}\n".format(parameters['number_of_nodes']))
    f.write("Start: {}\n".format(parameters['start_time']))
    f.write("End: {}\n".format(parameters['end_time']))
    f.write("Packet Size: {}\n".format(parameters['packet_size']))
    f.write("Minimum Security provided: {}\n\n".format(parameters['minimum_security']))
    f.write("# Results\n")
    f.write("Guarantee Ratio: {}%\n".format(parameters['guarantee_ratio']))
    f.write("Average Security provided: {}\n".format(parameters['average_security']))
    f.write("Average Waiting Time: {}\n".format(parameters['average_waiting_time']))


def random_packets(number_packets, start, end, packet_size, min_security):
    """
    :param number_packets: Number of packets to be generated
    :param start: Start-time of simulation
    :param end: End-time of simulation
    :param packet_size: Processing time of each packet without any security
    :param min_security: Minimum security expected from each packet
    :return: List of randomly generated packets
    """
    packet_l = list()
    arrival_t = list()

    # RANDOM PACKETS GENERATION
    for i in range(number_packets):
        temp_start = round(random.uniform(start, end), 2)
        temp_min_sec = min_security + round(random.uniform(0, 10 - min_security), 2)
        temp_max_sec = round(random.uniform(temp_min_sec, 10), 2)
        temp_deadline = round(random.uniform(temp_start + packet_size + temp_min_sec, end), 2)
        temp = packet.Packet(i, temp_start, temp_deadline, temp_min_sec, temp_max_sec, packet_size)
        packet_l.append(temp)
        temp_time = time_event.TimeEvent(temp_start, "arrival")
        arrival_t.append(temp_time)

    return packet_l, arrival_t


if __name__ == '__main__':

    NUMBER_OF_PACKETS, NUMBER_OF_NODES, START_TIME, END_TIME, PACKET_SIZE, MIN_SECURITY = get_config()
    packet_list, events = random_packets(NUMBER_OF_PACKETS, START_TIME, END_TIME, PACKET_SIZE, MIN_SECURITY)

    outputs = dict()
    outputs['number_of_packets'] = NUMBER_OF_PACKETS
    outputs['number_of_nodes'] = NUMBER_OF_NODES
    outputs['start_time'] = START_TIME
    outputs['end_time'] = END_TIME
    outputs['packet_size'] = PACKET_SIZE
    outputs['minimum_security'] = MIN_SECURITY

    packet_list = sorted(packet_list, key=lambda x: x.start)

    output_file = input("Specify output file (eg: output.txt): ")

    events = sorted(events, key=lambda x: x.time)

    master = master_node.MasterNode(number_of_processors=NUMBER_OF_NODES)

    packet_index = 0
    while len(events) > 0 and packet_index < len(packet_list):
        event = events[0]
        # print()
        # print(event)
        events = events[1:]
        new_event = None
        if event.category == "arrival":
            # Arrival event
            new_event = master.process_event(event, packet_list[packet_index])
            packet_index += 1

        else:
            # Completion event
            new_event = master.process_event(event)

        if new_event is not None:
            events.append(new_event)
            events = sorted(events, key=lambda x: x.time)

    try:
        outputs['guarantee_ratio'] = (NUMBER_OF_PACKETS - len(master.dropped_packets)) * 100/NUMBER_OF_PACKETS
        outputs['average_security'] = master.total_security/(NUMBER_OF_PACKETS - len(master.dropped_packets))
        outputs['average_waiting_time'] = master.total_wait_time/(NUMBER_OF_PACKETS - len(master.dropped_packets))
        output(output_file, outputs)
    except:
        print("Encountered Error while writing {}".format(output_file))
