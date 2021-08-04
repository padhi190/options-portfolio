from option.Option import Option, OptionPortfolio
import datetime as dt
import matplotlib.pyplot as plt

eval_date = dt.date(2021,8,1)
expiry = dt.date(2021,9,2)

c100ibm = Option("IBM",105.0, 103, expiry, eval_date, 0.05, 0.20, "Call", 10)
p110ibm = Option("IBM",105.0, 107, expiry, eval_date, 0.05, 0.20, "Call", -10)

c100ibm.opt_price = c100ibm.price()
c100ibm.opt_summary()
c100ibm.drawpayoff_diagram(95, 115)

c100ibm.t = eval_date + dt.timedelta(days=14)
c100ibm.opt_summary()
c100ibm.drawpayoff_diagram(95,115)

c100ibm.t = eval_date + dt.timedelta(days=30)
c100ibm.opt_summary()
c100ibm.drawpayoff_diagram(95,115)

plt.show()
# p110ibm.opt_summary()
# p110ibm.drawpayoff_diagram()
# port = OptionPortfolio([c100ibm])
# port.add(p110ibm)
# port.add(p110ibm)
# port.remove(p110ibm)

# port.port_summary()
