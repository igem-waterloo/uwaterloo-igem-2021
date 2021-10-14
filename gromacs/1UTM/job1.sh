#!/bin/bash
#SBATCH --account=def-bingalls
#SBATCH --job-name=job1-sehacker
#SBATCH --mail-user=sehacker@uwaterloo.ca
#SBATCH --nodes=1                # number of nodes
#SBATCH --ntasks-per-node=8      # request 8 MPI tasks per node
#SBATCH --cpus-per-task=4        # 4 OpenMP threads per MPI task => total: 8 x 4 = 32 CPUs/node
#SBATCH --mem=0                  # request all available memory on the node
#SBATCH --time=0-01:00           # time limit (D-HH:MM)

module purge  
module load StdEnv/2020 gcc/9.3.0 openmpi/4.0.3 gromacs/2021.2
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"

gmx mdrun -deffnm nvt