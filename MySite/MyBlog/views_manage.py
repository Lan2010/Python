#!/usr/bin/env python3
#-- coding:utf8 --
'''
Created on 2018年10月10日

@author: dev-lan
'''
from django.shortcuts import render
from django.template import loader, Context
from django.http import HttpResponse

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p

def manage_blogs(request, page='1'):
    print('------manage_blogs-----')
    t = loader.get_template('manage_blogs.html')
    return HttpResponse(t.render({'page_index': get_page_index(page)}))
