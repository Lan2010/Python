#!/usr/bin/env python3
#-- coding:utf8 --
'''
Created on 2018年10月10日

@author: dev-lan
'''
import json,markdown2
from MyBlog.views import getCookiesUser,get_blog,text2html
from MyBlog.views_manage import get_page_index
from MyBlog.models import Blog,Page,Comment,User
from MyBlog.tools import pagination
from MyBlog.Error import  APIValueError, APIError, APIPermissionError, APIResourceNotFoundError

from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,render_to_response
from django.db.models.query import QuerySet
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt

class BlogEncoder( json.JSONEncoder ):  
    def default(self, obj):     
        if isinstance(obj, Blog):       
            return obj.__str__() 
        if isinstance(obj, Page):       
            return obj.__str__() 
        if isinstance(obj, QuerySet):       
            return obj.__str__() 
        if isinstance(obj, Comment):       
            return obj.__str__() 
        return json.JSONEncoder.default(self, obj)

@csrf_exempt
def api_blogs(request, page='1'):
            
    # 新建blogs
    if request.method == 'POST':
        print('---add_blogs----')
        json_result = json.loads(request.body)
        name = json_result.get('name')
        summary = json_result.get('summary')
        content = json_result.get('content')
        if not name or not name.strip():
            raise APIValueError('name', 'name cannot be empty.')
        if not summary or not summary.strip():
            raise APIValueError('summary', 'summary cannot be empty.')
        if not content or not content.strip():
            raise APIValueError('content', 'content cannot be empty.')
        user = getCookiesUser(request)
        user = User.objects.get(email = user.email)
        blog = Blog(user_id=user.id, user_name=user.name, user_image=user.image, name=name.strip(), summary=summary.strip(), content=content.strip())
        blog.save()
        return HttpResponse(json.dumps(blog, cls= BlogEncoder, ensure_ascii=False).encode('utf-8'), content_type="application/json")

    
    page_index = get_page_index(page)
    num =  Blog.objects.count()
    p = Page(num, page_index)
    blogs=()
    if num != 0:
        blogs =  Blog.objects.order_by('-created_at')[p.offset: p.limit]    
    data_list, page_range, count, page_nums = pagination(request, blogs)
    user = getCookiesUser(request)
    t = loader.get_template('manage_blogs.html')
    context = Context().update({
        'data':data_list,
        'page_range': page_range,
        'count': count,
        'page_nums': page_nums,
        'user':user
        })
    return HttpResponse(t.render(context))

def getall(param):
    comments = Comment.objects.filter(blog_id = param).order_by('-created_at')    for c in comments:
        c.html_content = text2html(c.content)
    return comments



@csrf_exempt
def api_create_comment(request, param):
    json_result = json.loads(request.body)
    content = json_result.get('content')
    user = request.user
    if user is None:
        raise APIPermissionError('Please signin first.')
    if not content or not content.strip():
        raise APIValueError('content')
    user = User.objects.get(email = user.email)
    blog = Blog.objects.get(id = param)
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image, content=content.strip())
    comment.save()
    return HttpResponse(json.dumps(comment, cls= BlogEncoder, ensure_ascii=False).encode('utf-8'), content_type="application/json")

@csrf_exempt
def edit_blog(request):
    print('-----------edit_blog-----------------')
    #blog编辑页面
    if request.method == 'GET':
        t = loader.get_template('manage_blog_edit.html')
        __id__ = request.GET.get('id')
        blog = Blog.objects.get(id = __id__)
        user = getCookiesUser(request)
        context = Context().update({
            'blog': blog,
            'user':user
            })
        return HttpResponse(t.render(context))
    #保存blog
    if request.method == 'POST':
        __id__ = request.GET.get('id')
        json_result = json.loads(request.body)
        name = json_result.get('name')
        summary = json_result.get('summary')
        content = json_result.get('content')
        Blog.objects.filter(id = __id__).update(name = name,summary = summary,content = content)
        blog = Blog(id=__id__,name=name,summary=summary,content=content)
        return HttpResponse(json.dumps(blog, cls= BlogEncoder, ensure_ascii=False).encode('utf-8'), content_type="application/json")


def delete_blog(request):
    print('-----------delete_blog-----------------')
    param = request.GET.get('id')
    Blog.objects.get(id = param).delete()
    return redirect('/api/blogs/')

def create_blog(request):
    print('-----------create_blog-----------------')
    user = getCookiesUser(request)
    t = loader.get_template('manage_blog_edit.html')
    context = Context().update({
        'user':user,
        'action': '/api/blogs/'
        })
    return HttpResponse(t.render(context))

def get_blog(request,param):
    print('-----------get_blog-----------------')
    blog = Blog.objects.get(id = param)
    return HttpResponse(json.dumps(blog, cls= BlogEncoder, ensure_ascii=False).encode('utf-8'), content_type="application/json")

    