# -*- coding: utf-8 -*-
import os
import sys

def type_1_line(year,month,day, hour, minute,lat,lon,dep,m1,m2):
	if len(month)<2:
		month = ' '+month
	if len(day)<2:
		day = ' '+day
	if len(hour)<2:
		hour = ' '+hour
	if len(minute)<2:
		minute = ' '+minute
	lat = str(round(float(lat),3))
	if len(lat.split('.')[1]) == 1:
		lat +='00'
	elif len(lat.split('.')[1]) == 2:
		lat += '0'
	if len(lat.split('.')[0]) == 1:
		lat = '  '+lat
	elif len(lat.split('.')[0]) == 2:
		lat = ' '+lat
	lon = str(round(float(lon),3))
	if len(lon.split('.')[1]) == 1:
                lon +='00'
        elif len(lon.split('.')[1]) == 2:
                lon += '0'
        if len(lon.split('.')[0]) == 1:
                lat = '   '+lat
        elif len(lon.split('.')[0]) == 2:
                lon = '  '+lon
	elif len(lon.split('.')[0]) == 3:
		lon = ' '+lon
	dep = str(round(float(dep),1))
        if len(dep.split('.')[0]) == 1:
                dep = '  '+dep
        elif len(dep.split('.')[0]) == 2:
                dep = ' '+dep 
	line = ' '+year+' '+month+day+' '+hour+minute+' 00.0 L '+lat+lon+dep+'  RSN  3 0.1 '+m1+'LRSN '+m2+'WRSN        1\n' 	
	return line

def sfile_builder(date,hour,lat,lon,dep, M, source):
	year, month, day = date.split('-')[0], date.split('-')[1], date.split('-')[2]
	Hour, minute, second = hour.split(':')[0], hour.split(':')[1], hour.split(':')[2] 
	sfile_name = day+'-'+Hour+minute+'-'+second+source+'.S'+year+month
	S = open(sfile_name, 'w')
	line1 = type_1_line(year, month, day, Hour, minute, lat, lon, dep, M, M)
	S.write(line1)
	S.write(' GAP=135        0.80       2.6     3.6  4.8 -0.1622E+01  0.5295E+01 -0.1830E+00E\n')
    	S.write(' ACTION:REG 15-11-17 19:58 OP:xxx  STATUS:               ID:'+year+month+day+Hour+minute+second+'     I\n')
	S.write(' 2016-05-19-1921-58M.COL___284                                                 6\n')
    	S.write(' STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO AIN AR TRES W  DIS CAZ7\n')
	S.write(' STA1 EZ EP       1214 15.24                             110   -0.0210 29.7 251\n')
	S.write(' STA1 EZ ES       1214 19.3                              110   -0.1010 29.7 251\n')
	S.write(' STA2 EZ EP       1214 15.24                             110   -0.0210 29.7 251\n')
	S.write(' STA2 EZ ES       1214 19.3                              110   -0.1010 29.7 251\n')
	S.write(' STA3 EZ EP       1214 15.24                             110   -0.0210 29.7 251\n')
	S.write(' STA3 EZ ES       1214 19.3                              110   -0.1010 29.7 251\n')
	S.close()
	return S.name
