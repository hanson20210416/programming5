#!/bin/bash
#SBATCH --job-name=assignment4
#SBATCH --output=assignment4.out  
#SBATCH --error=assignment4.err   
#SBATCH --account=zhe    
#SBATCH --partition=assemblix  
#SBATCH --nodes=1                      
#SBATCH --ntasks=1                     
#SBATCH --cpus-per-task=1              
#SBATCH --time=0-00:10:00               
#SBATCH --mem-per-cpu=400M
#SBATCH --array=0-4                    # Create 5 tasks (IDs 0 through 4)

INPUT_FILES=(
    "/data/datasets/NCBI/PubMed/pubmed21n0021.xml"
    "/data/datasets/NCBI/PubMed/pubmed21n0022.xml"
)

# Select the file corresponding to the current task
INPUT_FILE="${INPUT_FILES[$SLURM_ARRAY_TASK_ID]}"

# Activate your Python environment
source /homes/zhe/Desktop/programming/dsls1/bin/activate

# Run your Python script with the selected file
python3 /homes/zhe/Desktop/programming/p5/week4/assignment3.py "$INPUT_FILE"
