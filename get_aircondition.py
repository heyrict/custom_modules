import pandas as pd, numpy as np
import os
from dateutil import parser
from multiprocessing.dummy import Pool

_spotlist = pd.read_csv('~/Eric/datasets/air_condition/spot_list_new.csv')
_datelist = [i.split('_')[-1].split('.')[0] for i in os.listdir('/home/ericx/Eric/datasets/air_condition/data')]

def _get_city_no(city_name):
    '''
    get all spot number in one city
    '''
    return list(_spotlist[_spotlist['城市']==city_name]['监测点编码'])

def get_city_pollution(city_name,date=None,month=None,year=None\
                    ,pollution='AQI',func='mean'):
    '''
    get average pollution in city_name on date/month/year
    
    Parameters
    ----------
    city_name : str
    date : scarlar indicating one date or a list of them
    month : scarlar indicating one date or a list of them
    year : scarlar indicating one year or a list of them
    pollution : str
        one of ['AQI','PM2.5','PM2.5_24h','PM10','PM10_24h','SO2','SO2_24h','NO2','NO2_24h',
                'O3','O3_24h','O3_8h','O3_8h_24h','CO','CO_24h']
    func : str or function
        - 'mean' : calculate mean of all pollution data
        - 'sum' : calculate sum of all pollution data
    '''
    if not (((type(date)!=type(None)) ^ (type(month)!=type(None))) ^ (type(year)!=type(None))):
        raise ValueError('make sure exactly one of date, month, year is passed')

    if date:

        if type(date) == list:
            pool = Pool(3)
            returns = pool.map(lambda i: get_city_pollution(city_name,date=i,pollution=pollution,func=func),date)
            pool.close()
            return returns

        if type(pollution)==list:
            pool = Pool(3)
            returns = pool.map(lambda i: get_city_pollution(city_name,date=date,pollution=i,func=func),pollution)
            pool.close()
            return returns

        city_list = _get_city_no(city_name)
        if not city_list:
            raise Warning('city %s not in spot list'%city_name)
       
        date = parser.parse(str(date))
        curdaypoll = pd.read_csv('/home/ericx/Eric/datasets/air_condition/data/china_sites_%s.csv'%date.strftime('%Y%m%d'))

        curdaypoll = curdaypoll[curdaypoll['type']==pollution]

        if type(func)==str and func == 'mean':
            return curdaypoll[city_list].bfill().values.mean()
        elif type(func)==str and func == 'sum':
            return curdaypoll[city_list].bfill().values.sum()
        else:
            return curdaypoll[city_list].bfill().values.flatten().map(func)

    if month:

        if type(month) == list:
            pool = Pool(3)
            returns = pool.map(lambda i: get_city_pollution(city_name,month=i,pollution=pollution,func=func),month)
            pool.close()
            return returns

        month = parser.parse(str(month))
        monthlist = [i for i in _datelist if month.strftime('%Y%m') == i[:6]]

        return pd.Series(get_city_pollution(city_name,date=monthlist,pollution=pollution,func=func)).mean()

    if year:

        if type(year) == list:
            pool = Pool(3)
            returns = pool.map(lambda i: get_city_pollution(city_name,year=i,pollution=pollution,func=func),year)
            pool.close()
            return returns

        year = parser.parse(str(year))
        yearlist = [i for i in _datelist if year.strftime('%Y') == i[:4]]

        return pd.Series(get_city_pollution(city_name,date=yearlist,pollution=pollution,func=func)).mean()
