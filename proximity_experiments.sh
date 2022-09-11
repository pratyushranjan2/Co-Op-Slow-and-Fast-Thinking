#!/bin/bash

# Parameters
sys_to_use=(1 2)
proxi_dist=(1 2 3 4 5)
n_games=2000
data_path='./aws_data'

# parameters for mini sample run
# n_games=3
# data_path='./mini_aws_data'

mkdir $data_path/proximity
data_path=$data_path/proximity

echo $data_path

rm $data_path/*

# Run multiple random probs
for p in "${proxi_dist[@]}"; do
    for sys in "${sys_to_use[@]}"; do
        touch $data_path'/proximity_agent_proxi_'$p'_sys_'$sys'.csv'
        python2 pacman.py -p ProximityAgent -n $n_games -l smallClassic -g DirectionalGhost -q -a proxi_dist=$p,escape_sys=$sys --fname $data_path'/proximity_agent_proxi_'$p'_sys_'$sys'.csv'
        echo '>>Proximity Agent Dist ('$p') Escape system ('$sys') - Complete<<'
    done
done


echo "All done"
