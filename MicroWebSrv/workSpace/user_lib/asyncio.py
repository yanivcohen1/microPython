import uasyncio
from time import sleep

def wait_for_fun():
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

def wait_for_event():

    async def waiter(event):
        print('waiting for it ...')
        await event.wait()
        print('... got it!')

    async def main():
        # Create an Event object.
        event = uasyncio.Event()

        # Spawn a Task to wait until 'event' is set.
        waiter_task = uasyncio.create_task(waiter(event))

        # Sleep for 1 second and set the event.
        await uasyncio.sleep(1)
        event.set()

        # Wait until the waiter task is finished.
        await waiter_task

    uasyncio.run(main())