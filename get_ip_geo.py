import pandas as pd, numpy as np
from data_processing import split_wrd

_ipdata = pd.read_csv('/home/ericx/Eric/datasets/ipdatabase/data/ipdata.csv')
_ipgeo = pd.read_csv('/home/ericx/Eric/datasets/ipdatabase/data/ipgeo.csv')
M = len(_ipdata)

def get_geo_from_ip(ip):
    ip = split_wrd(ip,'*','0')
    ip = '.'.join([i.zfill(3) for i in ip.split('.')])
    #returns = _ipdata[_ipdata['startip']<=ip]
    #returns = returns[returns['endip']>=ip]['geo']

    c = M//2
    tn = M//2
    while 1:
        if c<2: c=2
        t = _ipdata.ix[tn,:]
        if t['startip'] <= ip:
            if t['endip'] >= ip: break
            else: c//=2; tn+=c
        else: c//=2; tn-=c
    returns = t['geo']
    #if len(returns)!=1: raise Warning('ip %s not in database'%ip)
    return returns#.values[0]


def get_place_from_geo(geo,place=['prov','city']):
    return _ipgeo[_ipgeo['geo']==geo][place].values


def get_place_from_ip(ip,place=['prov','city']):
    return get_place_from_geo(get_geo_from_ip(ip),place)
