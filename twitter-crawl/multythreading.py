'''Does scraping in various threads.

'''


from twitter_handles import get_handles
from tweets import get_tweets
from threading import Thread
import threading
import timeit
import time

TWEETS_NUM = 1000
THREAD_NUM = 4

if __name__ == '__main__':
    handles = get_handles()

    print handles

    threads = []
    for handle in handles[0:THREAD_NUM]:
        thread = Thread(target=get_tweets, args=(handle, TWEETS_NUM))
        threads.append(thread)

    t0 = timeit.default_timer()
    print 'Start threading'

    for thread in threads:
        thread.start()

    print 'End threading'
    while True:
        # time.sleep(0.5)
        if threading.activeCount() == 1:
            break
    t1 = timeit.default_timer()
    print t1 - t0
