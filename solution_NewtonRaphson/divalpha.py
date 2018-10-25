"""
 Versiones no OOP de funciones de polinomios
 @author loriacarlos@gmail.com 
 @since 2018
"""
from functools import reduce

from div import add_x_to, ZERO
import utils as ut

def divalpha(poly, alpha):
    def div_step(acc, c):
        (last, q) = acc
        new = c - alpha * last
        return (new, (*q, new))
    #
    if len(poly) == 1: # p(x)=c and  c // (x - alpha) = 0 remainder is 0
       return ZERO, poly
    #
    first_poly, rest_poly = poly[0], poly[1:]
    rem, quotient = reduce(div_step, rest_poly, (first_poly, (first_poly,)))
    #
    return (list(quotient[:-1]), [rem])

if __name__ == '__main__':
    print("\n*** Alpha Synthetic Division ***") 
    tests = [
        ([10, -20, 10], -1),
        ([1, -3, 3, -1], -1),
        ([1, -3, 3, -1], 0),
        ([2, 1], -1),
        ([10], -5),
        ([1,-2,1,0], 0),
        ([1, -6, 12, -8], -2)
    ]
    for (case, (poly, alpha)) in enumerate(tests):
        print(f"\n{case+1}) Alpha-Dividing {add_x_to(poly)} by {add_x_to([1, alpha])}")
        q, r = divalpha(poly, alpha)
        print(f"Result: quotient= {add_x_to(q)} remainder= {add_x_to(r)}")
    
    