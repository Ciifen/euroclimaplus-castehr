from dateutil.relativedelta import relativedelta
import numpy as np
def create_datelist(start_date, n_months):
    print(type(start_date))
    dates = [start_date + relativedelta(months=i)
             for i in range(0, n_months)]

    return np.array(dates)