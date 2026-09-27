#!/bin/bash
# B-17 stage B: where new places are born, under Allen's rule (arm 'both'). 7 at a time.
cd "$(dirname "$0")"
J=()
for seed in 1 2; do for base in pres p11; do for rule in R1 R3; do J+=("python b17.py $base both 1 1 $rule live $seed"); done; done; done
for base in pres p11; do J+=("python b17.py $base both 1 1 R3 frozen 1" "python b17.py $base both 1 1 R2 live 1" "python b17.py $base both 1 1 R4 live 1"); done
for base in pres p11; do for rule in R1 R3; do J+=("python b17.py $base both 1 0 $rule live 1"); done; done
for j in "${J[@]}"; do
  while [ "$(jobs -rp | wc -l)" -ge 7 ]; do sleep 5; done
  bash -c "$j" >> b17_stageB.log 2>&1 &
done
wait; echo DONE >> b17_stageB.log
