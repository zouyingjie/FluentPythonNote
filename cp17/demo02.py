# -*- coding: utf-8 -*-

# 使用 concurrent.futures 包来并发下载
# ThreadPoolExecutir 线程池
# ProcessPoolExecutor 进程池
import os
from concurrent import futures

import sys

import requests
import time

POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = "http://flupy.org/data/flags"
DEST_URL = "./"

# 保存图片
def save_flat(img, filename):
    path = os.path.join(DEST_URL, filename)
    with open(path, 'wb') as fp:
        fp.write(img)

# 下载图片
def get_flag(cc):
    url = '{}/{cc}{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content

# 显示文本
def show(text):
    print(text, end='  ')
    sys.stdout.flush()

def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))

MAX_WORKERS = 20 #设定线程池的最大线程数

def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flat(cc, cc.lower()+ ".gif")
    return cc

# def download_many(cc_list):
#     workers = min(MAX_WORKERS, len(cc_list))
#     with futures.ThreadPoolExecutor(workers) as executor:
#         res = executor.map(download_one, sorted(cc_list))
#
#     return len(list(res))

# 使用 futures.as_completed 函数 修改 download_many 函数

def download_many(cc_list):
    cc_list = cc_list[:5]

    with futures.ThreadPoolExecutor(max_workers=3) as executor: # 获取到线程池的执行器
        to_do = []
        for cc in sorted(cc_list):
            # submib 生成一个 Future 期物对象, 表示排期后待执行的操作
            future = executor.submit(download_many, cc)
            to_do.append(future)
            msg = 'Schedule for {}:{}'
            print(msg.format(cc, future))

        # 遍历所有的期物对象，使用 futures.as_completed() 方法执行，返回期物执行完成后的结果，
        # 第一个程序中的 futures.map() 相当于直接完成了 submit 和 as_completed() 两步返回期物完成后的街而过
        results = []
        for future in futures.as_completed(to_do):
            res = future.result()
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            results.append(res)
    return len(results)
if __name__ == '__main__':
    main(download_many)

"""
CPython 解释器有全局解释器锁(GIL), 一次只允许使用一个线程执行 Python 字节码，因此无法使用多核 CPU 的优势
然鹅，标准库中所有执行阻塞型的 IO 操作的函数在等待返回结果时都会释放 GIL,因此，一个Python线程等待网络响应的时候，阻塞型 IO 函数
会释放 GIL，在运行一个线程。
"""

"""
concurrent.futures 提供了两个类，ThreadPoolExecutor 和 ProcessPoolExecutor ，前者作为线程池，可以任意指定线程的数量，
比较适合IO 密集型操作。而 ProcessPoolExecutor 是把工作分配给多个进程，因此受 CPU 数据的影响，不适合 IO 密集型操作，更加适合
CPU 密集型操作

Python 基本的线程和进程实现是 threading 和 multiprocessing 包， concurrent.futures 是在该基础之上的使用线程的最新方式，如果觉得
futures 不够灵活也可以使用 threading 和 multiprocessing

使用 futures 时，通过 submit 获取所有的 期物 Future 对象然后使用 as_completed() 方法获取期物对象的结果比使用 map 更加
的灵活，另外 as_completed 方法有个惯用法是构建一个字典，将期物对象作为 key, 然后映射到其他数据上，这在运行结束后可能比较有用
。比如顺序，期物的运行结果顺序是混乱的，而我们可以通过期物映射的数据来进行后续的处理
"""


