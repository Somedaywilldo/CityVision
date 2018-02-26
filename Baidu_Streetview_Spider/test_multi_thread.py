#!/usr/bin/python3

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开始线程：" + self.name)
        print_time(self.name, self.counter, 5)
        print ("退出线程：" + self.name)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启新线程
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print ("退出主线程")






from multiprocessing import Pool
import os, time, random

def long_time_task(name,test):
	print("testarg:",test)
	print('Run task %s (%s)...' % (name, os.getpid()))
	start = time.time()
	time.sleep(random.random() * 3)
	end = time.time()
	print('Task %s runs %0.2f seconds.' % (name, (end - start)))
	return name

for j in range(3):
	print('Parent process %s.' % os.getpid())
	p = Pool(3)
	result=[]
	for i in range(4):
		d = 0
		result.append(p.apply_async(long_time_task, args=(i,i-1,), callback=d))
	for i in result:
		print(i.get()+123123)
	print('Waiting for all subprocesses done...')
	p.close()
	p.join()
	print('All subprocesses done.')