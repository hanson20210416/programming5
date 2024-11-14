"""Module for numerical integration using the trapezoidal rule with MPI."""

import argparse
import math
from mpi4py import MPI

def compute_cosine(x):
    """Calculate the cosine of x."""
    return math.cos(x)

def trapezoidal_integration(func, lower_bound, upper_bound, *, num_steps=256):
    """Calculate the definite integral of the function func from lower_bound to upper_bound
    using the composite trapezoidal rule with num_steps subdivisions (default num_steps=256).
    """
    step_size = (upper_bound - lower_bound) / num_steps
    integral_value = (func(lower_bound) + func(upper_bound)) * step_size / 2
    for i in range(1, num_steps):
        x_i = lower_bound + step_size * i
        integral_value += func(x_i)
    return integral_value

def distribute_integration_bounds(lower_bound, upper_bound, num_processes, comm):
    """Distribute the integration bounds among the available processes."""
    rank = comm.Get_rank()
    chunk_size = (upper_bound - lower_bound) / num_processes
    local_lower_bound = lower_bound + rank * chunk_size
    local_upper_bound = local_lower_bound + chunk_size if rank < num_processes - 1 else upper_bound
    return local_lower_bound, local_upper_bound

def main():
    """Main function to perform numerical integration using MPI."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    num_processes = comm.Get_size()
    if rank == 0:
        parser = argparse.ArgumentParser(description='Numerical \
            integral using the trapezoid rule')
        parser.add_argument("-a", help="the lower bound of the definite integral",
                            type=float, required=True)
        parser.add_argument("-b", help="the upper bound of the definite integral", type=float,
                            required=True
                            )
        parser.add_argument("-n", help="the number of steps to take \
            in your numerical approximation",
                            type=int,default=256)
        args = parser.parse_args()
        lower_bound = args.a
        upper_bound = args.b
        num_steps = args.n
        print('rank0')
    else:
        lower_bound = None
        upper_bound = None
        num_steps = None
    # Broadcast the values of lower_bound, upper_bound,
    # and num_steps from the root process to all processes
    lower_bound = comm.bcast(lower_bound, root=0)
    upper_bound = comm.bcast(upper_bound, root=0)
    num_steps = comm.bcast(num_steps, root=0)

    local_steps = num_steps // num_processes
    local_lower_bound, local_upper_bound = distribute_integration_bounds(lower_bound,
                                                                         upper_bound,
                                                                         num_processes,
                                                                         comm
                                                                         )

    # Each process computes its own portion of the integral
    local_integral = trapezoidal_integration(compute_cosine, local_lower_bound,
                                             local_upper_bound,
                                             num_steps=local_steps
                                             )
    print(f"Process {rank}: local_lower_bound = {local_lower_bound}, \
          local_upper_bound = {local_upper_bound}")

    total_integral = comm.reduce(local_integral, op=MPI.SUM, root=0)
    if rank == 0:
        total_integral *= (upper_bound - lower_bound) / num_steps
        print(f"Approximate integral of cos(x) from {lower_bound} \
            to {upper_bound} with {num_steps} steps: {total_integral}")

if __name__ == '__main__':
    main()
