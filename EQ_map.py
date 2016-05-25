from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import os, stat

def EQ_map(lon,lat,M,source, region, ID):
	llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat = -84, -7, -64, 15 
	if  (llcrnrlon < float(lon) < urcrnrlon) and (llcrnrlat < float(lat) < urcrnrlat):
		map = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat, projection='cyl', resolution=None)
		x, y = map(float(lon), float(lat))
		map.scatter(x, y, 500, color="yellow", marker="*", edgecolor="k", zorder=3)
		map.arcgisimage(service='NatGeo_World_Map', xpixels = 1500, verbose= True)
		plt.title('M:'+M+','+region+', Fuente:'+source, fontsize='20')
		name = ID+'.jpg'
		if os.path.exists(name) == False:
			plt.savefig(name)
    			os.chmod(sfile_name,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
		else:
			pass
	else:
		map = Basemap(projection='ortho', lat_0=float(lat), lon_0=float(lon), resolution='l')
		map.drawmapboundary(fill_color=(0.478,0.859,0.988))
		map.fillcontinents(color=(0.235,0.705,0.427), lake_color=(0.478,0.859,0.988))
		map.drawparallels(np.arange(-90.,120.,30.))
		map.drawmeridians(np.arange(0.,420.,60.))
		x, y = map(float(lon), float(lat))
		map.scatter(x, y, 800, color="yellow", marker="*", edgecolor="k", zorder=3)
		plt.title('M:'+M+','+region+', Fuente:'+source, fontsize='20')
		name = ID+'.jpg'
		if os.path.exists(name) == False:
			plt.savefig(name)
    			os.chmod(name,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
		else:
			pass
	return name
#EQ_map('-78.7','-2.73','5','USGS', 'Ecuador', 'prueba1')
#figura = EQ_map(50,50,'5','GFZ', 'Banda Sea', 'prueba2')	
#print figura
