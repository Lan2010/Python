import time,uuid
from django.db import models
from django.contrib import admin

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField();
    timeStamp = models.DateTimeField();
    author = models.CharField(max_length=30)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'timeStamp','author')

admin.site.register(BlogPost, BlogPostAdmin)

class Blog(models.Model):
    id = models.IntegerField(primary_key=True);
    user_id = models.TextField();
    user_name = models.TextField();
    user_image = models.TextField();
    name = models.TextField();
    summary = models.TextField();
    content =models.TextField();
    created_at = models.DateTimeField(auto_now_add=True);
    
    class Meta:   
        db_table = 'blogs'

class User(models.Model):
    id = models.TextField(primary_key=True);
    email = models.TextField();
    passwd = models.TextField();
    admin = models.IntegerField();
    name = models.TextField();
    image = models.TextField();
    created_at = models.DateTimeField(auto_now_add=True);
    class Meta:
        db_table ='users'

class Comment(models.Model):
    id = models.IntegerField(primary_key=True);
    blog_id = models.TextField();
    user_id = models.TextField();
    user_name = models.TextField();
    user_image = models.TextField();
    content = models.TextField();
    created_at = models.DateTimeField(auto_now_add=True);
    class Meta:
        db_table ='comments'
        
class Page(object):
    def __init__(self, item_count, page_index=1, page_size=10):
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
        if (item_count == 0) or (page_index > self.page_count):
            self.offset = 0
            self.limit = 0
            self.page_index = 1
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1

    def __str__(self):
        return 'item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s' % (self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)

    __repr__ = __str__
    