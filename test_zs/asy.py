import random
import asyncio
from time import sleep


class Potato:
    @classmethod
    def make(cls, num, *args, **kwargs):
        x = []
        for i in range(num):
            x.append(cls.__new__(cls, *args, **kwargs))
        return x


allp = Potato.make(5)


def ask_for_pota():   
    # await asyncio.sleep(random.random())
    allp.extend(Potato.make(random.randint(1, 9)))


def take_potato(num):
    count = 0
    while True:
        if len(allp) == 0:
            # sleep(0.1)
            ask_for_pota()
        else:
            pota = allp.pop()
            yield pota
            count += 1
            if count == num:
                break


def buy():
    bucket = []
    for i in take_potato(10):
        bucket.append(i)
        print(f'{id(i)}')

print(buy())
# 1940515928264
# 1940510263816
# 1940510076872
# 1940510076552
# 1940512893960
# 1940516882888
# 1940516882824
# 1940516883144
# 1940516558984
# 1940516558408
# None   why none ???



# ******************************************************************
# async way
# ******************************************************************
# class Potato:
#     @classmethod
#     def make(cls, num, *args, **kwargs):
#         x = []
#         for i in range(num):
#             x.append(cls.__new__(cls, *args, **kwargs))
#         return x

# class Tomato:
#     @classmethod
#     def make(cls, num, *args, **kws):
#         all_toma = []
#         for i in range(num):
#             # new a current class object  <__main__.Tomato object at 0x000001DA0EF92748>
#             all_toma.append(cls.__new__(cls, *args, **kws))
#         return all_toma


# all_toma = Tomato.make(6)
# print(all_toma)

# allp = Potato.make(5)


# async def take_potato(num):
#     count = 0
#     while True:
#         if len(allp) == 0:
#             await ask_for_pota()
#         else:
#             pota = allp.pop()
#             yield pota
#             count += 1
#             if count == num:
#                 break


# async def ask_for_pota():
   
#     await asyncio.sleep(random.random())
#     allp.extend(Potato.make(random.randint(1, 9)))

# async def ask_for_toma():


# async def buy():
#     bucket = []
#     async for i in take_potato(10):
#         bucket.append(i)
#         print(f'Got potato {id(i)}................')


# async def take_tomato(num):
#     count = 0
#     while True:
#         if len(all_toma) == 0:
#             sleep(.1)
#         else:
#             toma = all_toma.pop()
#             yield toma
#             count += 1
#             if count == num:
#                 break


# async def buy_tomato():
#     bucket = []
#     async for t in take_tomato(7):
#         bucket.append(t)
#         print(f'Got tomato {id(t)}********')


# # print(buy())
# import asyncio
# loop = asyncio.get_event_loop()
# res = loop.run_until_complete(asyncio.wait([buy_tomato()]))
# loop.close()