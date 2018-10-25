"""
 Versiones no OOP de funciones de polinomios
 @author loriacrlos@gmail.com
 @since II-2018
"""
from functools import reduce
import operator as op 
import math
import itertools as it
import utils as ut # Homemade combinators

def normalize(poly):
    normalizer = poly[0]
    return poly.copy() if normalizer == 1 else [c / normalizer for c in poly]
    
def poly_eval(poly, x):
    return reduce(lambda a, c: a*x + c, poly[1:], poly[0])
    
def poly_dx(poly):
    exps = list(range(len(poly)-1, 0, -1))
    return map( lambda p: op.mul(*p), zip(poly[0:len(poly)-1], exps) )
    
def solve_newton(poly, r0, max=20, epsilon=1e-6):
    pdx = list(poly_dx(poly)) # poly's derivate
    def approximations(): # yields approximations one by one
        def improve_root(state):
            (r, _) = state
            return (r - poly_eval(poly, r) / poly_eval(pdx, r), r)
        yield from ut.iterate( improve_root, (r0, None) )
        
    def close_enough(state): # Checks epsilon convergence
        (r, rlast) = state
        return rlast and abs(r - rlast) < epsilon
    #
    def not_yet_found(state): # Skips not final states 
        (nstate, rstate) = state
        return nstate < max and not close_enough(rstate)
    # Answer:
    solution_states = it.dropwhile(not_yet_found, enumerate(approximations()) )
    (_, (r_first, _) ) = ut.first(solution_states)
        
    return r_first
    

def solve_formula(poly):
    pn = normalize(poly)
    _, b, c = pn
    delta = b*b - 4*c
    
    if delta < 0:
        print(f"*** WARNING: Quadratic has no real solutions {poly}***")
        return ut.NaN, ut.NaN
    
    r1 = -(b + math.sqrt(delta)) / 2
    r2 = -b if r1 == 0 else c / r1
    return (r1, r2)
 
 
def add_x_to(poly, x="x"): 
    """ Converts poly:list to string with variable x:str """
    def monom(n):
        """ Returns monom x**n as string """
        if n == 0: return ""
        if n == 1: return x
        return f"{x}**{n}"
        
    def mult(c, e):
        """ Joins coeficient c:float and exponent e:str """
        if c == 0: return ""
        if c == 1: return f"+ {e if e else 1}"
        if c < 0: return f"- {-c}{e}"
        return f"+ {c}{e}"
        
    def first(c, e):
        """ Deals with joining the first monom """
        if c == 0: return ""
        if c == 1: return e if e else "1"
        if c == -1: return f"-{e}" if e else "-"
        return f"{c}{e} "
    #    
    deg = len(poly)
    if deg <= 1:
        return f"{poly[0]}"
    monoms = map( monom, range(deg - 1, -1, -1) )
    polyXmonoms = list(zip(poly, monoms))
    fce = first(*polyXmonoms[0])
    
    return f"{fce} " + " ".join(f"{mult(c, e)}" for (c, e) in polyXmonoms[1:])
    
ZERO = [0]
    


if __name__ == '__main__':
    print("\n*** Poly operations in FP Style  ***")
    p = [1, -5, 6]
    r0 = 1.5
    root = solve_newton(p, r0)
    print(f"Solve Newton {add_x_to(p)} r0={r0} root={round(root, 6)}")
    p = [2, -10, 12]
    r1, r2 = solve_formula(p)
    print(f"Solve formula {add_x_to(p)} r1={r1} r2={r2}")