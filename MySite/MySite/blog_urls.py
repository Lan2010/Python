#!/usr/bin/env python3
#-- coding:utf8 --
'''
Created on 2018年10月10日

@author: dev-lan
'''
from django.conf.urls import url
from MyBlog.views_blogs import *

urlpatterns =[
    url(r'^$',api_blogs),
    url(r'(\w+)/comments$',api_create_comment),
    url(r'edit$',edit_blog),
    url(r'delete$',delete_blog),
    url(r'create$',create_blog),
    url(r'get/(\w+)$',get_blog), 

]