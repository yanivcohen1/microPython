try:
    import uasyncio
except:
    import asyncio as uasyncio

from time import sleep

def wait_for_event():

    lock = uasyncio.Lock()

    async def waiter(name, event):
        for i in range(2):
            print(name, i, 'waiting for it ...')
            await event.wait()
            event.clear()
            async with lock:
                print(name, i, '... got it!')

    async def main():
        # Create an Event object.
        event = uasyncio.Event()

        # Spawn a Task to wait until 'event' is set.
        waiter_task = uasyncio.create_task(waiter('one', event))
        waiter_task2 = uasyncio.create_task(waiter('two', event))

        # Sleep for 1 second and set the event.
        await uasyncio.sleep(2)
        event.set()
        await uasyncio.sleep(3)
        event.set()

        # Wait until the waiter task is finished.
        await waiter_task
        await waiter_task2

    uasyncio.run(main())

def wait_for_async_fun():
    sleep_sec = 2
    async def eternity():
        # Sleep for one hour
        await uasyncio.sleep(sleep_sec-1)
        print('yay!')

    async def main(_sleep_sec):
        # Wait for at most 1 second
        try:
            await uasyncio.wait_for(eternity(), timeout = _sleep_sec)
        except uasyncio.TimeoutError:
            print('timeout!')

    uasyncio.run(main(sleep_sec)) #  yay!
    uasyncio.run(main(sleep_sec-2)) # timeout!

# how to use it
# import user_lib.asyncios as asy
# asy.wait_for_event()
# asy.wait_for_async_fun

# run in local file
# wait_for_event()

# wait_for_event print output
# one 0 waiting for it ...
# two 0 waiting for it ...
# one 0 ... got it!
# one 1 waiting for it ...
# two 0 ... got it!
# two 1 waiting for it ...
# one 1 ... got it!
# two 1 ... got it!