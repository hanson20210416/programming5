# Programming Assignments (Week 1-5, Pretest, and Exam)

This repository contains my programming assignments for various computational tasks across five weeks, as well as pretest and exam solutions.

---

## Week 1
### Files:
- **assignment1.py**: Numerical integration using the trapezoidal rule.
  - Accepts the following arguments:
    - `-a`: Lower bound of the definite integral.
    - `-b`: Upper bound of the definite integral.
    - `-n`: Number of steps for numerical approximation.
  - Outputs: Number of steps and the error with the symbolic integral value (e.g., `1000, 0.000001`).

- **assignment1.sh**: Bash script to run the Python script for various `-n` values (10, 100, 1000, etc.). Results are saved to `results.csv`.

---

## Week 2
### Files:
- **assignment2.py**: Parallel computation of numerical integration using MPI.
  - Two methods implemented:
    - **Broadcast (bcast)**: Distributes tasks and collects results by gather.
    - **Reduce (reduce)**: Aggregates results directly.
  - Results are saved to `results.csv` and `results_reduce.csv`.

- **assignment2.sh**: SLURM script to run the tasks with 1-32 subtasks. Saves runtime data to `results.csv`.

---

## Week 3 
### Week 3 went wrong, So I uploaded the files outside here.
### Files:
- **assignment3.py**: Database operations using SQLAlchemy.
  - Connects to a database.
  - Creates 3 tables using Python classes.
  - Extracts specific information from an XML dataset and inserts it into the database.

- **assignment3.sh**: SLURM script to run `assignment3.py`. Tasks can be split into arrays. But sometimes goes wrong. So not present here.

---

## Week 4
### Files:
- **assignment4.py**: Analysis of data using PySpark.
  - Connects to the database created in Week 3.
  - Creates Spark DataFrames from the database tables.
  - Performs specific analyses on the DataFrames to answer predefined questions.

- **assignment4.sh**: SLURM script to run `assignment4.py`. Handles large-scale XML files (5 total, with 150,000+ articles).
- **Note** : Apply slurm to run the assignment3.py at week4 , the XML files are 5. It inserted 150000+ articles into my database. It causes the assignment4.py does not work anymore. (because of the computation resource)
  If I rerun my assignment3.sh, the 5 files will be covered by 1 XML file in my database, Then assigment4.py will work again.
- **assignment3.py at week4**
   The same implementation as at week3, but something changes at the main() just to make the assignment4.sh 
 to run.

---

## Week 5
### Files:
- **assignment1.py**: Modified to measure runtime by cProfile for optimization analysis.
- **assignment5.py**: Visualization of runtime results from Week 2 (`results.csv`).
  - Draws a plot to find the balance between computational resources and performance.

---

## Pretest
- **pretest_answers.py** and **pretest_answers.ipynb**: Solutions to pretest questions.

---

## Exam
- **exam_answers.py** and **exam_answers.ipynb**: Solutions to the exam questions.
  - Includes explanations for some tasks written in `.ipynb` files.

---

### Notes:
1. Some explanations are written in Jupyter notebooks (`.ipynb`) rather than directly in the `.py` files.
2. my code did not extract the month info from the XML file, So I calculated years at the week4 assignemnt.py(because the approaches are similar)
