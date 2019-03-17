# Discrete Event Simulator


## Usage

	>>> python run.py
	
After running the file, the simulator will ask for the output file:

	    Specify output file (eg: output.txt): <enter output file>

## File Descriptions
* run.py - main executable file (edit to change the parameters)
* config.json - used for setting the simulation parameters
* classes/time_event.py - TimeEvent Class
* classes/packet.py - Packet Class
* classes/node.py - Node Class
* classes/master_node.py - MasterNode Class

## Changing Simulation Parameters
The following changes are to be made in the 'config.json':

    "number_of_packets": <NUM_OF_PACKETS>,
    "number_of_nodes" : <NUM_OF_NODES>,
    "simulation_start_time": <START_TIME>,
    "simulation_end_time": <END_TIME>,
    "packet_size" : <PACKET_SIZE>,
    "set_minimum_security_level": <true OR false>,
    "minimum_security_level_value": <MIN_SECURITY>