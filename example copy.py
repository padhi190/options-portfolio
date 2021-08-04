from option.Option import Option, OptionPortfolio
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

eval_date = dt.date(2021,8,1)
expiry = dt.date(2021,9,2)

c100ibm = Option("IBM",105.0, 100, expiry, eval_date, 0.05, 0.20, "Put", 100)
p110ibm = Option("IBM",105.0, 107, expiry, eval_date, 0.05, 0.20, "Put", -100)

c100ibm.opt_price = c100ibm.price()
c100ibm.opt_summary()


p110ibm.opt_price = p110ibm.price()
p110ibm.opt_summary()

plt.show()
port = OptionPortfolio([c100ibm])
port.add(p110ibm)
port.add(p110ibm)
port.remove(p110ibm)

port.port_summary()
port.draw_payoff_diagram(95, 110, eval_date, 105)
eval_date += dt.timedelta(days=20)
port.draw_payoff_diagram(95, 110, eval_date, 105)
eval_date += dt.timedelta(days=30)
port.draw_payoff_diagram(95, 110, eval_date, 105)

plt.show()