
import numpy as np
import re
import subprocess
from collections import defaultdict
import json
import ast
cellNumberRe = re.compile(r"^Cell\s+(?P<cellnumber>.+)\s+-\s+Address:\s(?P<mac>.+)$")
regexps = [
    re.compile(r"^ESSID:\"(?P<essid>.*)\"$"),
    re.compile(r"^Protocol:(?P<protocol>.+)$"),
    re.compile(r"^Mode:(?P<mode>.+)$"),
    re.compile(r"^Frequency:(?P<frequency>[\d.]+) (?P<frequency_units>.+) \(Channel (?P<channel>\d+)\)$"),
    re.compile(r"^Encryption key:(?P<encryption>.+)$"),
    re.compile(r"^Quality=(?P<signal_quality>\d+)/(?P<signal_total>\d+)\s+Signal level=(?P<signal_level_dBm>.+) d.+$"),
    re.compile(r"^Signal level=(?P<signal_quality>\d+)/(?P<signal_total>\d+).*$"),
]

# Detect encryption type
wpaRe = re.compile(r"IE:\ WPA\ Version\ 1$")
wpa2Re = re.compile(r"IE:\ IEEE\ 802\.11i/WPA2\ Version\ 1$")


# Parses the response from the command "iwlist scan"
def parse(content):
    cells = []
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        cellNumber = cellNumberRe.search(line)
        if cellNumber is not None:
            cells.append(cellNumber.groupdict())
            continue
        wpa = wpaRe.search(line)
        if wpa is not None :
            cells[-1].update({'encryption':'wpa'})
        wpa2 = wpa2Re.search(line)
        if wpa2 is not None :
            cells[-1].update({'encryption':'wpa2'}) 
        for expression in regexps:
            result = expression.search(line)
            if result is not None:
                if 'encryption' in result.groupdict() :
                    if result.groupdict()['encryption'] == 'on' :
                        cells[-1].update({'encryption': 'wep'})
                    else :
                        cells[-1].update({'encryption': 'off'})
                else :
                    cells[-1].update(result.groupdict())
                continue
    return cells
if __name__=="__main__":
    content=open("/Users/tagore_pothuneedi/testv1/test_logs/192.168.0.184_sta4_2020-06-19_1592581152.log","r")
    #print(content.read())
    content1=parse(content.read())
    jsonret=json.dumps(content1)
    _data = json.loads(jsonret)

sta_loc=[(0,0),(40,0),(110,0),(15,15),(25,20),(55,15),(5,40),(60,40),(3,55),(35,55),(110,55)]
a = defaultdict(list)
i=0
#print(_data)
for (x,y) in sta_loc:
    _data[i]['x']=x
    _data[i]['y']=y
    i+=1
for row in _data:
    a['x'].append(row['x'])
    a['y'].append(row['y'])
    a['rssi'].append(row['signal_level_dBm'])
    #a['signal_quality'].append(row['signal_quality'])
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as pp
from scipy.interpolate import Rbf
from pylab import imread, imshow
#import matplotlib



# _image_width=610
# _image_height=395
_image_path='/Users/tagore_pothuneedi/Desktop/map.png'
_layout = imread(_image_path)
_image_width= len(_layout[0])
_image_height= len(_layout) - 1
for x, y in [
            (0, 0), (0, _image_height),
            (_image_width, 0), (_image_width, _image_height)
        ]:
            a['x'].append(x)
            a['y'].append(y)
            for k in a.keys():
                 if k in ['x', 'y']:
                     continue
                 #a[k] = [0 if x is None else x for x in a[k]]
                 a[k].append(min(a[k]))
num_x = int(_image_width / 4)
num_y = int(num_x / (_image_width / _image_height))

x = np.linspace(0,_image_width, num_x)

y = np.linspace(0,_image_height, num_y)

gx,gy = np.meshgrid(x, y)
gx,gy = gx.flatten(), gy.flatten()

def _plot(a,key,gx,gy,num_x,num_y):
    pp.rcParams['figure.figsize'] = (_image_width / 300,_image_height / 300)
    i=0
    for ele in a['x']:
        a['x'][i]=int(ele)
        i+=1
    j=0
    for point in a['y']:
        a['y'][j]=int(point)
        j+=1
    k=0
    for points in a['rssi']:
        a['rssi'][k]=int(points)
        k+=1
    rbf = Rbf(a['x'], a['y'], a[key], function='linear')
    z = rbf(gx, gy)
    z = z.reshape((num_y, num_x))
    # Render the interpolated data to the plot
    pp.axis('off')
    # begin color mapping
    norm = matplotlib.colors.Normalize(vmin=min(a[key]), vmax=max(a[key]), clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap='RdYlBu_r')
    # end color mapping
    image = pp.imshow(z,extent=(0,_image_width,_image_height, 0),cmap='RdYlBu_r', alpha=0.5, zorder=100)
    pp.colorbar(image)
    pp.imshow(_layout, interpolation='bicubic', zorder=1, alpha=1)
    #print(z)
_plot(a,'rssi',gx,gy,num_x,num_y)