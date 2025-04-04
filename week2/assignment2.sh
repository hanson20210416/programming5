#!/bin/bash
#SBATCH --job-name="assignment2.py"             
#SBATCH --comment="assignment2"
#SBATCH --account=zhe            
#SBATCH --partition=assemblix         
#SBATCH --output=results.out              
#SBATCH --error=assignment2.err               
#SBATCH --time=0-00:10:00               
#SBATCH --nodes=1                      
#SBATCH --ntasks=32                    
#SBATCH --cpus-per-task=1              
#SBATCH --mem-per-cpu=400M

N=100000000
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

echo "Integration complete.the times Results saved in results.csv"
