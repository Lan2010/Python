#!/usr/bin/env python3
#-- coding:utf8 --
'''
Created on 2018年9月27日

@author: dev-lan
'''
# def log(func):
#     def wrapper(*args,**kw):
#         print('%s:'% func.__name__)
#         return func(*args,**kw)
#     return wrapper
print('register:failed', 'email', 'Email is already in use.')

import functools

def log(text1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper1(*args,**kw):
            print('%s %s():'% (text1,func.__name__))
            return func(*args,**kw)
        return wrapper1
    return decorator

@log('daw')
def now():
    print('2015-2-1')
    
now()
print(now.__name__)

class A(object):
    bar = 1
    def foo(self):
        print('foo')
    
    @staticmethod
    def static_foo():
        print('static_foo')
        print(A.bar)
        A().foo()
    
    #使用cls参数，编码硬编码
    @classmethod  
    def class_foo(cls):
        print('class_foo')
        print(cls.bar)
        cls().foo()
        
    
A.static_foo()
A.class_foo()
        
        