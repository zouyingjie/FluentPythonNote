### 笔记汇总

* 1. 真正的构造方法是 __new__ 方法，__init__ 是初始化方法，在 __new__ 调用完成生成实例，然后传入 __init__ 方法

* 2. 当实例属性和类属性同名时，实例属性会覆盖掉类属性
* 3. obj.attr 表达式查找的顺序是，首先从 obj.__class__ 中开始寻找 attr, 并且当类中没有名为 attr 的特性时，Python 才会在 obj 的实例中寻找。
即 obj.data 的查找顺序是: 先查找是否有类属性 data, 然后查找是否有 property 特性 data，有的话返回特性的值，没有特性则查找是否有实例属性 data
有的话返回实例属性 data, 否则返回类属性 data

```
class PropertyDemo:
    """
    使用属性示例
    """

    def __init__(self, data):
        set._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
```
