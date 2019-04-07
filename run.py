from classes import master_node, packet, time_event
import random
import json
import os


def get_config():
    """
    Initializes the parameter from 'config.json'
    """
    with open("config.json") as f:
        data = json.load(f)
    packet_rate = 0
    number_of_nodes = 0
    start_time = 0
    end_time = 0
    minimum_security = 0
    packet_size = 0
    for item in data:
        packet_rate = item['packet_rate']
        number_of_nodes = item['number_of_nodes']
        start_time = item['simulation_start_time']
        end_time = item['simulation_end_time']
        packet_size = item['packet_size']
        is_set_min_security = item['set_minimum_security_level']
        if is_set_min_security:
            minimum_security = item['minimum_security_level_value']
    return packet_rate, number_of_nodes, start_time, end_time, packet_size, minimum_security


def output(file, parameters):
    f = open(file, "w+")
    f.write("# Simulation Summary\n")
    f.write("Packet Rate: {}\n".format(parameters['packet_rate']))
    f.write("Number of nodes: {}\n".format(parameters['number_of_nodes']))
    f.write("Start: {}\n".format(parameters['start_time']))
    f.write("End: {}\n".format(parameters['end_time']))
    f.write("Packet Size: {}\n".format(parameters['packet_size']))
    f.write("Minimum Security provided: {}\n\n".format(parameters['minimum_security']))
    f.write("# Results\n")
    f.write("Guarantee Ratio: {}%\n".format(parameters['guarantee_ratio']))
    f.write("Average Security provided: {}\n".format(parameters['average_security']))
    f.write("Average Waiting Time: {}\n".format(parameters['average_waiting_time']))


def output_data(file, parameters):
    # print("{}, {}, {}, {}, {}, {}".format(parameters['packet_rate'], parameters['number_of_nodes'],
    #                                       parameters['minimum_security'], parameters['guarantee_ratio'],
    #                                       parameters['average_security'], parameters['average_waiting_time']))
    f = open(file, "a+", encoding='utf-8')
    f.write(str(parameters['packet_rate']))
    f.write(", ")
    f.write(str(parameters['number_of_nodes']))
    f.write(", ")
    f.write(str(parameters['minimum_security']))
    f.write(", ")
    f.write(str(parameters['guarantee_ratio']))
    f.write(", ")
    f.write(str(parameters['average_security']))
    f.write(", ")
    f.write(str(parameters['average_waiting_time']))
    f.write("\n")
    f.close()


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

    PACKET_RATE, NUMBER_OF_NODES, START_TIME, END_TIME, PACKET_SIZE, MIN_SECURITY = get_config()

    output_file = input("Specify output file (eg: output.txt): ")
    fi = open(output_file, "a+", encoding="utf-8")
    fi.write("Packet Rate, Number of Nodes, Minimum Security, Guarantee Ratio, Average Security, Average Waiting Time\n")
    fi.close()

    MIN_SECURITY = 0
    while MIN_SECURITY <= 10:
        PACKET_RATE = 1
        while PACKET_RATE <= 100:
            NUMBER_OF_NODES = 2
            while NUMBER_OF_NODES <= 16:
                packet_list, events = random_packets(int(PACKET_RATE * (END_TIME - START_TIME)), START_TIME, END_TIME,
                                                     PACKET_SIZE,
                                                     MIN_SECURITY)

                outputs = dict()
                outputs['packet_rate'] = PACKET_RATE
                outputs['number_of_nodes'] = NUMBER_OF_NODES
                outputs['start_time'] = START_TIME
                outputs['end_time'] = END_TIME
                outputs['packet_size'] = PACKET_SIZE
                outputs['minimum_security'] = MIN_SECURITY

                packet_list = sorted(packet_list, key=lambda x: x.start)



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
                    outputs['guarantee_ratio'] = (PACKET_RATE * (END_TIME - START_TIME) - len(master.dropped_packets)) * \
                                                 (100 / (PACKET_RATE * (END_TIME - START_TIME)))
                    outputs['average_security'] = master.total_security / ((PACKET_RATE * (END_TIME - START_TIME)) -
                                                                           len(master.dropped_packets))
                    outputs['average_waiting_time'] = master.total_wait_time / (
                                (PACKET_RATE * (END_TIME - START_TIME)) -
                                len(master.dropped_packets))

                except:
                    print("Encountered Error while writing {}".format(output_file))

                output_data(output_file, outputs)
                NUMBER_OF_NODES *= 2

            PACKET_RATE += 1

        MIN_SECURITY += 0.1


    # packet_list, events = random_packets(int(PACKET_RATE * (END_TIME - START_TIME)), START_TIME, END_TIME, PACKET_SIZE,
    #                                      MIN_SECURITY)
    #
    # outputs = dict()
    # outputs['packet_rate'] = PACKET_RATE
    # outputs['number_of_nodes'] = NUMBER_OF_NODES
    # outputs['start_time'] = START_TIME
    # outputs['end_time'] = END_TIME
    # outputs['packet_size'] = PACKET_SIZE
    # outputs['minimum_security'] = MIN_SECURITY
    #
    # packet_list = sorted(packet_list, key=lambda x: x.start)
    #
    # output_file = input("Specify output file (eg: output.txt): ")
    #
    # events = sorted(events, key=lambda x: x.time)
    #
    # master = master_node.MasterNode(number_of_processors=NUMBER_OF_NODES)
    #
    # packet_index = 0
    # while len(events) > 0 and packet_index < len(packet_list):
    #     event = events[0]
    #     # print()
    #     # print(event)
    #     events = events[1:]
    #     new_event = None
    #     if event.category == "arrival":
    #         # Arrival event
    #         new_event = master.process_event(event, packet_list[packet_index])
    #         packet_index += 1
    #
    #     else:
    #         # Completion event
    #         new_event = master.process_event(event)
    #
    #     if new_event is not None:
    #         events.append(new_event)
    #         events = sorted(events, key=lambda x: x.time)
    #
    # try:
    #     outputs['guarantee_ratio'] = (PACKET_RATE*(END_TIME-START_TIME) - len(master.dropped_packets)) *\
    #                                  (100/(PACKET_RATE*(END_TIME-START_TIME)))
    #     outputs['average_security'] = master.total_security/((PACKET_RATE*(END_TIME-START_TIME)) -
    #                                                          len(master.dropped_packets))
    #     outputs['average_waiting_time'] = master.total_wait_time/((PACKET_RATE*(END_TIME-START_TIME)) -
    #                                                               len(master.dropped_packets))
    #     output_data(output_file, outputs)
    # except:
    #     print("Encountered Error while writing {}".format(output_file))
