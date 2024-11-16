"""
Module for numerical integration using trapezoidal rule.
"""

import argparse
import math

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

def exact_integral(lower_bound, upper_bound):
    """
    Calculates the exact integral of cos(x) from a to b.
    """
    return math.sin(upper_bound) - math.sin(lower_bound)

def main():
    """
    Main function to parse command-line arguments, perform numerical integration
    using the trapezoidal rule, and compare it with the exact integral of cos(x).

    This function:
    1. Parses the command-line arguments to get the bounds of integration and the
       number of steps.
    2. Defines the function to be integrated (cos(x)).
    3. Calls the trapezoidal integration function with the provided arguments.
    4. Computes the exact integral using the `exact_integral` function.
    5. Calculates the difference between the numerical result and the exact result.
    6. Prints the number of steps and the difference between the numerical and exact
       integral results.
    """
    parser = argparse.ArgumentParser(description='Numerical integral using the trapezoid rule')
    parser.add_argument("-a", help="The lower bound of the definite integral", type=float,
                        required=True)
    parser.add_argument("-b", help="The upper bound of the definite integral", type=float,
                        required=True)
    parser.add_argument("-n", help="The number of steps for the numerical approximation",
                        type=int, default=256)
    args = parser.parse_args()
    def func(value):
        return math.cos(value)
    numerical_result = trapezoid_rule(func, args.a, args.b, num_subdivisions=args.n)
    exact_result = exact_integral(args.a, args.b)
    difference = abs(numerical_result - exact_result)
    print(f"{args.n}, {difference}")

if __name__ == "__main__":
    main()
