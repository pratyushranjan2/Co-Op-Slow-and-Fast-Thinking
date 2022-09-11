#!/bin/bash

touch ./aws_data/proximity/proximity_agent_proxi_1_sys_1_part_2.csv
python2 pacman.py -p ProximityAgent -n 10 -l smallClassic -g DirectionalGhost -q -a proxi_dist=1,escape_sys=1 --fname ./aws_data/proximity/proximity_agent_proxi_1_sys_1_part_2.csv
echo "Finished part 1"

touch ./aws_data/proximity/proximity_agent_proxi_1_sys_2_part_2.csv
python2 pacman.py -p ProximityAgent -n 10 -l smallClassic -g DirectionalGhost -q -a proxi_dist=1,escape_sys=2 --fname ./aws_data/proximity/proximity_agent_proxi_1_sys_2_part_2.csv
echo "Finished part 2"

touch ./aws_data/proximity/proximity_agent_proxi_2_sys_1_part_2.csv
python2 pacman.py -p ProximityAgent -n 10 -l smallClassic -g DirectionalGhost -q -a proxi_dist=2,escape_sys=1 --fname ./aws_data/proximity/proximity_agent_proxi_2_sys_1_part_2.csv
echo "Finished part 3"

touch ./aws_data/proximity/proximity_agent_proxi_2_sys_2_part_2.csv
python2 pacman.py -p ProximityAgent -n 10 -l smallClassic -g DirectionalGhost -q -a proxi_dist=2,escape_sys=2 --fname ./aws_data/proximity/proximity_agent_proxi_2_sys_2_part_2.csv
echo "Finished part 4"

# touch ./aws_data/proximity/proximity_agent_proxi_3_sys_1_part_2.csv
# python2 pacman.py -p ProximityAgent -n 0 -l smallClassic -g DirectionalGhost -q -a proxi_dist=3,escape_sys=1 --fname ./aws_data/proximity/proximity_agent_proxi_3_sys_1_part_2.csv

touch ./aws_data/proximity/proximity_agent_proxi_3_sys_2_part_2.csv
python2 pacman.py -p ProximityAgent -n 10 -l smallClassic -g DirectionalGhost -q -a proxi_dist=3,escape_sys=2 --fname ./aws_data/proximity/proximity_agent_proxi_3_sys_2_part_2.csv
echo "Finished part 5"

# touch ./aws_data/proximity/proximity_agent_proxi_4_sys_1_part_2.csv
# python2 pacman.py -p ProximityAgent -n 0 -l smallClassic -g DirectionalGhost -q -a proxi_dist=4,escape_sys=1 --fname ./aws_data/proximity/proximity_agent_proxi_4_sys_1_part_2.csv

touch ./aws_data/proximity/proximity_agent_proxi_4_sys_2_part_2.csv
python2 pacman.py -p ProximityAgent -n 10 -l smallClassic -g DirectionalGhost -q -a proxi_dist=4,escape_sys=2 --fname ./aws_data/proximity/proximity_agent_proxi_4_sys_2_part_2.csv
echo "Finished part 6"

# touch ./aws_data/proximity/proximity_agent_proxi_5_sys_1_part_2.csv
# python2 pacman.py -p ProximityAgent -n 0 -l smallClassic -g DirectionalGhost -q -a proxi_dist=5,escape_sys=1 --fname ./aws_data/proximity/proximity_agent_proxi_5_sys_1_part_2.csv

touch ./aws_data/proximity/proximity_agent_proxi_5_sys_2_part_2.csv
python2 pacman.py -p ProximityAgent -n 10 -l smallClassic -g DirectionalGhost -q -a proxi_dist=5,escape_sys=2 --fname ./aws_data/proximity/proximity_agent_proxi_5_sys_2_part_2.csv
echo "Finished part 7"
