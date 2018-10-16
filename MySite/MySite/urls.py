"""MySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import  include, url
from django.contrib import admin
from django.urls import path
from MyBlog.views import *
from MyBlog import views_manage
import MySite
from django.conf.urls.static import static
from django.conf import settings

extra_patterns = [
    url(r'blogs',views_manage.manage_blogs),
    ]

urlpatterns =[
    url(r'^admin/',admin.site.urls),
    url(r'^$', index),
    url(r'^MyBlog/$', archive),
    url(r'^index/$', index),
    url(r'signin$', signin),
    url(r'^register$', register),
    url(r'^api/authenticate/$', login),
    url(r'^signout$', signout),
    url(r'^blog/(.+)$', get_blog),
    url(r'^register/$', register),
    url(r'^api/users$', api_user),
    url(r'^api/blogs/',include('MySite.blog_urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)