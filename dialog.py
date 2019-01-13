import sys
from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import Combobox
from binomial_handler import CHandler
from EuExplicit import EuExplicit
from EuImplicit import EuImplicit
from simulation import CSimulation


class Window(Frame):
    option_type_b = {
        'Call': True,
        'Put': False
    }

    def __init__(self, master=None, nr=1, nc=1):
        self.dt = []
        self.dv = []
        Frame.__init__(self, master)
        self.master = master
        self.init_window(nr, nc)

    def init_window(self, nr, nc):
        self.master.title("Option pricing  (by Ioulia Terechtchenko)")
        self.master.geometry('640x600')

        for i in range(nc):
            self.master.columnconfigure(i, weight=1)

        for i in range(nr):
            self.master.rowconfigure(i, weight=1)

        n_row = 0

        # Parameters
        lbl_parameters = Label(self.master, text='Enter parameters:', font=('Arial Bold', 12))
        lbl_parameters.grid(row=n_row, column=0, columnspan=5)

        n_row += 1
        lbl_method = Label(self.master, text='Select pricing method:')
        lbl_method.grid(row=n_row, column=0, sticky='e')
        self.cmb_method = Combobox(self.master, width=20, state='readonly')
        self.cmb_method.grid(row=n_row, column=1, sticky='w')
        self.cmb_method['values'] = ('Binomial', 'Explicit Difference', 'Implicit Difference', 'Monte Carlo')
        self.cmb_method.current(0)
        self.cmb_method.bind("<<ComboboxSelected>>", self.check_divs)


        lbl_div_time = Label(self.master, text='Time in years')
        lbl_div_time.grid(row=n_row, column=3, sticky='w')
        lbl_div = Label(self.master, text='Dividend')
        lbl_div.grid(row=n_row, column=4, sticky='w')
        for i in range(3):
            dt = Entry(self.master, width=10)
            dt.grid(row=n_row + i + 1, column=3, sticky='w')
            dv = Entry(self.master, width=10)
            dv.grid(row=n_row + i + 1, column=4, sticky='w')

            self.dt.append(dt)
            self.dv.append(dv)

        n_row += 1
        lbl_underlier = Label(self.master, text='Select underlier type:')
        lbl_underlier.grid(row=n_row, column=0, sticky='e')
        self.cmb_underlier = Combobox(self.master, width=15, state='readonly')
        self.cmb_underlier.grid(row=n_row, column=1, sticky='w')
        self.cmb_underlier['values'] = ('Equity', 'Currency', 'Index', 'Futures')
        self.cmb_underlier.current(0)
        self.cmb_underlier.bind("<<ComboboxSelected>>", self.check_divs)

        n_row += 1
        lbl_uprice = Label(self.master, text='Enter current price:')
        lbl_uprice.grid(row=n_row, column=0, sticky='e')
        self.txt_current_price = Entry(self.master, width=10)
        self.txt_current_price.grid(row=n_row, column=1, sticky='w')

        n_row += 1
        lbl_volatility = Label(self.master, text='Enter volatility (%):')
        lbl_volatility.grid(row=n_row, column=0, sticky='e')
        self.txt_volatility = Entry(self.master, width=10)
        self.txt_volatility.grid(row=n_row, column=1, sticky='w')

        n_row += 1
        lbl_riskfreerate = Label(self.master, text='Enter risk free rate (%):')
        lbl_riskfreerate.grid(row=n_row, column=0, sticky='e')
        self.txt_riskfreerate = Entry(self.master, width=10)
        self.txt_riskfreerate.grid(row=n_row, column=1, sticky='w')

        n_row += 1
        lbl_yield = Label(self.master, text='Enter divident/foreign yield:')
        lbl_yield.grid(row=n_row, column=0, sticky='e')
        self.txt_yield = Entry(self.master, width=10)
        self.txt_yield.grid(row=n_row, column=1, sticky='w')

        n_row += 1
        lbl_optiontype = Label(self.master, text='Select option type:')
        lbl_optiontype.grid(row=n_row, column=0, sticky='e')
        self.cmb_eu_am = Combobox(self.master, width=15, state='readonly')
        self.cmb_eu_am.grid(row=n_row, column=1, sticky='w')
        self.cmb_eu_am['values'] = ('European', 'American')
        self.cmb_eu_am.current(0)
        self.cmb_put_call = Combobox(self.master, width=15, state='readonly')
        self.cmb_put_call.grid(row=n_row, column=2, sticky='w')
        self.cmb_put_call['values'] = ('Put', 'Call')
        self.cmb_put_call.current(0)

        n_row += 1
        lbl_life = Label(self.master, text='Enter option life in years:')
        lbl_life.grid(row=n_row, column=0, sticky='e')
        self.txt_life = Entry(self.master, width=10)
        self.txt_life.grid(row=n_row, column=1, sticky='w')

        lbl_max_price = Label(self.master, text='Enter max price:')
        lbl_max_price.grid(row=n_row, column=2, sticky='e')
        self.txt_max_price = Entry(self.master, width=10)
        self.txt_max_price.grid(row=n_row, column=3, sticky='w')

        n_row += 1
        lbl_strike = Label(self.master, text='Enter strike price:')
        lbl_strike.grid(row=n_row, column=0, sticky='e')
        self.txt_strike = Entry(self.master, width=10)
        self.txt_strike.grid(row=n_row, column=1, sticky='w')

        lbl_size_price = Label(self.master, text='Enter grid size for price:')
        lbl_size_price.grid(row=n_row, column=2, sticky='e')
        self.txt_size_price = Entry(self.master, width=10)
        self.txt_size_price.grid(row=n_row, column=3, sticky='w')

        n_row += 1
        lbl_steps = Label(self.master, text='Enter tree steps:')
        lbl_steps.grid(row=n_row, column=0, sticky='e')
        self.txt_steps = Entry(self.master, width=10)
        self.txt_steps.grid(row=n_row, column=1, sticky='w')

        lbl_size_time = Label(self.master, text='Enter grid size for time:')
        lbl_size_time.grid(row=n_row, column=2, sticky='e')
        self.txt_size_time = Entry(self.master, width=10)
        self.txt_size_time.grid(row=n_row, column=3, sticky='w')

        # Results
        n_row += 1
        lbl_results = Label(self.master, text='Results:', font=('Arial Bold', 12))
        lbl_results.grid(row=n_row, column=0, columnspan=4, pady=(5,0))

        btn_calculate = Button(self.master, text='Calculate', font=('Arial Bold', 10), command=self.calculate)
        btn_calculate.grid(row=n_row, column=3, sticky='we', pady=(5,0), padx=(0, 2))

        btn_quit = Button(self.master, text='Exit', command=sys.exit, font=('Arial Bold', 10))
        btn_quit.grid(row=n_row, column=4, sticky='we', pady=(5,0))

        n_row += 1
        self.txt_result = scrolledtext.ScrolledText(self.master, height=14, width=40, wrap=NONE)
        self.txt_result.grid(row=n_row, column=0, columnspan=6, sticky='news')

        self.check_divs(None)

    @staticmethod
    def disable_combo(elem, index):
        elem.current(0)
        elem.config(state=DISABLED)

    @staticmethod
    def enable_combo(elem):
        elem.config(state='normal')

    @staticmethod
    def disable_entry(elem):
        elem.delete(0, END)
        elem.config(state=DISABLED)

    @staticmethod
    def enable_entry(elem):
        elem.delete(0, END)
        elem.config(state='normal')

    def check_divs(self, event):
        if self.cmb_method.get() == 'Explicit Difference' or self.cmb_method.get() == 'Implicit Difference' or self.cmb_method.get() == 'Monte Carlo':
            self.disable_entry(self.txt_steps)
            self.disable_combo(self.cmb_underlier, 0)
            self.disable_combo(self.cmb_eu_am, 0)
            self.disable_entry(self.txt_yield)
            self.disable_divs()

        if self.cmb_method.get() == 'Explicit Difference' or self.cmb_method.get() == 'Implicit Difference':
            self.enable_entry(self.txt_max_price)
            self.enable_entry(self.txt_size_price)
            self.enable_entry(self.txt_size_time)
        else:
            self.disable_entry(self.txt_max_price)
            self.disable_entry(self.txt_size_price)
            self.disable_entry(self.txt_size_time)

        if self.cmb_method.get() == 'Binomial':
            self.enable_entry(self.txt_steps)
            self.enable_combo(self.cmb_underlier)
            self.enable_combo(self.cmb_eu_am)
            if self.cmb_underlier.get() != 'Equity':
                self.disable_divs()

            if self.cmb_underlier.get() == 'Equity':
                self.disable_entry(self.txt_yield)
                self.enable_divs()

            if self.cmb_underlier.get() == 'Currency' or self.cmb_underlier.get() == 'Index':
                self.enable_entry(self.txt_yield)

            if self.cmb_underlier.get() == 'Futures':
                self.disable_entry(self.txt_yield)

    def disable_divs(self):
        for i in range(3):
            self.disable_entry(self.dt[i])
            self.disable_entry(self.dv[i])

    def enable_divs(self):
        for i in range(3):
            self.enable_entry(self.dt[i])
            self.enable_entry(self.dv[i])

    @staticmethod
    def client_exit():
        exit()

    @staticmethod
    def is_int(x):
        try:
            int(x)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(x):
        try:
            float(x)
            return True
        except ValueError:
            return False

    def calculate(self):
        self.txt_result.delete('1.0', END)
        if not self.is_entered_data_valid():
            return

        if self.cmb_method.get() == 'Binomial':
            self.calculate_binomial()

        if self.cmb_method.get() == 'Implicit Difference':
            self.calculate_implicit()

        if self.cmb_method.get() == 'Explicit Difference':
            self.calculate_explicit()

        if self.cmb_method.get() == 'Monte Carlo':
            self.do_monte_carlo()

    def do_monte_carlo(self):
        mc = CSimulation()

        mc.s = float(self.txt_current_price.get())
        mc.sigma = float(self.txt_volatility.get()) * 0.01
        mc.r = float(self.txt_riskfreerate.get()) * 0.01
        mc.k = float(self.txt_strike.get())
        mc.t = float(self.txt_life.get())
        mc.is_call = mc.option_type_b[self.cmb_put_call.get()]

        mc.run()
        mc.process_results()
        self.txt_result.insert(INSERT, 'Option price mean: {}\n'.format(mc.pf_mean))
        self.txt_result.insert(INSERT, ' Option price std: {}\n\n'.format(mc.pf_std))
        self.txt_result.insert(INSERT, '       Gamma mean: {}\n'.format(mc.gm_mean))
        self.txt_result.insert(INSERT, '        Gamma std: {}\n'.format(mc.gm_std))

    def calculate_implicit(self):
        is_call = self.option_type_b[self.cmb_put_call.get()]
        s0 = float(self.txt_current_price.get())
        sigma = float(self.txt_volatility.get()) * 0.01
        r = float(self.txt_riskfreerate.get()) * 0.01
        k = float(self.txt_strike.get())
        t = float(self.txt_life.get())

        smax = float(self.txt_max_price.get())
        m = int(self.txt_size_price.get())
        n = int(self.txt_size_time.get())
        #option = EuImplicit(50, 50, 0.1, 5. / 12., 0.4, 100, 100, 1000, False)
        option = EuImplicit(s0, k, r, t, sigma, smax, m, n, is_call)
        self.txt_result.insert(INSERT, "Option price: {}".format(option.price()))

    def calculate_explicit(self):
        is_call = self.option_type_b[self.cmb_put_call.get()]
        s0 = float(self.txt_current_price.get())
        sigma = float(self.txt_volatility.get()) * 0.01
        r = float(self.txt_riskfreerate.get()) * 0.01
        k = float(self.txt_strike.get())
        t = float(self.txt_life.get())

        smax = float(self.txt_max_price.get())
        m = int(self.txt_size_price.get())
        n = int(self.txt_size_time.get())
        #option = EuExplicit(50, 50, 0.1, 5. / 12., 0.4, 100, 100, 1000, False)
        option = EuExplicit(s0, k, r, t, sigma, smax, m, n, is_call)
        self.txt_result.insert(INSERT, "Option price: {}".format(option.price()))

    def calculate_binomial(self):
        self.txt_result.delete('1.0', END)

        ch = CHandler()

        ch.underlying_type = ch.underlier_types[self.cmb_underlier.get()]
        ch.is_american = ch.option_type_a[self.cmb_eu_am.get()]
        ch.is_call = ch.option_type_b[self.cmb_put_call.get()]

        ch.s = float(self.txt_current_price.get())
        ch.sigma = float(self.txt_volatility.get())
        ch.r = float(self.txt_riskfreerate.get())

        ch.q = 0
        if self.txt_yield.get():
            ch.q = float(self.txt_yield.get())

        ch.x = float(self.txt_strike.get())
        ch.n_steps = int(self.txt_steps.get())
        ch.t = float(self.txt_life.get())

        if self.cmb_underlier.get() == 'Equity':
            if len(''.join([dv.get() for dv in self.dv])) > 0:
                for i in range(3):
                    if self.dt[i].get() and self.dv[i].get():
                        ch.div_list.tt[i] = float(self.dt[i].get())
                        ch.div_list.vv[i] = float(self.dv[i].get())

        if not ch.handler() and len(ch.errors) > 0:
            self.txt_result.insert(INSERT, 'Please resolve following validation errors:\n\n  ')
            self.txt_result.insert(INSERT, '\n  '.join(ch.errors))
            return

        self.txt_result.insert(INSERT, ch.print_tree() + '\n')
        self.txt_result.insert(INSERT, 'Price: {}\n'.format(ch.price))
        self.txt_result.insert(INSERT, 'Delta: {}\n'.format(ch.delta))
        self.txt_result.insert(INSERT, 'Gamma: {}\n'.format(ch.gamma))
        self.txt_result.insert(INSERT, 'Theta: {}\n'.format(ch.theta))
        self.txt_result.insert(INSERT, '  Rho: {}\n'.format(ch.rho))

    def is_entered_data_valid(self):
        errors = []

        if self.cmb_underlier.get() == 'Equity':
            for i in range(3):
                if self.dt[i].get() or self.dv[i].get():
                    if not (self.is_float(self.dt[i].get()) and self.is_float(self.dv[i].get())):
                        errors.append('All entered time/divident values have to be numbers.')
                        break

        if not self.is_float(self.txt_current_price.get()):
            errors.append('Current price value has to be a not empty number value')

        if not self.is_float(self.txt_volatility.get()):
            errors.append('Volatility value has to be a not empty number value')

        if not self.is_float(self.txt_riskfreerate.get()):
            errors.append('Risk free rate value has to be a not empty number value')

        if (self.cmb_underlier.get() == 'Currency' or self.cmb_underlier.get() == 'Index') and not self.is_float(self.txt_yield.get()):
            errors.append('Yield value has to be a not empty number value')

        if not self.is_float(self.txt_life.get()):
            errors.append('Life value has to be a not empty number value')

        if not self.is_float(self.txt_strike.get()):
            errors.append('Strike price value has to be a not empty number value')

        if self.cmb_method.get() == 'Binomial' and not self.is_int(self.txt_steps.get()):
            errors.append('Tree steps value has to be a not empty number value')

        if self.cmb_method.get() == 'Explicit Difference' or self.cmb_method.get() == 'Implicit Difference':
            if not self.is_float(self.txt_max_price.get()):
                errors.append('Finite difference requires Max Price value to be a not empty number value')

            if not self.is_float(self.txt_size_price.get()):
                errors.append('Finite difference requires Price Grid Size value to be a not empty number value')

            if not self.is_float(self.txt_size_price.get()):
                errors.append('Finite difference requires Time Grid Size value to be a not empty number value')

        if len(errors) > 0:
            self.txt_result.insert(INSERT, 'Please resolve following validation errors:\n\n  ')
            self.txt_result.insert(INSERT, '\n  '.join(errors))
            return False

        return True


main_window = Tk()
app = Window(main_window, 13, 6)

main_window.mainloop()
