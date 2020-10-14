#### get all climate index from packages
import pandas as pd
import numpy as np
import datetime as dt
from SPEI import spei
from SPEI import spi
from SPEI import plot_index as graf
from util import utils
#from climate_indices import indices as clin
### from spei


### load file with etp computed previously
M0001 = pd.read_csv("/home/darwin/Documentos/Desarrollo/PythonProyects/indicesequia/datasets/M0001_Mounthly_etp.csv")
#### compute the balance
M0001['Balance'] = M0001['rr']-M0001['ETP_PM(mm/mes)']
M0001['fecha'] = pd.to_datetime(M0001['fecha'],dayfirst=False,yearfirst=True)
print(M0001.head(2))
################################
### compute de SPI
#################################
print("############### SPI ##############")
spiob = spi.SPI()
### setting spi configurations
spiob.set_rolling_window_params(span=1,window_type=None,center=True)
spiob.set_distribution_params(dist_type='gam')
reainfall = M0001['rr'].to_numpy(dtype=np.float64)
res_SPI = spiob.calculate(reainfall,starting_month=1)
date_list = M0001['fecha'].to_numpy(dtype=dt.date)

graf.plot_index(date_list,res_SPI)

################################
### compute de SPEI
#################################
print("############### SPEI ##############")
## in this case we need set distribution
speiob = spei.SPEI()
speiob.set_rolling_window_params(span=1,window_type=None,center=True)
speiob.set_distribution_params(dist_type='exp')
balance = M0001['Balance'].to_numpy(dtype=np.float64)
res_spei =  speiob.calculate (balance,starting_month=1)
#print(res_spei)
graf.plot_index(date_list,res_spei,index_type="SPEI")

""" Computes SPI (Standardized Precipitation Index).
    :param values: 1-D numpy array of precipitation values, in any units,
        first value assumed to correspond to January of the initial year if
        the periodicity is monthly, or January 1st of the initial year if daily
    :param scale: number of time steps over which the values should be scaled
        before the index is computed
    :param distribution: distribution type to be used for the internal
        fitting/transform computation
    :param data_start_year: the initial year of the input precipitation dataset
    :param calibration_year_initial: initial year of the calibration period
    :param calibration_year_final: final year of the calibration period
    :param periodicity: the periodicity of the time series represented by the
        input data, valid/supported values are 'monthly' and 'daily'
        'monthly' indicates an array of monthly values, assumed to span full
         years, i.e. the first value corresponds to January of the initial year
         and any missing final months of the final year filled with NaN values,
         with size == # of years * 12
         'daily' indicates an array of full years of daily values with 366 days
         per year, as if each year were a leap year and any missing final months
         of the final year filled with NaN values, with array size == (# years * 366)
    :param fitting_params: optional dictionary of pre-computed distribution
        fitting parameters, if the distribution is gamma then this dict should
        contain two arrays, keyed as "alphas" and "betas", and if the
        distribution is Pearson then this dict should contain four arrays keyed
        as "probabilities_of_zero", "locs", "scales", and "skews"
    :return SPI values fitted to the gamma distribution at the specified time
        step scale, unitless
    :rtype: 1-D numpy.ndarray of floats of the same length as the input array
        of precipitation values
    """
#data_spi= clin.spi(toArray,12,)

