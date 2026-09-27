#!/bin/bash
# B-17 stage A + switch check + gentle arm. 7 at a time.
cd "$(dirname "$0")"
jobs_list=()
for seed in 1 2; do for base in pres p11; do for arm in old both commit; do for hs in "0 0" "1 0" "0 1" "1 1"; do
  jobs_list+=("python b17.py $base $arm $hs R1 live $seed"); done; done; done; done
for arm in old both; do for hs in "0 0" "1 1"; do jobs_list+=("python b17.py pres $arm $hs R1 live 1 1.5"); done; done
for hb in 100 50; do for arm in old both; do for p in 0.8 0.9 1.1 1.25; do
  jobs_list+=("B17_HB=$hb python b17.py pres $arm 0 0 R1 live 1 $p"); done; done; done
for j in "${jobs_list[@]}"; do
  while [ "$(jobs -rp | wc -l)" -ge 7 ]; do sleep 5; done
  bash -c "$j" >> b17_stageA.log 2>&1 &
done
wait; echo DONE >> b17_stageA.log
