#!/usr/bin/env python3
#-- coding:utf8 --
'''
Created on 2018年10月9日

@author: dev-lan
'''
import time,hashlib
from django.shortcuts import HttpResponseRedirect

COOKIE_NAME = 'awesession'
_COOKIE_KEY = 'AwEsOmE'

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  

def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = None
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        return None

def checkCookie(request):
    cookie_str = request.COOKIES.get(COOKIE_NAME)
    if cookie_str:
            user = cookie2user(cookie_str)
            if user:
                return user
            
class SimpleMiddleware(MiddlewareMixin):
 
    def process_request(self, request):
        request.__user__ = None
        cookie_str = request.COOKIES.get(COOKIE_NAME)
        if cookie_str:
            user = cookie2user(cookie_str)
            if user:
                request.__user__ = user
        if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
            return HttpResponseRedirect('/signin')
        pass
                