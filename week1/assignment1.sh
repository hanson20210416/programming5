#!/bin/bash
#SBATCH --job-name="assignment1.py"             
#SBATCH --comment="assignment1"
#SBATCH --account=zhe            
#SBATCH --partition=assemblix         
#SBATCH --output=results.out              
#SBATCH --error=assignment1.err               
#SBATCH --time=0-00:10:00               
#SBATCH --nodes=1                      
#SBATCH --ntasks=8                    
#SBATCH --cpus-per-task=1              
#SBATCH --mem-per-cpu=400M

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
