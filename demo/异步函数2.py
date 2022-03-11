import asyncio
import time


async def say_after(delay: float, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    print(f"started at{time.strftime('%X')}")

    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))
    await task1
    await task2
    # await say_after(1, 'hello')  # 其实就是可阻塞对象
    # await say_after(2, 'world')

    print(f"finished at{time.strftime('%X')}")


# 单线程异步, 作为单线程在运行
if __name__ == '__main__':
    asyncio.run(main())
