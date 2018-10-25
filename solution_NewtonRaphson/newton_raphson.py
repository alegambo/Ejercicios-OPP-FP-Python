"""
Demo irrelevante sobre newthon-raphson solo para ejercicio de FP
Se debe implementar todo lo que dice 'todo'
@author loriacrlos@gmail.com
@since II-2018
"""



from div import *

from divalpha import *

import operator as op

from functools import reduce

import itertools as it

import utils as ut

class Poly(list):
    """
        Polynom as coeffcients list
    """
    def __init__(self, *args, var = "x"):
        """ Creates polynom """
        if len(args) == 0: args = (0,)
        super(Poly, self).__init__( args )
        self.var = var
        self.epsilon = 1e-8
        self.max = 30
        self.args = args
        
    @property
    def coefs(self):
        yield from self.args
    
    def __str__(self):
        return add_x_to(self)
        
    def __repr__(self):
        return str(self)
        
    @property
    def dx(self):
        """ Derivates the polynome """
        return Poly(*poly_dx(self))
        
    def __call__(self, val):
        """ Evaluates the polynom """
        return poly_eval(self, val)
        
    def __mul__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError("Multiplication expects a Poly")
            
        other_scaled = list(map(lambda p : other.scale(p[1], p[0]), 
                                enumerate(list(reversed(list(self.coefs)))) ))
        
        return reduce(lambda a, p : a + p, other_scaled, ZERO)
        
    def scale(self, c, d): # returns self * (cx**d)
        if c == 0 : return ZERO
        return Poly(* list (map (lambda cp : c * cp, self.coefs) ) + ([0] * d) )
        
    def adjust(self, n): # adds n letf zeroes to self
        if n <= self.degree: return self
        return Poly(*([0]*(n - self.degree) + list(self.coefs)))   
        
    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError("Addition expects Poly")
        if self.is_zero: return other
        if other.is_zero: return self
        n = max(self.degree, other.degree)
        (p, q) = (self.adjust(n), other.adjust(n))
       
        return Poly(* map( op.add, p.coefs, q.coefs) )
        
    @property
    def degree(self):
        """ Polynom´s degree. Must be aproperty """
        
        nz = [* it.dropwhile(lambda x : x == 0, self.coefs) ]
        return max(0, (len(nz) - 1))
    @property
    def is_zero(self):
        return self.degree == 0 and not any(self.coefs)
    def solve(self, r0=None ):
        """ Solves by Newton-raphson starting in r0 """
       
        if not r0:
            r0 = self[-1] / (self[0]*self.degree)
        return solve_newton(self, r0, max=self.max, epsilon=self.epsilon)
    
    def __floordiv__(self, alpha):
        """ Performs synthetic division by x - alpha """
        q, _ = divalpha(self, alpha)
        return Poly(*q)
    
    def roots(self):
        """ Finds all root by using solve and // repeatedly """
        n = len(self)
        
        if n == 0: 
           raise StopIteration()
        
        if n == 1: # p(x) = c
           c = self[0]
           if c != 0: # No solution if c != 0
               yield ut.NaN
           else: 
               yield ut.Infinity # Any real is solution
           
           raise StopIteration()
        
        if n == 2: # p(x) = ax + b with a != 0
            yield -self[1] / self[0]
            
        if n == 3: # p(x) = ax**2 + bx + c with a != 0
            yield from solve_formula(self)
            raise StopIteration()
            
        # p(x) = a_0*x**n + ... + a_{n-1} with a_0 != 0, n >= 2
        # Reduces self by Newton-Raphson until degree is less than 3
        p = self
        for (p, alpha) in solve_by_reduction(p) :
            if alpha: # First alpha is None, ignore it
               yield alpha
            if p.degree < 3: 
               break
        # Now p.degree < 3               
        yield from p.roots()
        
ZERO = Poly(0)
        

def solve_by_reduction(p)  :
    """ 
       Yields (p_0, None), (p_1, alpha_0), (p_2, alpha_1) ...
       where p_0 = p, alpha_0 = None
             alpha_i = a Newton-Raphson root of p_i
             p_{i+1} = p_i // - alpha_i
             
    """
    def solve_divide(state):
        (p, _) = state
        alpha = p.solve()
        return (p // - alpha, alpha)
        
    yield from ut.iterate(solve_divide, (p, None))

if __name__ == "__main__":
    print("*** Revisión Newton-Raphson 22/10/2018 ***")
    print("*** Caso Conocido *** ")
    p = Poly(1, -7, 7, 15)
    print(p)
    print(p(3))
    print(p.dx)
    print(p.solve(3))
    print(p // -5) # <-- Ojo - alpha en mi caso 
    print( list( map(lambda n: round(n, 6), p.roots()) ) ) # <- redondeo
    print()
    #
    print("*** Caso Nuevo *** ")
    p = Poly(16, 136, -40, -784, 384, 0)
    print(p)
    print(p(0.5))
    print(p.dx)
    print(p.solve())
    print(p // -0.5) # <-- Ojo - alpha en mi caso 
    print( list( map(lambda n: round(n, 6), p.roots()) ) ) # <- redondeo
    
    ############## Other test cases #####################
    print()
    print("*** Caso Final *** ")
    p = Poly(1, -3, 0, 4)
    print(p)
    print( list( map(lambda n: round(n, 6), p.roots()) ) ) # <- redondeo
    
    
    
    
    
    
    