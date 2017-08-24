import asyncio
import datetime

'''
async def display_date(num, loop):  # 声明一个协程
    end_time = loop.time() + 10.0
    while True:
        print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(2)  # 等同于yield from


loop = asyncio.get_event_loop()  # 获取一个event_loop

tasks = [display_date(1, loop), display_date(2, loop)]

loop.run_until_complete(asyncio.gather(*tasks))  # 阻塞直到所有的tasks完成
loop.close()'''

async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)  # 协程compute不会继续往下面执行，直到协程sleep返回结果
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)  # 协程print_sum不会继续往下执行，直到协程compute返回结果
    print("%s + %s = %s" % (x, y, result))

loop = asyncio.get_event_loop()
loop.run_until_complete(print_sum(1, 2))
loop.close()

