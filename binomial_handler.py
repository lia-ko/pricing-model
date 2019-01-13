import math


class CTreeNode(object):
    u_price = 0.0           # Price of underlying
    opt_price = 0.0         # Price of option
    intrinsic_value = 0.0   # Exercise value
    is_ex = False            # Exercise indicator


class CTreeBranch(object):
    def __init__(self):
        self.node = []               # CTreeNode() Node structure

    n_nodes = 0
    cur_time = 0.0          # time at this step
    pv_div = 0.0            # PV of future dividends at this step


class CTree(object):
    def __init__(self):
        self.branch = []         # CTreeBranch() Branch structure

    n_steps = 0             # Total time steps of the tree
    dt = 0.0                # length of time step
    u = 0.0                 # up step
    d = 0.0                 # down step
    disc = 0.0              # discount factor
    growth = 0.0            # growth factor for underlying price
    pu = 0.0                # up probability
    pd = 0.0                # down probability


class CList(object):
    def __init__(self):
        self.vv = []
        self.tt = []


class CHandler(object):
    one_day = 1.0/365.0

    underlier_types = {
        'Equity': 1,
        'Currency': 2,
        'Index': 3,
        'Futures': 4
    }

    option_type_a = {
        'American': True,
        'European': False
    }

    option_type_b = {
        'Call': True,
        'Put': False
    }

    equity = 1
    currency = 2
    index = 3
    futures = 4

    underlying_type = index

    s = 300.     # 60 stock_price / futures price / Exchange Rate ($ / foreign): / Index Level:
    sigma = 20.   # 45 volatility
    r = 8.     # risk_free_rate
    q = 3.0     # Foreign Risk-free Rate (% per year): / Dividend Yield (% per yer):

    is_call = False
    is_american = False
#    imply_volatility = False

    t = 0.5         # 0.25 life_years
    x = 300.        # 60 strike_price
    n_steps = 3     # 3 tree_steps

    price = 0.0     # 5.162780851
    delta = 0.0     # -0.435574121
    gamma = 0.0     # 0.033753297
    vega = 0.0
    theta = 0.0     # -0.025253369
    rho = 0.0       # -0.06498894

    c_price = 0.0
    c_gamma = 0.0
    c_delta = 0.0
    c_theta = 0.0

    def __init__(self):
        self.price_tree = CTree()
        self.c_tree = CTree()
        self.div_list = CList()
        self.errors = []

    def handler(self):
        self.sigma = self.sigma * 0.01
        self.r = self.r * 0.01
        self.q = self.q * 0.01

        if self.is_not_valid_parameters():
            return False

        if self.underlying_type == self.futures:
            self.q = self.r

        dt = self.t/self.n_steps
        sig_min = (self.r - self.q) * math.sqrt(dt)
        if sig_min < 0.0001:
            sig_min = 0.0001

        if self.sigma < sig_min:
            self.errors.append("Volatility must be greater than {0:.6f}% for this tree".format(sig_min))
            return False

        t1 = 0.0

        try:
            self.tree_equity_opt(self.s, self.x, self.r, t1, self.t, self.q, self.sigma, self.n_steps, self.is_american, self.is_call)
            if self.underlying_type == self.futures:
                delta_q = 0.01
            else:
                delta_q = 0.0
            # assigning greeks
            self.price = self.c_price
            self.delta = self.c_delta
            self.gamma = self.c_gamma
            self.theta = self.c_theta
            self.price_tree = self.c_tree
            # tree equity
            self.tree_equity_opt(self.s, self.x, self.r + 0.01, t1, self.t, self.q + delta_q, self.sigma, self.n_steps, self.is_american, self.is_call)
            self.rho = self.c_price - self.price
        except:
            self.errors.append("Generic exception happened in calculations of binomial tree")
            return False

        return True

    def print_tree(self):
        result = ""
        layers = []

        for i in range(2, len(self.price_tree.branch) - 1):
            layer = []
            for j in range(1, len(self.price_tree.branch[i].node) - 1):
                s = '[S:' + str(round(self.price_tree.branch[i].node[j].u_price, 4)) + '/'
                s += 'O:' + str(round(self.price_tree.branch[i].node[j].opt_price, 4)) + ']'
                layer.append(s)

            layers.append(layer)

        layers = [' -- '.join(layers[i]) for i in range(len(layers) - 1, -1, -1)]

        sl = len(layers[0])

        layers = [self.space((sl - len(layer))//2) + layer  for layer in layers]

        result = '\n' + self.space((sl - 14)//2) + 'BINOMIAL TREE:' + '\n'
        for layer in layers:
            result += layer + '\n\n'

        return result

    @staticmethod
    def space(n):
        return ''.join([' ' for i in range(n)])

    def tree_equity_opt(self, s_in, x, r, t1, t, q, sig, steps, is_american, is_call):
        pv_div = 0.0
        s = s_in
        uprice_tree = CTree()

        for i in range(len(self.div_list.vv)):
            if 0.0 < self.div_list.tt[i] <= t:
                pv_div = pv_div + self.div_list.vv[i] * math.exp(-r * self.div_list.tt[i])

        s = s - pv_div

        self.build_tree(s, x, r, t1, t, q, self.div_list, sig, steps, is_american, is_call, uprice_tree)

        self.c_price = uprice_tree.branch[2].node[1].opt_price
        d_up = (uprice_tree.branch[4].node[3].opt_price - uprice_tree.branch[4].node[2].opt_price) / (uprice_tree.branch[4].node[3].u_price - uprice_tree.branch[4].node[2].u_price)
        d_dn = (uprice_tree.branch[4].node[2].opt_price - uprice_tree.branch[4].node[1].opt_price) / (uprice_tree.branch[4].node[2].u_price - uprice_tree.branch[4].node[1].u_price)

        self.c_gamma = 2.0 * (d_up - d_dn) / (uprice_tree.branch[4].node[3].u_price - uprice_tree.branch[4].node[1].u_price)
        self.c_delta = (uprice_tree.branch[3].node[2].opt_price - uprice_tree.branch[3].node[1].opt_price) / (uprice_tree.branch[3].node[2].u_price - uprice_tree.branch[3].node[1].u_price)
        self.c_theta = (uprice_tree.branch[4].node[2].opt_price - uprice_tree.branch[2].node[1].opt_price) / (2.0 * uprice_tree.dt) * self.one_day

        self.c_tree = uprice_tree

    def build_tree(self, s, x, r, t1, t, q, divs, sig, steps, is_american, is_call, uprice_tree):
        uprice_tree.n_steps = steps

        uprice_tree.branch = [CTreeBranch() for i in range(uprice_tree.n_steps + 3 + 1)]

        uprice_tree.dt = t / uprice_tree.n_steps
        uprice_tree.u = math.exp(sig * math.sqrt(uprice_tree.dt))
        uprice_tree.d = 1.0 / uprice_tree.u
        uprice_tree.disc = math.exp(-r * uprice_tree.dt)
        uprice_tree.growth = math.exp((r - q) * uprice_tree.dt)

        uprice_tree.pu = (uprice_tree.growth - uprice_tree.d) / (uprice_tree.u - uprice_tree.d)
        uprice_tree.pd = 1.0 - uprice_tree.pu

        for i in range(uprice_tree.n_steps + 2, 1, - 1):
            uprice_tree.branch[i].node = [CTreeNode() for m in range(i + 1)]
            # Set current date
            uprice_tree.branch[i].cur_time = (i - 2) * uprice_tree.dt

            # Calculating PV of dividends at this date
            uprice_tree.branch[i].pv_div = 0.0
            for k in range(len(self.div_list.vv)):
                t_div = divs.tt[k]
                if uprice_tree.branch[i].cur_time < t_div <= t:
                    t_div = t_div - uprice_tree.branch[i].cur_time
                    uprice_tree.branch[i].pv_div = uprice_tree.branch[i].pv_div + divs.vv[k] * math.exp(-r * t_div)

            for j in range(i):
                uprice_tree.branch[i].node[j].u_price = s * (uprice_tree.u ** (2 * j - i)) + uprice_tree.branch[i].pv_div
                if is_call:
                    uprice_tree.branch[i].node[j].intrinsic_value = uprice_tree.branch[i].node[j].u_price - x
                else:
                    uprice_tree.branch[i].node[j].intrinsic_value = x - uprice_tree.branch[i].node[j].u_price

                if uprice_tree.branch[i].node[j].intrinsic_value < 0.0:
                    uprice_tree.branch[i].node[j].intrinsic_value = 0.0

                if i == (uprice_tree.n_steps + 2):
                    uprice_tree.branch[i].node[j].opt_price = uprice_tree.branch[i].node[j].intrinsic_value
                    if uprice_tree.branch[i].node[j].intrinsic_value > 0.0:
                        uprice_tree.branch[i].node[j].is_ex = True
                    else:
                        uprice_tree.branch[i].node[j].is_ex = False
                else:
                    uprice_tree.branch[i].node[j].opt_price = (uprice_tree.pu * uprice_tree.branch[i + 1].node[j + 1].opt_price + uprice_tree.pd * uprice_tree.branch[i + 1].node[j].opt_price) * uprice_tree.disc
                    uprice_tree.branch[i].node[j].is_ex = False
                    if is_american and uprice_tree.branch[i].cur_time >= t1:
                        if uprice_tree.branch[i].node[j].intrinsic_value > uprice_tree.branch[i].node[j].opt_price:
                            uprice_tree.branch[i].node[j].opt_price = uprice_tree.branch[i].node[j].intrinsic_value
                            uprice_tree.branch[i].node[j].is_ex = True

    def is_not_valid_parameters(self):
        if self.s <= 0.0:
            self.errors.append("Price of underlying must be positive")
            return True

        if self.sigma < 0.0001 or self.sigma > 10.0 and not self.imply_volatility:
            self.errors.append("Volatility must be between 0.01% and 1000%")
            return True

        if self.r <= -0.1 or self.r > 1.0:
            self.errors.append("Risk-free rate must be between -10% and 100%")
            return True

        if self.underlying_type == self.currency:
            if self.q <= -0.1 or self.q > 1.0:
                self.errors.append("Foreign risk-free rate must be between -10% and 100%")
                return True
        elif self.underlying_type == self.index:
            if self.q < 0.0 or self.q > 1.0:
                self.errors.append("Dividend yield must be between 0% and 100%")
                return True

        if self.underlying_type == self.equity:
            for i in range(len(self.div_list.vv)):
                self.s = self.s - self.div_list.vv[i] * math.exp(-self.r * self.div_list.tt[i])

            if self.s <= 0:
                self.errors.append("Stock price must be greater than PV of dividends")
                return True

        if self.x <= 0:
            self.errors.append("Exercise price must be positive")
            return True

        if self.t <= 0:
            self.errors.append("Exercise date must be later than valuation date")
            return True

        if self.n_steps < 2:
            self.errors.append("Tree must have at least 2 steps")
            return True

        if self.n_steps > 500:
            self.errors.append("Tree must have no more than 500 steps")
            return True

        return False

#ch = CHandler()
#ch.handler()
#ch.print_tree()

#print('Price: ' + str(ch.price))
#print('Delta: ' + str(ch.delta))
#print('Gamma: ' + str(ch.gamma))
#print('Theta: ' + str(ch.theta))
#print('Rho: ' + str(ch.rho))