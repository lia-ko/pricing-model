import math
import numpy as np


class CSimulation(object):
    option_type_b = {
        'Call': True,
        'Put': False
    }

    step = 0.10
    n = 20000

    s0 = 50
    k = 50
    r = 0.05
    sigma = 0.3
    t = 0.5
    is_call = True

    def __init__(self):
        self.eps = np.random.standard_normal(self.n)
        self.stock_prices = []
        self.option_payoffs = []
        self.gamma = []

    def run(self):
        for i in range(self.n):
            sp = self.s0 * math.exp((self.r - self.sigma**2/2)*self.t + self.sigma*math.sqrt(self.t)*self.eps[i])
            if self.is_call:
                op = math.exp(-self.r*self.t)*max(sp - self.k, 0)
            else:
                op = math.exp(-self.r * self.t) * max(self.k - sp, 0)

            sp1 = sp + self.step
            if self.is_call:
                op1 = math.exp(-self.r*self.t)*max(sp1 - self.k, 0)
            else:
                op1 = math.exp(-self.r*self.t)*max(self.k - sp1, 0)

            g = (op1 - op)/self.step

            self.stock_prices.append(sp)
            self.option_payoffs.append(op)
            self.gamma.append(g)

    def process_results(self):
        pf = np.array(self.option_payoffs)
        self.pf_mean = pf.mean()
        self.pf_std = pf.std()

        gm = np.array(self.gamma)
        self.gm_mean = gm.mean()
        self.gm_std = gm.std()
