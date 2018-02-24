import os
import threading

from time import ctime,sleep

def segmentation(x):
	os.system("python test_segmentation.py --city_name "+x)

threads = []
t1 = threading.Thread(target=segmentation,args=(u"Beijing",))
threads.append(t1)
t2 = threading.Thread(target=segmentation,args=(u"Shanghai",))
threads.append(t2)
t3 = threading.Thread(target=segmentation,args=(u"Guangzhou",))
threads.append(t3)

if __name__ == '__main__':
	#多线程，一个city一个线程
    for t in threads:
        t.setDaemon(True)
        t.start()
    
    t.join()

    #print "all over %s" %ctime()

#os.system("python test_segmentation.py --city_name Beijing")
#os.system("python test_segmentation.py --city_name Shanghai")
#os.system("python test_segmentation.py --city_name Guangzhou")


