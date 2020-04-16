#!/usr/bin/python
#Author: Vijay Nag
import urllib, json
from datetime import datetime
from scipy import optimize
from matplotlib import pylab as plt
import numpy as np
import pdb
from numpy import log

url="https://api.covid19india.org/raw_data.json"
response = urllib.urlopen(url)
data=json.loads(response.read())
ka_data=filter(lambda x:  x[u'detectedstate']=="Karnataka",data[u'raw_data'])
dates=list(set(map(lambda x: x[u'dateannounced'], ka_data)))
bydate=dict(map(lambda d: (d,filter(lambda x: x[u'dateannounced']==d,ka_data)),dates))
x_axis=map(lambda x: str(x[0]),sorted(bydate.items(),key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"),reverse=False))
positives=map(lambda x: len(x[1]),sorted(bydate.items(),key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"),reverse=False))
y_axis=[sum(positives[0:i+1]) for i in xrange(0,len(positives))]
dtime=map(lambda x: log(2)/(log(x[1])-log(x[0])),zip(y_axis,y_axis[1:]))
print "Total cases: %d"%(sum(positives))
for t in zip(x_axis,dtime): print "%5s     %20s"%(t[0],t[1])
xaxis=[x for x in xrange(1,len(x_axis))]
plt.plot(xaxis,dtime)
plt.title('Covid-19 Karnataka State Growth Rate')
plt.xlabel('Days')
plt.xticks(xaxis,x_axis,rotation='vertical')
plt.ylabel('Doubling Time in days')
plt.gca().invert_yaxis()
plt.show()
