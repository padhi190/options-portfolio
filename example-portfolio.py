from option.option import Option, OptionPortfolio
import datetime as dt
import matplotlib.pyplot as plt

eval_date = dt.date(2021,8,1)
expiry = dt.date(2021,9,2)

c103ibm = Option("IBM",105.0, 103, expiry, eval_date, 0.05, 0.20, "Call", 10)
c107ibm = Option("IBM",105.0, 107, expiry, eval_date, 0.05, 0.20, "Call", -20)
c110ibm = Option("IBM",105.0, 110, expiry, eval_date, 0.05, 0.20, "Call", 10)

c103ibm.opt_price = c103ibm.price()
c103ibm.opt_summary()


c107ibm.opt_price = c107ibm.price()
c107ibm.opt_summary()

c110ibm.opt_price = c110ibm.price()

plt.show()
port = OptionPortfolio([c103ibm])
port.add(c107ibm)
port.add(c110ibm)

port.port_summary()
port.draw_payoff_diagram(95, 113, eval_date, 105)
eval_date += dt.timedelta(days=20)
port.draw_payoff_diagram(95, 113, eval_date, 105)
eval_date += dt.timedelta(days=16)
port.draw_payoff_diagram(95, 113, eval_date, 105)

plt.show()