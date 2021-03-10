import numpy as np
import matplotlib.mlab as ml
import matplotlib.pyplot as pp
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import AxesGrid
from scipy.interpolate import Rbf
from pylab import imread, imshow
from ordered_set import OrderedSet
import matplotlib
import statistics

layout = imread('/Users/tagore_pothuneedi/Desktop/map.png')
a={}
##station location measured from floormap
sta_loc={"sta1":(83,1239),"sta2":(1174,1237),"sta3":(1936,1258),"sta4":(356,954),"sta5":(578,855),"sta6":(1448,970),"sta7":(154,519),"sta8":(1653,495),"sta9":(107,197),"sta10":(1004,183),"sta11":(1955,212)}

image_width= len(layout[0])
image_height= len(layout) - 1

num_x = int(image_width / 4)
num_y = int(num_x / (image_width / image_height))

x = np.linspace(0,image_width, num_x)
y = np.linspace(0,image_height, num_y)

gx, gy = np.meshgrid(x, y)
gx, gy = gx.flatten(), gy.flatten()

interpolate = True

##Data grouping from different logs of stations
data={}
for num in range(1,12):
    file=open('/Users/tagore_pothuneedi/testv1/test_logs/192.168.0.186_sta{}_2020-06-22_1592870286.log'.format(num),'r')
    op=file.read()
    op=op.strip()
    op=op.split('\n')
    ## station mac:op[0][8:25]
    ## signal level: op[1][11:17]
    i=0
    a={}
    for item in op:
        if i%3==0:
            key=item[8:25]
            a[key]=op[i+1][11:14]
            i+=1
        else:
            i+=1
            continue
    data['sta{}'.format(num)]=a
#data

## MAC addr of stations detected in the mesh
sta_dec= OrderedSet()
for station in data:
    for values in data[station].keys():
        sta_dec.add(values)
#sta_dec

## signal from different station at location
a={}
for i,j in zip(sta_loc.values(),data.values()):
     a[i]=j
locx=[]
locy=[]
for value in sta_loc.values():
    locx.append(value[0])
    locy.append(value[1])
def plot():
    # Mean for each dectected station rssi
    res=[]
    for station in sta_dec:
        temp=[]
        for loc in a.keys():
            try:
                temp.append(int(a[loc][station]))
            except:
                temp.append(0)
                continue
        #print(temp)
        res.append(statistics.mean(temp))
    #rssi_mac
    pp.title("RSSI Heat Map")

    if interpolate:
        # Interpolate the data
        rbf = Rbf(locx, locy, res, function='linear')
        z = rbf(gx, gy)
        z = z.reshape((num_y, num_x))
        # Render the interpolated data to the plot
        # color mapping
        norm = matplotlib.colors.Normalize(vmin=min(res), vmax=max(res), clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap='RdYlBu_r')
        image = pp.imshow(z,extent=(0,image_width,image_height, 0),cmap='RdYlBu_r', alpha=0.5, zorder=100)

    pp.colorbar(image)
    pp.imshow(layout, interpolation='bicubic', zorder=1, alpha=1)
    pp.show()
    print(res,locx,locy)
if __name__=="__main__":
    plot()