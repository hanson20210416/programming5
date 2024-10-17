#!/bin/bash
#SBATCH --job-name=assignment3
#SBATCH --output=assignment3.out
#SBATCH --error=assignment3.err
#SBATCH --array=0-19  
#SBATCH --time=2:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1


# source /Desktop/programming/dsls1/bin/ activate

INPUT_DIR="/homes/zhe/Desktop/programming/p5/week3/assignment3.py"
SLURM_ARRAY_TASK_ID='/data/datasets/NCBI/PubMed/pubmed21n0022.xml'
INPUT_FILE="${INPUT_DIR}/part_${SLURM_ARRAY_TASK_ID}"

python3 /homes/zhe/Desktop/programming/p5/week3/assignment3.py "$INPUT_FILE"

