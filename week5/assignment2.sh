#!/bin/bash -l
#SBATCH --job-name="assignment2.py"                # Job name
#SBATCH --comment="assignment2"
#SBATCH --account=zhe                               # Your account
#SBATCH --partition=assemblix                       # Partition name
#SBATCH --output=results.out                         # Output file
#SBATCH --error=assignment5.err                     # Error file
#SBATCH --time=0-00:10:00                           # Job time limit (1 hour)
#SBATCH --nodes=1                                   # Number of nodes
#SBATCH --ntasks=32                                 # Number of tasks (total CPUs)
#SBATCH --cpus-per-task=1                           # CPUs per task (set to 1 if using multiple tasks)
#SBATCH --mem-per-cpu=400M 
N=10000000  
A=0        
B=3.14       

OUTPUT_FILE="results.csv"
echo "Workers,UserTime,SystemTime,ElapsedTime" > $OUTPUT_FILE 

for p in {1..32}
do
    echo "Running with $p workers..."
    # Capture user, system, and elapsed time separately
    { /usr/bin/time -f "%U,%S,%e" mpirun -np $p python3 assignment2.py -a $A -b $B -n $N; } 2>&1 | \
    awk -v workers="$p" '{print workers "," $0}' >> $OUTPUT_FILE
done

echo "done"
