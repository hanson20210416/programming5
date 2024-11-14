#!/bin/bash
#SBATCH --job-name=pubmed_analysis
#SBATCH --output=pubmed_analysis.out
#SBATCH --error=pubmed_analysis.err
#SBATCH --time=01:00:00
#SBATCH --mem=4G
#SBATCH --ntasks=1

module load python/your_python_version
python assignment4.py
