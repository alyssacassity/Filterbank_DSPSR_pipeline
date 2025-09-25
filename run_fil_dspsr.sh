#!/bin/bash
#run dspsr -k CHIME -nsub 1 -F 1 -E pulsar.par *.fil on all fil in directory 
#SBATCH --account=def-istairs
#SBATCH --time=6:00:00
#SBATCH --mem-per-cpu=4096M
#SBATCH --cpus-per-task=1
#SBATCH --job-name=run-dspsr
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

# Directory with files
DIR="/home/acassity/scratch/J1541+47/data/dspsr"

# activate environment
cd ~/astro-work
source .venv/bin/activate
module use /project/6004902/chimepsr-software/v1/environment-module
cd
module load dspsr

# cd back to working directory
cd $DIR

for fil in "$DIR"/*.fil; do
    echo "Extracting .ar from $fil with DSPSR..."
    dspsr -k CHIME -nsub 1 -F 1 -E pulsar.par "$fil" -O "$fil"
done

