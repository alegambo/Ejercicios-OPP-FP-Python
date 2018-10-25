"""
Autores: Juan Alfonso Miranda Bonilla ID: 111950373
		Marco Trigueros Soto ID: 402270078
		Alejandro Gamboa Barahona  ID: 115790444
		David Morales Hidalgo  ID: 116300616
		José Fabio Alfaro Quesada  ID:  207580494
"""
import numpy as np

class Poly(list):
    """
        Polynom as coeffcients list
    """
    def __init__(self, *args, var = "x"):
        """ Creates polynom """
        super(Poly, self).__init__( args )
        self.var = var
        self.epsilon =1e-5
        self.max = 20
        self.deriv = np.poly1d(self).deriv()
        
    def __str__(self):
        deg = self.degree()
        ret = ""
        for elemt in self[:-2]:
            if elemt != 0:
                ret += f"{elemt if elemt !=1 else ''}{self.var}**{deg} + "
            deg -= 1
        return  f"{ret}{self[-2] if self[-2] !=1 else ''}{self.var} + {self[-1]}"

    def __repr__(self):
        return super(Poly, self).__repr__()
        
    #@property
    def dx(self):
        """ Derivates the polynome """
        return Poly(*(list(self.deriv)))
        
    def __call__(self, val):
        """ Evaluates the polynom """
        #todo(self.__call__)
        deg = self.degree()
        ret = 0
        for elemt in self[:-1]:
            ret += elemt*val**deg
            deg -= 1

        return ret + self[-1]
        
    #@property
    def degree(self):
        """ Polynom´s degree. Must be aproperty """
       # todo(self.degree, "Must be property")
        return len(self) - 1
        
    def solve(self, r0=None ):
        """ Solves by Newton-raphson starting in r0 """
        #todo(self.solve, "r0 must be a number")
        if not r0:
            r0 = self[-1] / self.degree()
        for i in range(self.max):
          #  print(r0)
          #  print(i)
            r0 = r0 - self.__call__(r0) / self.deriv(r0)

        return r0
    
    def __floordiv__(self, alpha):
        """ Performs synthetic division by x - alpha """
        '''  todo(self.__floordiv__, 
             "alpha must be a number", 
             "Returns a new poly"
            )
        '''
        ret = [self[0]]
        for i in self[1:]:
            ret.append(ret[-1]*alpha + i)

        return Poly(*(ret[:-1]))
    
    def roots(self):
        """ Finds all root by using solve and // repeatedly """

        ret = self.solve()
        temp = self
        yield ret
        for i in range(self.degree()-1):

            temp = temp.__floordiv__(ret)
            ret = temp.solve()
            yield ret


    
if __name__ == "__main__":
    print("Revision Newton-raphson 22/10/2018")
    print("***Caso Conocido***")
    p = Poly(1, -7, 7, 15)
    print(p)
    print(p(3))
    print(p.dx())
    print(p.solve())
    print(p // 5)
    print(list(p.roots()))
    print()
    print("***Caso Nuevo***")
    d = Poly(16, 136, -40, -784, 384, 0)
    print(d)
    print(d(3))
    print(d.dx())
    print(d.solve())
    print(d // 5)
    print(list(d.roots()))