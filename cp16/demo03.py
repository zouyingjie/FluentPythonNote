
# -*- coding: utf-8 -*-
# 终止协程与异常处理: throw 和 close
class DemoException(Exception):
    """演示"""
    pass


def demo_exc_handling():
    print("-> coroutine started")
    while True:
        try:
            x = yield
        except DemoException as e:
            print('-> DemoException handled Continuing')
        else:
            print('-> coroutine received :', x)
    raise RuntimeError("this line should never run")

exec_coro = demo_exc_handling()
next(exec_coro)
exec_coro.send(11)
exec_coro.send(12)
# 发送 GeneratorExit 异常，没有处理的话会正常退出
exec_coro.close()
# 发送指定异常，如果没有处理则向上冒泡
# exec_coro.throw(ZeroDivisionError)
from inspect import getgeneratorstate
print(getgeneratorstate(exec_coro))


# 让协程返回值
from collections import namedtuple
Result = namedtuple("Result", "count average")

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)

print("==============")

coro_avg = averager()
next(coro_avg)
coro_avg.send(10)
coro_avg.send(30)
coro_avg.send(6.5)
try:
    excepton = coro_avg.send(None)

# 传递 None 后导致协程中循环 break 结束，协程结束，抛出 StopIterException
# 然后 return 的表达式会传给调用方，将值赋给 StopIterException 的 value 属性
# 在这里可以通过 try-catch 捕获异常后获取其 value， 而通过 yield from ，解释器不仅可以捕获 StopIterException ，还可以将
# 其 value 属性的值变成  yield from 表达式的值
except StopIteration as e:
    print(e.value)

"""
协程有两种终止方式: 第一提供一个 哨兵值，当send 该值是终止，然后协程会返回值。或者调用 close 方法，会传递 GeneratorExitException,
如果没有处理则终止协程，且调用方不会报错
"""