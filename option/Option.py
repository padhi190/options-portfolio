from dataclasses import dataclass
import datetime as dt
import numpy as np
import scipy.stats as si
import matplotlib.pyplot as plt

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

@dataclass
class Option:
    symbol: str #underlying symbol
    S: float #underlying price
    K: float #strike price
    T: dt #expiry date
    t: dt #evaluation date
    r: float #risk free rate
    sigma: float #volatility (forecasted)
    type: str #Call/Put
    pos: int = 1 #no of position, use negative number to represent short
    opt_price: float = 1. #actual option price

    def time_to_expiry(self):
        tte = self.T - self.t
        return max(tte.days,0)
    
    def Tt(self):
        return self.time_to_expiry()/360.0

    def __str__(self) -> str:
        pos = "Long" if self.pos > 0 else "Short"
        return f"{pos} {abs(self.pos)} {self.symbol} {self.K} {self.type} {self.T:%b %d, %Y} @{self.opt_price}"

    def __d1(self):
        result = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.Tt()) / (self.sigma * np.sqrt(self.Tt()))
        return result

    def __d2(self):
        result = self.__d1() - self.sigma * np.sqrt(self.Tt())
        return result

    def price(self):
        if self.time_to_expiry() > 0:
            call = (self.S * si.norm.cdf(self.__d1(), 0.0, 1.0) - self.K * np.exp(-self.r * self.Tt()) * si.norm.cdf(self.__d2(), 0.0, 1.0))
            put = (self.K * np.exp(-self.r * self.Tt()) * si.norm.cdf(-1*self.__d2(), 0.0, 1.0) - self.S * si.norm.cdf(-1*self.__d1(), 0.0, 1.0))
        else:
            call = max(self.S - self.K, 0)
            put = max(self.K - self.S, 0)
        return call if self.type == "Call" else put

    def delta(self):
        if self.time_to_expiry() > 0:
            call_delta = si.norm.cdf(self.__d1(), 0.0, 1.0)
            put_delta = call_delta - 1.0
        else:
            call_delta = 1.0 if self.S > self.K else 0.0
            put_delta = call_delta - 1.0
        return call_delta if self.type == "Call" else put_delta

    def gamma(self):
        if self.time_to_expiry() > 0:
            result = si.norm.pdf(self.__d1()) / (self.S * self.sigma * np.sqrt(self.Tt()))
        else:
            result = 0
        return result

    def theta(self):
        if self.time_to_expiry() > 0:
            t1 = (self.S * si.norm.pdf(self.__d1()) * self.sigma) / (2 * np.sqrt(self.Tt()))
            t2 = self.r * self.K * np.exp(-self.r * self.Tt())
            if self.type == "Call":
                return (-1 * (t1 + t2 * si.norm.cdf(self.__d2())))/360.
            else:
                return (-t1 + t2 * si.norm.cdf(self.__d2() * -1))/360.
        else:
            return 0

    def vega(self):
        if self.time_to_expiry() > 0:
            return self.sigma * si.norm.cdf(self.__d1()) * np.sqrt(self.Tt())
        else:
            return 0

    def opt_summary(self):
        price = round(self.price(),3)
        delta = round(self.delta(),3)
        gamma = round(self.gamma(),3)
        theta = round(self.theta(),6)
        vega = round(self.vega(),6)
        stock_mult = 100
        Tt = round(self.Tt(),3)
        line_mult=37
        print("-"*line_mult)
        print(self)
        print(f"Underlying: {self.S}")
        print(f"Time to expiry: {self.time_to_expiry()} days  ({Tt} years)")
        print(f"Theo. Price: {price} ({round(price * self.pos * stock_mult,3)} Total)")
        print(f"Delta: {delta} ({round(delta * self.pos * stock_mult,3)} Total)")
        print(f"Gamma: {gamma} ({round(gamma * self.pos * stock_mult,3)} Total)")
        print(f"Vega: {vega} ({round(vega * self.pos * stock_mult,3)} Total)")
        print(f"Theta: {theta} ({round(theta * self.pos * stock_mult,3)} Total)")
        print("-"*line_mult)
        print("")

    def payoff_data(self, lower_bound, upper_bound):
        x = np.linspace(lower_bound, upper_bound, 100)
        y = np.zeros(100)
        cur_price = self.S
        for i, j in enumerate(x):
            self.S = j
            y[i] = (self.price() - self.opt_price) * self.pos * 100
        self.S = cur_price
        return x, y

    def drawpayoff_diagram(self, lower_bound, upper_bound):
        x, y = self.payoff_data(lower_bound, upper_bound)
        plt.plot(x,y)
        dot_x = self.S
        dot_y = (self.price() - self.opt_price) * self.pos * 100
        plt.scatter(dot_x, dot_y, c='red')
        plt.annotate(f"  {round(dot_y, 3)}", (dot_x, dot_y))
        # plt.show()

@dataclass
class OptionPortfolio:
    portfolio: list[Option]

    def __str__(self) -> str:
        result = list(map(lambda x: print(x), self.portfolio))
        return (str(result))

    def add(self, addport):
        self.portfolio.append(addport)
    
    def remove(self, remport):
        self.portfolio.remove(remport)

    def port_delta(self):
        delta = 0.
        stock_mult = 100
        for d in self.portfolio:
            delta += d.delta() * d.pos * stock_mult
        return delta
    
    def port_gamma(self):
        gamma = 0.
        stock_mult = 100
        for d in self.portfolio:
            gamma += d.gamma() * d.pos * stock_mult
        return gamma

    def port_vega(self):
        vega = 0.
        stock_mult = 100
        for d in self.portfolio:
            vega += d.vega() * d.pos * stock_mult
        return vega
    
    def port_theta(self):
        theta = 0.
        stock_mult = 100
        for d in self.portfolio:
            theta += d.theta() * d.pos * stock_mult
        return theta

    def port_summary(self):
        port_delta = round(self.port_delta(),3)
        port_gamma = round(self.port_gamma(),3)
        port_vega = round(self.port_vega(),6)
        port_theta = round(self.port_theta(),6)
        line_mult = 37
        print("-"*line_mult)
        print("Portfolio Summary: ")
        print("-"*line_mult)
        for p in self.portfolio:
            print(p)
        print("-"*line_mult)
        print(f"Porfolio Delta: {port_delta}")
        print(f"Porfolio Gamma: {port_gamma}")
        print(f"Porfolio Vega: {port_vega}")
        print(f"Porfolio Theta: {port_theta}")
        print("")

    def payoff_data(self, lower_bound, upper_bound, eval_date):
        y_sum = np.zeros(100)
        for i in self.portfolio:
            i.t = eval_date
            x_sum, y = i.payoff_data(lower_bound, upper_bound)
            y_sum += y
    
        return x_sum, y_sum

    def draw_payoff_diagram(self, lower_bound, upper_bound, eval_date, U):
        x, y = self.payoff_data(lower_bound, upper_bound, eval_date)
        # dot_x = self.portfolio[0].S
        dot_x = find_nearest(x, U)
        y_index = np.where(x == dot_x)[0][0]
        dot_y = y[y_index]
        plt.scatter(dot_x, dot_y, c='red')
        plt.annotate(f"  {round(dot_y, 3)}", (dot_x, dot_y))
        plt.plot(x, y)
