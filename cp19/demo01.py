# -*- coding: utf-8 -*-
"""
动态属性(attribute)和特性(property)

1. 真正的构造方法是 __new__ 方法，__init__ 是初始化方法，在 __new__ 调用完成生成实例，然后传入 __init__ 方法
2.
"""

from collections import abc
import keyword


# 将 JSON 结构转换为一个类
class FrozenJSON:

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


# 使用 __new__ 改造上面的 build 方法
class FrozenJSONNew:

    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON(self.__data[name])


# 使用 shelve 模块调整 JSON 数据源结构
import shelve
import warnings

DB_NAME = "data/schedule_db"
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def load_db(db):
    # raw_data = iscibfeed.load()
    raw_data = {}
    warnings.warn('loading' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        record_type = collection[:-1]
        for record in rec_list:
            key = "{}.{}".format(record_type, record['serial'])
            record['serial'] = key
            db[key] = Record(**record)


db = shelve.open(DB_NAME)
load_db(db)
