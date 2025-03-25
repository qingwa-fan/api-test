# 装饰器：在不改变原方法的基础上，为该方法添加新的功能
# python的闭包：
# 函数中嵌套函数，内部函数引用外部函数的变量，外部函数把内部函数名返回
# def outer(x):
#     def inner(y):
#         return x + y
#     return inner
#
# # outer(3)  # outer(3) 返回的是一个 inner 内部函数的函数名称
# print(outer(3)(6))   # outer(3)(6) == inner(6)

# def func_2(func):
#     print("执行func_2的功能")
#     def func_3():
#         func()
#     return func_3
#
# @func_2       # func_2 装饰了函数 func_1, 此时 func_1 的函数名会以参数的形式传给 func_2 的形参，然后执行func_2中的代码
# def func_1():
#     print("执行func_1中的功能")
#
# func_1()


# def func_1(*args, **kwargs):  # *args -> 可变参数， **kwargs -> 可变关键字参数
#     a = args
#     b = kwargs
#     print(a)
#     print(b)
#
# func_1()
# func_1(by="locator", name="yuan")

# def func_B(func):
#     def func_b(x):
#         return 2*func(x)
#     return func_b
#
# @func_B
# def func_A(x):
#     return int(x)+1

def func_B(func):
    def func_b(*args, **kwargs):
        return 2*func(*args, **kwargs)  # 2*func_A(1, 2)
    return func_b

@func_B
def func_A(x,y):
    return int(x)+int(y)

if __name__ == '__main__':
    print(func_A(1, 2))  # func_A == func_b  所以 func_A(1, 2) == func_b(1, 2)








