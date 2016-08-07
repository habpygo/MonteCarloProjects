# File distribution.py

class Distribution:
    def __init__(self, no_simulations, kind, mean, stdv, c = 0):
        self.no_simulations = no_simulations
        self.kind = kind
        self.mean = mean
        self.stdv = stdv
        self.c = c

        if self.kind == 'norm':
            print('number of simulations is \n', no_simulations)
            print('kind of distribution is \n', kind)
            print('mean is \n', mean)
            print('stdv is \n', stdv)
            print('c is \n', c)