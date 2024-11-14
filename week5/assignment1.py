"""
Module for numerical integration using trapezoidal rule.
"""
import cProfile
import argparse
import math

def trapezoid(func, a, b, *, n=256):
    """
    Calculates the definite integral of the function f(x)
    from a to b using the composite trapezoidal rule with
    n subdivisions.
    """
    step_size = (b - a) / n
    integral = (func(a) + func(b)) * step_size / 2
    for i in range(1, n):
        xi = a + step_size * i
        integral += func(xi) * step_size
    return integral

def exact_integral(a, b):
    """
    Calculates the exact integral of cos(x) from a to b.
    """
    return math.sin(b) - math.sin(a)

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
    parser = argparse.ArgumentParser(description='Numerical integration using trapezoid rule')
    parser.add_argument("-a", help="The lower bound of the integral", type=float, required=True)
    parser.add_argument("-b", help="The upper bound of the integral", type=float, required=True)
    parser.add_argument("-n", help="steps to take in approximation", type=int, required=True)
    args = parser.parse_args()
    def func(value):
        return math.cos(value)
    numerical_result = trapezoid(func, args.a, args.b, n=args.n)
    exact_result = exact_integral(args.a, args.b)
    difference = abs(numerical_result - exact_result)
    print(f"{args.n}, {difference}")

if __name__ == "__main__":
    #main()
    cProfile.run('print(main()); print()')
