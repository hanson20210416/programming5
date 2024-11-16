#!/bin/bash
#SBATCH --job-name=assignment3
#SBATCH --output=assignment3.out
#SBATCH --error=assignment3.err
#SBATCH --account=zhe    
#SBATCH --partition=assemblix  
#SBATCH --cpus-per-task=1
#SBATCH --time=0-00:10:00               
#SBATCH --nodes=1                      
#SBATCH --ntasks=8                    
#SBATCH --cpus-per-task=1              
#SBATCH --mem-per-cpu=400M


source home/zhe/Desktop/programming/dsls1/bin/activate

INPUT_DIR="/homes/zhe/Desktop/programming/p5/week3/assignment3.py"
SLURM_ARRAY_TASK_ID='/data/datasets/NCBI/PubMed/pubmed21n0021.xml'
INPUT_FILE="${INPUT_DIR}/part_${SLURM_ARRAY_TASK_ID}"

python3 /homes/zhe/Desktop/programming/p5/week3/assignment3.py "$INPUT_FILE"
