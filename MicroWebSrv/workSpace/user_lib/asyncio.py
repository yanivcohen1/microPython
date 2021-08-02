import uasyncio
from time import sleep

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
