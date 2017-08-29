# -*- coding: utf-8 -*-
def simple_cououtine():
    print("-> coroutin started")
    x = yield
    print("-> coroutine received", x)


my_coro = simple_cououtine()
print(my_coro)
next(my_coro)
my_coro.send(42)


# 协程，从程序表现上是一个包含 yield 关键字的函数，并且yield 通常出现在表达式的右边，并且后面可以跟表达式。表达式的值将作为产出值有 yield 生成产出
# 协程的执行过程: 1. 调用协程，得到一个生成器 generator 对象 2. 预激协程，通过 next 调用之前生成的 generator 对象，使协程运行到第一个 yield 处暂停
# 并且生成其后面的值，3. 通过 generator 对象调用其 send() 方法，执行到 下一个 yield 处暂停，传递的值赋值给 yield 左边的变量，然后再次产出 yield 右边表达式
# 的值，直到结束，抛出 StopIteration 异常


# 计算平均值的协程
# def averager():
#     total = 0.0
#     count = 0
#     average = None
#     while True:
#         term = yield average
#         total += term
#         count += 1
#         average = total / count


# 预激协程装饰器
from functools import wraps


def coroutine(func):
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen

    return primer


# 为计算移动平均值的协程添加预激协程的装饰器
@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count
