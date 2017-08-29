# -*- coding: utf-8 -*-
"""
1. 当实例属性和类属性同名时，实例属性会覆盖掉类属性
2. obj.attr 表达式查找的顺序是，首先从 obj.__class__ 中开始寻找 attr, 并且当类中没有名为 attr 的特性时，Python 才会在 obj 的实例中寻找

即 obj.data 的查找顺序是: 先查找是否有类属性 data, 然后查找是否有 property 特性 data，有的话返回特性的值，没有特性则查找是否有实例属性 data
有的话返回实例属性 data, 否则返回类属性 data
"""


# 使用属性示例
class PropertyDemo:

    def __init__(self, data):
        set.data = data

    @property
    def data(self, data):
        return self.data

    @data.setter
    def data(self, data):
        self.data = data


class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


# 把商品属性换成特性
class LineItem2:

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError("value must be > 0")


# 给特性加文档注释，和其他的类，方法加注释一致
class Foo:

    @property
    def bar(self):
        '''The bar attribute'''
        return self.__dict__['bar']

    @bar.setter
    def bar(self, value):
        self.__dict__['bar'] = value


# 以下为特性工厂函数程序示例
# 根据名称来创建属性
# 因为 Python 中，函数是作为一级对象的，因此可以直接把函数作为工厂
# Java 中的话需要使用一个工厂类
def quantity(storage_name):
    def qty__getter(istance):
        return istance.__dict__[storage_name]

    def qty_setter(istance, value):
        if value > 0:
            istance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')
    # 构建自定义的特性对象
    # 四个参数，get, set, del 和 doc
    return property(qty__getter, qty_setter)


class LineItem3:

    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


# 特性删值方法: deleter
class BlackKnight:
    def __init__(self):
        self.members = ['an arm', 'another arm', 'a leg', 'another leg']
        self.phrases = ['Tis but a scratch']

    @property
    def member(self):
        print('next member is')
        return self.member

    @member.deleter
    def member(self):
        text = 'BLACK KNIGHT(loses {})\n-- {}'
        print(text.format(self.members.pop(0), self.phrases.pop(0)))
    # 使用经典方式创建
    # member = property(member.getter, fdel=member_deleter)


# 处理属性的属性和函数

# 1. __class__ ，对象所属类的引用， __getattr__ 只在对象的类中寻找，而不在实例中寻找
# 2. __dict__， 存储类或对象的可写属性，有 __dict__ 属性的对象任何时候都可以新增属性
# 3. __slots__

# 处理属性的内置函数

getattr()  # 获取对象的属性，可以设置返回值
setattr()  # 给对象设置指定的属性值，没有的话会新建属性
hasattr()  # 判断对象有没有某属性
dir()  # 列出大多数属性
vars()  # 返回对象的 __dict__ 属性

# 处理属性的特殊方法


class Class:

    # 获取指定属性失败时调用
    def __getattr__(self, item):
        pass

    # 取值时调用
    def __getattribute__(self, item):
        pass

    # 设值时调用
    def __setattr__(self, key, value):
        pass

    # 将对象传给 dir() 时会调用
    def __dir__(self):
        pass

    # 使用 del 语句删除属性时会调用
    def __delattr__(self, item):
        pass
