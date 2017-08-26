# -*- coding: utf-8 -*-
# yield from

# yield from 使用示例
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

def grouper(results, key):
    while True:
        results[key] = yield from averager()

def main(data):
    results = {}
    for key , values in data.iterms():
        group = grouper(results, key)
        next(group)
        for value in values:
            group.send(value)
        group.send(None)
    print(results)

def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(',')


# yield from 的简化伪代码
# EXPR = ""
# _i = iter(EXPR)
# try:
#     _y = next(_id)
# except StopIteration as _e:
#     _r = _e.value
# else:
#     while 1:
#         _s = yield _y
#         try:
#             _y = i.send(_s)
#         except StopIteration as _e:
#             _r = _e.value
#             break
#
# RESULT = _r

"""
yield from 类似于 ES6 中的 await，
"""

"""
协程示例程序: 使用协程做离散事件方针
"""

