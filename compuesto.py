class Compuesto:
    def __init__(self,principal,yearly_rate,term_in_years):
        self.principal=principal
        self.yearly_rate=yearly_rate
        self.term_in_years=term_in_years
        self.monthly_rate=yearly_rate / 1200
        self.term_in_months=term_in_years*12
    def __iter__(self):
        return self
    def __next__(self):
        self.principal *= (1 + self.monthly_rate)
        return self.principal
    def payments1(self,func1):
        return [func1() for i in range(self.term_in_months)]
        
if __name__ == "__main__":
    a=Compuesto(10_000,21,2)
    print(a.payments1(a.__next__))