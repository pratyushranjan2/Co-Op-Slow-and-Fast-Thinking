#!/bin/bash

# Parameters
probs=(0.3 0.5 0.7 0.9)
food_thresh=(0.1 0.3 0.5 0.7 0.9)
n_games=4000
data_path='aws_data'

# parameters for mini sample run
# n_games=3
# data_path='mini_aws_data'

rm $data_path/*

# # Create all data files
touch $data_path'/system_2.csv'
touch $data_path'/system_1.csv'

for i in "${probs[@]}"; do
    touch $data_path'/random_choice_'$i'.csv'
done

touch $data_path'/proximity_agent.csv'

for i in "${food_thresh[@]}"; do
    touch $data_path'/food_thresh_'$i'.csv'
done

echo "All data files created"

# Set system 2 baseline
python2 pacman.py -p System2Agent -n $n_games -l smallClassic -g DirectionalGhost -q --fname $data_path/system_2.csv
echo ">>>System 2 - Complete<<<"

# Set system 1 baseline
python2 pacman.py -p System1Agent -n $n_games -l smallClassic -g DirectionalGhost -q --fname $data_path/system_1.csv
echo ">>>System 1 - Complete<<<"

# Run proximity system
touch $data_path'/proximity_agent.csv'
python2 pacman.py -p ProximityAgent -n $n_games -l smallClassic -g DirectionalGhost -q --fname $data_path'/proximity_agent.csv'
echo ">>>Proximity Agent - Complete<<<"

touch $data_path'/proximity_agent.csv'
python2 pacman.py -p ProximityAgent -n $n_games -l smallClassic -g DirectionalGhost -q --fname $data_path'/proximity_agent.csv'
echo ">>>Proximity Agent - Complete<<<"

touch $data_path'/random_choice_0.1.csv'
python2 pacman.py -p RandomChoiceAgent -n 23 -l smallClassic -g DirectionalGhost -q -a prob_sys1=0.1 --fname $data_path'/random_choice_0.1.csv'
echo '>>Random choice 0.1 - Complete<<'

# Run multiple random probs
for i in "${probs[@]}"; do
    touch $data_path'/random_choice_'$i'.csv'
    echo "Running prob "$i
    python2 pacman.py -p RandomChoiceAgent -n $n_games -l smallClassic -g DirectionalGhost -q -a prob_sys1=$i --fname $data_path'/random_choice_'$i'.csv'
    echo '>>Random choice ('$i') - Complete<<'
done


# Run proximity plus food density system
for i in "${food_thresh[@]}"; do
    touch $data_path'/food_thresh_'$i'.csv'
    echo "Running food thre "$i
    python2 pacman.py -p ProximityAndFoodAgent -n $n_games -l smallClassic -g DirectionalGhost -q -a food_thresh=$i --fname $data_path'/food_thresh_'$i'.csv'
    echo '>>Proximity plus food ('$i') - Complete<<'
done


echo "All done"
