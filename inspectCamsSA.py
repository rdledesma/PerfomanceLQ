#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 13:54:25 2024

@author: dario
"""
import pandas as pd
import Metrics as m
import Geo
from datetime import timedelta
for i in [1,5,10, 15,30,60]:
    d = pd.read_csv(f'measured/SA/sa_{i}.csv')
    c = pd.read_csv(f'cams/SA/sa_{i}.csv', usecols=['date','TOA','GHI','Clear sky GHI'])

    c['date'] = pd.to_datetime(c.date)
    d['date'] = pd.to_datetime(d.date)
    c = c[c.date.dt.year>2020]


    

    c['ghi'] = d.ghi.values
    
    
    
    
    g = Geo.Geo(
              range_dates= d.date + timedelta(minutes = i/2), 
              lat=-24.7288, 
              long=-65.4095, 
              gmt=0, 
              beta=0,
              alt=1233).df

    c['sza'] = g.SZA.values
    c['mak'] = g.Mak.values
    c['alpha'] = g.alphaS.values
    c['argp2'] = g.GHIargp2.values
    c['ghicc'] = c['Clear sky GHI']
    c['ktmod'] = c['GHI'] / c['TOA']
    c['kcmod'] = c['GHI'] / c['ghicc']
    c['kcmodargp'] = c['GHI'] / c['argp2']
    c = c.drop(['Clear sky GHI','TOA'], axis=1)
    
    
    
    
    
    
    
    c.to_csv(f'process/SA/{i}.csv', index=False)
    
    s = c.dropna()

    pred = s.GHI.values
    true = s.ghi.values

    print(m.rrmsd(true, pred))

