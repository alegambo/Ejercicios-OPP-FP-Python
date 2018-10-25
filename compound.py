"""
Autores: Juan Alfonso Miranda Bonilla ID: 111950373
		Marco Trigueros Soto ID: 402270078
		Alejandro Gamboa Barahona  ID: 115790444
		David Morales Hidalgo  ID: 116300616
		José Fabio Alfaro Quesada  ID:  207580494
"""
class Compuesto:
    def __init__(self, conditions):
        self.principal, self.yearly_rate , self.term_in_years = (conditions['principal'],
                                                 conditions['yearly_rate'],
                                                 conditions['term_in_years'])
        self.monthly_rate = self.yearly_rate / 1200
        self.term_in_months = self.term_in_years * 12
        self.step = 0;
        self.therange = range(self.term_in_months)

    def __iter__(self):
        return self

    def __next__(self):
        self.step += 1
        if self.step > len(self.therange):
            raise StopIteration
        self.principal *= (1 + self.monthly_rate)
        return self.principal

    def payments1(self):
        return (self.__next__() for i in self.therange)


def total_amount(payments):
    total = 0
    for i in range(len(payments)):
        total += payments[i]
    return total
    
def growth(payments, conditions):
    return payments[-1] - conditions['principal']
    
def print_table(conditions):
    #
    paymentsGen = Compuesto(conditions).payments1()
    payments = list(Compuesto(conditions).payments1())
    total_growth = growth(payments, conditions)
    #
    margin = " " * 3
    separation = " " * 3
    print(">> Conditions: principal=${principal:0,.2f}; rate={yearly_rate:0.2f}annually%;  term={term_in_years:0d}years <<".format(**conditions))
    header = f"{margin}Month{separation}Principal"
    underline = "-" * ( len(header) + len(margin) )
    print(underline)
    print(header)
    print(underline)
    n = len(payments)
    i = 0
    for v in paymentsGen:
        i += 1
        print(f"{margin}{(i):^5d}{separation}{v:>8,.2f}")
     
    print(underline)
    footer = f"{margin}{n:^5d}{separation}{total_growth:,>0,.2f}"
    print(footer)

def test():
    print("*** Simple Compound Interest ***")
    conditions = {'principal' : 10_000, 'yearly_rate' : 21, 'term_in_years' :2}
    print_table(conditions)



if __name__ == "__main__":
    test()