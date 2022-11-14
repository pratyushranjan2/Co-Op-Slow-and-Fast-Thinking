#!/bin/sh

for N in $(seq 200)
do
    python pacman.py -p System2Agent -n 100 -q -g DirectionalGhost -l mas_large --conf $1
done