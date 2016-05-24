#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Program that makes a request of the latest earthquakes via ATOM (NEIC) and RSS (GeoFon)
v(1) 2016-04-26
author: Nelson David Pérez García , e-mailnperez@sgc.gov.co
"""
import urllib
import feedparser
from datetime import datetime
import os, stat, sys
from correo import correo
from sfile import sfile_builder
from EQ_map import EQ_map

def event_printer(file_, source, date, hour, lat, lon, dep, M, region):
	print >> file_, source+"\t"+date+"\t"+hour+"\t"+lat+"\t"+lon+"\t"+dep+"\t"+M+"\t"+region

def geofon_event_printer(file_, source, summary, title):
	print >> file_, source+"\t"+summary+"\t"+title

def neic_event_printer(file_, source, date, lat, lon, dep, title):
	print >> file_, source+"\t"+date+"\t"+lat+"\t"+lon+"\t"+dep+"\t"+title

#Parsing the url's
link_usgs = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.atom"
link_usgs2 = "http://earthquake.usgs.gov/"
link_gfz = "http://geofon.gfz-potsdam.de/eqinfo/list.php?fmt=rss"
link_gfz2 = "http://geofon.gfz-potsdam.de/eqinfo/list.php"
neic = feedparser.parse(link_usgs)
gfz = feedparser.parse(link_gfz)

#Creating  request file_
date = datetime.now()
file_name = "request_"+str(date.year)+str(date.month)+str(date.day)+str(date.hour)+str(date.minute)+str(date.second)+".txt"#Nombre del archivo generado
file_ = open(file_name, 'w+')
print >> file_, "#Agency Date Time Lat Lon Depth(km) Mag Region"
print >> file_, "======================================================="
os.chmod(file_.name,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO) #Dándole permisos a los archivos¿?

#GeoFon Data request
map_geofon=str(gfz.entries[0]['id'])+".jpg"
source = 'GFZ'
GFZ_ID=str(gfz.entries[0]['id'])
date, hour, lat, lon, dep = str(gfz.entries[0]['summary']).split()[0], str(gfz.entries[0]['summary']).split()[1], str(gfz.entries[0]['summary']).split()[2], str(gfz.entries[0]['summary']).split()[3], str(gfz.entries[0]['summary']).split()[4] 
M, region = str(gfz.entries[0]['title_detail']['value']).split(',')[0], str(gfz.entries[0]['title_detail']['value']).split(',')[1]
print '1.',source, date, hour, lat, lon, dep, M, region
event_printer(file_, source, date, hour, lat, lon, dep, M, region)
##GeoFon map
if not os.path.isfile(str(gfz.entries[0]['id'])+".jpg"):
    try:
        gfzmap = urllib.URLopener()
        map_geofon = GFZ_ID+".jpg"
        gfzmap.retrieve(gfz.entries[0]['links'][1]['href'],map_geofon)
        os.chmod(str(gfz.entries[0]['id'])+".jpg",stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    except:
        print "Mapa no disponible en GeoFon"
else:
	pass
#NEIC Data request
source2 = 'USGS'
USGS_ID = str(neic.entries[0]['id'].split(':')[3])
date2 = str(neic.entries[0]['summary'].split('</dd><dd>')[0].split('</dt><dd>')[1].split(' ')[0])
hour2 = str(neic.entries[0]['summary'].split('</dd><dd>')[0].split('</dt><dd>')[1].split(' ')[1])
lat2 = str(neic.entries[0]['where']['coordinates'][1])
lon2 = str(neic.entries[0]['where']['coordinates'][0])
dep2 = str(neic.entries[0]['summary'].split('Depth')[1].split('</dt><dd>')[1].split('km')[0])
M2 =  str(neic.entries[0]['title'].split('-')[0])
region2 =  str(neic.entries[0]['title'].split('-')[1])
print '2.',source2, date2, hour2, lat2, lon2, dep2, M2, region2
event_printer(file_, source2, date2, hour2, lat2, lon2, dep2, M2, region2)
##NEIC kml
if not os.path.isfile(str(neic.entries[0]['id'].split(':')[3])+'.kml'):
	try:
		neicmap = urllib.URLopener()
		neicmap.retrieve(neic.entries[0]['links'][1]['href'].split('.cap')[0]+'.kml', str(neic.entries[0]['id'].split(':')[3])+'.kml')
		os.chmod(str(neic.entries[0]['id'].split(':')[3])+'.kml', stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
	except:
		print "KML no disponible en USGS"
else: 
	pass
#Changing modes

file_.close()

o=raw_input('Digite 1 o 2 para enviar correos de alguna de las 2 fuentes, 0 para no hacer nada: \n')
print o

if o=='1':
    print '========GFZ======='
    map = EQ_map(lon,lat,M.split(' ')[1],source,region, GFZ_ID)
    correo(source,date,hour,lat,lon,dep,M.split(' ')[1],region,GFZ_ID,map, link_gfz2)
    sfile_name=sfile_builder(date,hour,lat,lon,dep,M.split(' ')[1],'G')
    os.chmod(sfile_name,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    print sfile_name
elif o=='2':
    print '=======USGS======='
    map = EQ_map(lon2,lat2,M.split(' ')[1],source2,region2, USGS_ID)
    correo(source2,date2,hour2,lat2,lon2,dep2,M2.split(' ')[1],region2,USGS_ID,map, link_usgs2)
    sfile_name=sfile_builder(date2,hour2,lat2,lon2,dep2,M2.split(' ')[1],'N')
    os.chmod(sfile_name,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    print sfile_name
else:
	sys.exit()	    
