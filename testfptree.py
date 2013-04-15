#coding=utf-8
from math import ceil as cl
from fpgrowth import Fpgrowth
import time

data = {}
count = 10000
idx = 0
import codecs
#with codecs.open("neg.txt",'r','utf-8') as fr:
with codecs.open("new.txt",'r','utf-8') as fr:
    for line in fr.readlines():
        data[idx] = [it+'-' for it in set(line.split())]
       # data[idx] = set(line.split()])
        idx += 1
##        count -= 1
##        if count <=0:
##            break
##with codecs.open("connect-4.data",'r','utf-8') as fr:
##    for line in fr.readlines():
##        its = line[:-1].split(',')
##        #print len(its),its
##        for i in range(len(its)):
##            its[i] = str(i)+'-'+its[i]
##        data[idx] = its
##        idx += 1
print len(data)
#th = 10*1.0/len(data)
th = 0.1
th1=0.2
print 'th =',th

start = time.time()
##data = {
##    0: ['f','a','c','d','g','i','m','p'],
##    1: ['a','b','c','f','l','m','o'],
##    2: ['b','f','h','j','o'],
##    3: ['b','c','k','s','p'],
##    4: ['a','f','c','e','l','p','m','n'],
##    }

#th = 3.0/5

fp = Fpgrowth()

fp.Processing(data,th,th1)

print 'using time:',time.time() - start
total = 0
pts = fp.GetPattern()
for p in pts:
    for pp in pts[p]:
        print ''.join(pp[0]), pp[1]
    total += len(pts[p])
    
print 'pattern finding', total,
