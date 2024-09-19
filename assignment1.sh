#!/bin/bash
#SBATCH --job-name=numerical_integration       # Job name
#SBATCH --output=/home/shared/results.csv      # Output file
#SBATCH --nodes=1                              # Request 1 node
#SBATCH --ntasks=1                             # Number of tasks (processes)
#SBATCH --time=01:00:00                        # Time limit (hh:mm:ss)
#SBATCH --mem=4G                               # Memory per node
#SBATCH --partition=workstations               # Partition name (depends on your cluster setup)
#SBATCH --mail-user=z.he@st.hanze.nl           # Email address for notifications

# Load any necessary modules
module load python/3.8

# Set the bounds of the integral
a=0
b=3.14159  

# Create or clear the results file
echo "steps,difference" > results.csv

# Loop through different step sizes
for n in 10 100 1000 10000 100000 1000000
do
    python3 assignment1.py -a $a -b $b -n $n >> results.csv
done

echo "Integration complete. Results saved in results.csv"
