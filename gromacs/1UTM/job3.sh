#!/bin/bash
#SBATCH --account=def-bingalls
#SBATCH --job-name=job3-sehacker
#SBATCH --mail-user=sehacker@uwaterloo.ca
#SBATCH --mail-type=ALL
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --ntasks=16
#SBATCH --time=4-00:00           # time limit (D-HH:MM)

module purge  
module load StdEnv/2020 gcc/9.3.0 openmpi/4.0.3 gromacs/2021.2
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"

gmx mdrun -deffnm md_0_10