#!encoding:utf-8

import threading
import time
import os
from   multiprocessing import Pool,Queue
import multiprocessing

# This function could be any function to do other chores.


def doChore():
    time.sleep(1)

# Function for each thread

    # Available ticket number
    # Lock (i.e., mutex)
i = 10
lock = threading.Lock()





# Start of the main function

def multithred():
    threads=list()
    # Start 10 threads
    for k in range(2):
        # Set up thread; target: the callable (function) to be run, args: the
        # argument for the callable
        new_thread = threading.Thread(target=booth, args=(k,))
        new_thread.setDaemon(True)
        new_thread.start()
        threads.append(new_thread)
        # new_thread.join()         

    for t in threads:
        # t.setDaemon(True)
        t.join()                        # run the thread

    print('main thred end')



def func(msg):
    print "msg:", msg
    time.sleep(3)
    print "end"

# if __name__ == "__main__":
#     pool = Pool(processes = 3)
#     for i in xrange(4):
#         msg = "hello %d" %(i)
#         pool.apply_async(func, (msg, ))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去

#     print "Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~"
#     pool.close()
#     pool.join()   #调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
#     print "Sub-process(es) done."


def booth(num,pname):
    while(True):
        num.value+=1
        n=num.value
        print(n)
        if(n>=1000000):
            return
        

def test():
    print('test')


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    pool=Pool()
    num = manager.Value('d', 0.0)
    pool.apply_async(booth,args=(num,'1'))
    pool.apply_async(booth,args=(num,'2'))
    pool.close()
    pool.join()
    print("main process end")


