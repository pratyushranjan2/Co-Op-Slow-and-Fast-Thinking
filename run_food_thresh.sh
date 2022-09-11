#!/bin/zsh

probs=(0.3 0.9)

n_games=300

# rm data/*

for i in $probs; do
    touch 'data/food_thresh_'$i'.csv'
    python pacman.py -p ProximityAndFoodAgent -n $n_games -l smallClassic -g DirectionalGhost -q -a food_thresh=$i --fname data/food_thresh_$i.csv
    echo "---------------------------"
done
python viz_graphs_food_thresh.py
echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^"
