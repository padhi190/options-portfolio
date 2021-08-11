from option.option import Option
import datetime as dt
import matplotlib.pyplot as plt

eval_date = dt.date(2021,8,1)
expiry = dt.date(2021,9,2)

c103ibm = Option("IBM",105.0, 103, expiry, eval_date, 0.05, 0.20, "Call", 10)

print(c103ibm)
c103ibm.opt_price = c103ibm.price()
c103ibm.drawpayoff_diagram(95, 115)
c103ibm.t = eval_date + dt.timedelta(days=14)
c103ibm.drawpayoff_diagram(95,115)

c103ibm.t = eval_date + dt.timedelta(days=30)
c103ibm.opt_summary()
c103ibm.drawpayoff_diagram(95,115)

plt.show()