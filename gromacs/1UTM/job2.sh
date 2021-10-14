#!/bin/bash
#SBATCH --account=def-bingalls
#SBATCH --job-name=job2-sehacker
#SBATCH --mail-user=sehacker@uwaterloo.ca
#SBATCH --nodes=1                # number of nodes
#SBATCH --mem=0                  # request all available memory on the node
#SBATCH --time=0-01:00           # time limit (D-HH:MM)

module purge  
module load StdEnv/2020 gcc/9.3.0 openmpi/4.0.3 gromacs/2021.2
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"

gmx mdrun -deffnm npt -nt 1