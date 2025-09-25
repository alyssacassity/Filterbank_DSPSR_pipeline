#!/bin/bash
#
#SBATCH --account=def-istairs
#SBATCH --time=6:00:00
#SBATCH --mem-per-cpu=4096M
#SBATCH --cpus-per-task=1
#SBATCH --job-name=npz-generator
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#
#
# csv file name
CSV="$1"

# mark working directory
WORKDIR=$(pwd)

# activate environment
cd ~/rrat
source .venv/bin/activate
cd
module load scipy-stack

# cd back to working directory
cd $WORKDIR

MJD="${CSV%%.csv}"

# number of lines 
N_LINES=$(wc -l < "$CSV")

for i in $(seq 0 $((N_LINES - 1))); do
    echo "----------"
    echo "Line $i"
    echo "Running command:"
    echo "python ~/Fitburst_analyzer_rrat_timing_karl/Fitburst_fil_generator_decoupled.py $i $CSV ."
    python ~/Fitburst_analyzer_rrat_timing_karl/Fitburst_fil_generator_decoupled.py "$i" "$CSV" .
done
