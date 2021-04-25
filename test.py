class MetaClass(type): 
    def __iter__(cls): 
        return iter(cls.objs)

class Class(metaclass=MetaClass): 
    objs = []
    def __init__(self, x):
        self.x = x 
        self.objs.append(self)

c = Class(10)
c2 = Class(20)
c3 = Class(30)

for _cls in Class: 
    print(_cls.x)

