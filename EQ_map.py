from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

def EQ_map(lon,lat,M,source, region, ID):
	llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat = -84, -5, -64, 15 
	if  (llcrnrlon < lon < urcrnrlon) and (llcrnrlat < lat < urcrnrlat):
		map = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat, projection='cyl', resolution=None)
		x, y = map(float(lon), float(lat))
		map.scatter(x, y, 500, color="yellow", marker="*", edgecolor="k", zorder=3)
		map.arcgisimage(service='NatGeo_World_Map', xpixels = 1500, verbose= True)
		plt.title('M:'+M+','+region+', Fuente:'+source, fontsize='20')
		name = ID+'.jpg'
		plt.savefig(name)
		#plt.show()
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
		plt.savefig(name)
		#plt.show()				
	return name
#EQ_map(-72,4,10,'NEIC')
#figura = EQ_map(50,50,'5','NEIC', 'Banda Sea', 'figura')	
#print figura
