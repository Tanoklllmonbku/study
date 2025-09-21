# MRO - прослеживание порядка наследования
# Критично для ООП и CleanArch

# class Parent: pass
#
# class ChildA(Parent): pass
#
# class ChildB(Parent, ChildA): pass
#
# class ChildC(Parent, ChildB): pass
# Ошибки MRO. Наследник А уже наследуется от родителя, в наследниках В и С не нужно Parent


class Parent:
    def __init__(self):
        print("Parent")


class ChildA(Parent):
    def __init__(self):
        super().__init__()
        print("ChildA")


class ChildB(ChildA):
    def __init__(self):
        super().__init__()
        print("ChildB")


class ChildC(Parent):
    def __init__(self):
        super().__init__()
        print("ChildC")


class ChildD(ChildB, ChildC):
    def __init__(self):
        super().__init__()
        print("ChildD")


print(ChildD.__mro__)

class ChildF(ChildC, ChildB):
    def __init__(self):
        super().__init__()
        print("ChildF")

print(ChildF.__mro__)

D = ChildD()
print("_"*15)
F = ChildF()