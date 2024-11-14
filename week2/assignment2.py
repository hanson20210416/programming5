# author = Zhipeng He
"""This module performs trapezoidal integration using MPI for parallel computation."""
import argparse
import math
from mpi4py import MPI

def cos_function(x):
    """Returns the cosine of x."""
    return math.cos(x)

def trapezoid_rule(func, lower_bound, upper_bound, *, num_subdivisions=256):
    """Calculate the integral using the trapezoidal rule.
    
    Args:
        func: The function to integrate.
        lower_bound: The lower bound of integration.
        upper_bound: The upper bound of integration.
        num_subdivisions: The number of subdivisions (default 256).
    
    Returns:
        The approximate integral.
    """
    step_size = (upper_bound - lower_bound) / num_subdivisions
    integral = (func(lower_bound) + func(upper_bound)) * step_size / 2
    for i in range(1, num_subdivisions):
        x_i = lower_bound + step_size * i
        integral += func(x_i)
    return integral

def distribute_bounds(lower_bound, upper_bound, num_processes, comm):
    """Distribute the integration bounds across processes."""
    rank = comm.Get_rank()
    chunk_size = (upper_bound - lower_bound) / num_processes
    local_lower_bound = lower_bound + rank * chunk_size
    local_upper_bound = local_lower_bound + chunk_size if rank < num_processes - 1 else upper_bound
    return local_lower_bound, local_upper_bound

def main():
    """Main function to handle the distributed numerical integration."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    if rank == 0:
        parser = argparse.ArgumentParser(description='Numerical integral using the trapezoid rule')
        parser.add_argument("-a", help="The lower bound of the definite integral", type=float,
                            required=True)
        parser.add_argument("-b", help="The upper bound of the definite integral", type=float,
                            required=True)
        parser.add_argument("-n", help="The number of steps for the numerical approximation",
                            type=int, default=256)
        args = parser.parse_args()
        lower_bound = args.a
        upper_bound = args.b
        num_steps = args.n
    else:
        lower_bound = None
        upper_bound = None
        num_steps = None
    lower_bound = comm.bcast(lower_bound, root=0)
    upper_bound = comm.bcast(upper_bound, root=0)
    num_steps = comm.bcast(num_steps, root=0)
    local_lower_bound, local_upper_bound = distribute_bounds(lower_bound, upper_bound, size, comm)
    local_num_steps = num_steps // size
    local_integral = trapezoid_rule(cos_function, local_lower_bound, local_upper_bound,
                                    num_subdivisions=local_num_steps)
    total_integral = comm.reduce(local_integral, op=MPI.SUM, root=0)

    if rank == 0:
        total_integral = total_integral * ((upper_bound - lower_bound) / num_steps)
        print(f"Approximate integral of cos(x) from {lower_bound} to {upper_bound} with \
              {num_steps} steps: {total_integral}")

if __name__ == '__main__':
    main()

