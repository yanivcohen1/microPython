from    _thread     import start_new_thread, allocate_lock, get_ident
from time import sleep
import uasyncio as asyncio

def thread_event_test():
    tsf = asyncio.ThreadSafeFlag()

    def cb(_):
        while True:    
            tsf.set()
            sleep(1)

    async def foo():
        while True:
            await tsf.wait()
            # Could set an Event here to trigger multiple tasks
            print('Triggered from thread')

    # tim = Timer(1, freq=1, callback=cb)
    start_new_thread(cb, (1,))
    asyncio.run(foo())

def thread_test():

    lock = allocate_lock()

    def fun_1(num):
        with lock:
            # lock.acquire() // use as binary Semaphore- like event.wait()
            print('thread:', num, 'ident:', get_ident())
            # lock.release() // use as binary Semaphore- like event.clear() & event.set()

    def fun_2(num):
        with lock:
            # lock.acquire() // use as binary Semaphore- like event.wait()
            print('thread:', num, 'ident:', get_ident())
            # lock.release() // use as binary Semaphore- like event.clear() & event.set()

    def main():
        # Spawn a Task to wait until 'event' is set.
        start_new_thread(fun_1, (1,))
        start_new_thread(fun_2, (2,))
        # Sleep for 1 second and set the event.
        sleep(2)

    main()

# use it
# import user_lib.thread as t
# t.thread_test()
# t.thread_event_test()