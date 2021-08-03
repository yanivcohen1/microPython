from    _thread     import start_new_thread, allocate_lock, get_ident
from time import sleep

def thread_test():

    lock = allocate_lock()

    def fun_1(num):
        with lock:
            print('thread_', num, 'ident:', get_ident())

    def fun_2(num):
        with lock:
            print('thread:', num, 'ident:', get_ident())

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