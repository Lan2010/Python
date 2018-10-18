import json,hashlib,time,markdown2,re,logging
from django.shortcuts import render,redirect,render_to_response
from django.template import loader, Context
from django.http import HttpResponse,HttpResponseRedirect
from MyBlog.models import *
from MyBlog.tools import pagination
from MyBlog.Error import  APIValueError, APIError, APIPermissionError, APIResourceNotFoundError
from django.views.decorators.csrf import csrf_exempt
from MyBlog.mymiddleware import COOKIE_NAME,_COOKIE_KEY

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

def cookie2user(cookie_str):
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = User.objects.filter(id=uid).first()
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None
    
def getCookiesUser(request):
    cookie_str = request.COOKIES.get(COOKIE_NAME)
    user = None
    if cookie_str:
        users =  cookie2user(cookie_str)
        if users:
            user = users
    return user 
    
def archive(request):
    posts = BlogPost.objects.all()
    t = loader.get_template('archive.html')
    return HttpResponse(t.render({'posts': posts}))


def index(request, page='1'):
    print('----------index------')
    blogs = Blog.objects.get_queryset().order_by('id')
    data_list, page_range, count, page_nums = pagination(request, blogs)
    user = getCookiesUser(request)
    t = loader.get_template('blogs.html')
    context = Context().update({'data': data_list,
    'page_range': page_range,
    'count': count,
    'page_nums': page_nums,
    'user':user
        })
    return HttpResponse(t.render(context))

def signin(request):
    return render(request,'signin.html')

class UserEncoder(json.JSONEncoder ):  
    def default(self, obj):      
        if isinstance(obj, User):       
            return obj.name    
        return json.JSONEncoder.default(self, obj)


@csrf_exempt
def login(request):
    print('----login------')
    json_result = json.loads(request.body)
    email = json_result.get('email')
    passwd = json_result.get('passwd')
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = User.objects.filter(email=email)
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check passwd:
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie:
#     user.passwd = '*******'
    r = HttpResponse(json.dumps(user, cls=UserEncoder, ensure_ascii=False).encode('utf-8'))
    cookieString = user2cookie(user, 86400)
    r.set_cookie(COOKIE_NAME, cookieString, max_age=86400, httponly=True)
    r.content_type = 'application/json; charset=utf-8'
    return r


def signout(request):
    response = render(request,'signin.html')
    response.delete_cookie(COOKIE_NAME)
    return response

def register(request):
    return render(request,'register.html')

# 用户注册
@csrf_exempt
def api_user(request):
    json_result = json.loads(request.body)
    email = json_result.get('email')
    name = json_result.get('name')
    passwd = json_result.get('passwd')
    print('-----email-------:',email)
    print('-----name-------:',name)
    print('-----passwd-------:',passwd)
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users = User.objects.filter(email=email)
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    shal_passwd = '%s:%s' % (uid, passwd)
    print('type:',type(time.time()))
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(shal_passwd.encode(encoding='utf_8')).hexdigest(),admin=1, image='http://www.gravatar.com/avatar/%s?d=wavatar&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    user.save()
    # make session cookie:
    r = HttpResponse(json.dumps(user, cls=UserEncoder, ensure_ascii=False).encode('utf-8'))
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    r.content_type = 'application/json; charset=utf-8'
    return r

def text2html(text):
    lines = map(lambda s: '<p>%s</P>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)

def get_blog(request,param):
    blog = Blog.objects.get(id=param)
    comments = Comment.objects.filter(blog_id = param).order_by('-created_at')
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = markdown2.markdown(blog.content)
    user = getCookiesUser(request)
    t = loader.get_template('blog.html')
    context = Context().update({
        'blog': blog,
        'comments': comments,
        'user':user
        })
    return HttpResponse(t.render(context))
    