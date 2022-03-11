import asyncio


async def demo():

    for i in range(10):
        print(i)
        await asyncio.sleep(1)
        print(f"{-i}")
    print("end")
    # await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(demo())
    print("hello, 世界!")
