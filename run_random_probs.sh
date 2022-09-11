#!/bin/zsh

probs=(0.9)

n_games=300

rm data/*

for i in $probs; do
    touch 'data/system_2.csv'
    touch 'data/system_1.csv'
    touch 'data/random_choice_'$i'.csv'
    python pacman.py -p System2Agent -n $n_games -l smallClassic -g DirectionalGhost -q --fname data/system_2.csv
    echo "---------------------------"
    python pacman.py -p System1Agent -n $n_games -l smallClassic -g DirectionalGhost -q --fname data/system_1.csv
    echo "---------------------------"
    python pacman.py -p RandomChoiceAgent -n $n_games -l smallClassic -g DirectionalGhost -q -a prob_sys1=$i --fname data/random_choice_$i.csv
    echo "---------------------------"
    mkdir 'plots/'random_choice_$i
    python viz_graphs.py --prob $i
    rm data/*
    echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^"
done
