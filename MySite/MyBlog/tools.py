#!/usr/bin/env python3
#-- coding:utf8 --
'''
Created on 2018年10月9日

@author: dev-lan
'''
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# 分页函数
def pagination(request,queryset,display_amount=2, after_range_num = 5,before_range_num = 4):
    try:
        #从请求获取page值
        page = int(request.GET.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    # 引用Paginator类,display_amount每页显示数目
    paginator = Paginator(queryset,display_amount)
    #总计的数据条目
    count = paginator.count
    # 合计页数
    num_pages = paginator.num_pages
    
    try:
        #获得分页列表
        objects = paginator.page(page)
    #如果页数不存在   
    except EmptyPage:
        #获得最后一页
        objects = paginator.page(paginator.num_pages)
    #根据参数配置导航显示范围
    temp_range = paginator.page_range
    
    #如果页面很小
    if(page - before_range_num)<=0:
        #如果总页面比after_range_num大，那么显示到after_range_num
        if temp_range[-1] > after_range_num:
            page_range = range(1, after_range_num+1)
        #否则显示当前页
        else:
            page_range = range(1, temp_range[-1]+1)
        #如果页面比较大
    elif (page + after_range_num) > temp_range[-1]:
        #显示到最大页
        page_range = range(page-before_range_num,temp_range[-1]+1)
    #否则在before_range_num和after_range_num之间显示
    else:
        page_range = range(page-before_range_num+1, page+after_range_num)
    
    #返回分页相关参数
    return objects, page_range, count, num_pages
    
    