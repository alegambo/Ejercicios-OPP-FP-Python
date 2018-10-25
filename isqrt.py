import sys
class Isqrt:
        def __init__(self):
                pass
        @staticmethod
        def isqrt(a):
                x = a
                y = (x + 1) >> 1
                while y <  x :
                        x = y
                        y = (x + a // x) >> 1
                return x
        



def imprime(g, a):
       return  f"isrtq({a}) = {g}"

if __name__ == "__main__":
        o = int(sys.argv[1])
        i = Isqrt()
        print(imprime(i.isqrt(o), o))
