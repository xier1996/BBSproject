from django.shortcuts import render,redirect,HttpResponse
from my_web import models
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django_comments.models import Comment
from my_web.AuthRegisterForm import AuthRegisterForm
import json
import re
import os
import django.utils.timezone as timezone
from PIL import Image
from django.core.paginator import Paginator
# 首页
def index(request):
    # 查询数据库获取所有博文
    bbs_list = models.BBS.objects.all()
    # cate = models.Category.objects.get(id='2')
    bbs_categorys = models.Category.objects.all()  # 查询板块数据让前台显示
    # for item in bbs_categorys:
    #     print(item.objects.)
    # print('********************', bbs_categorys)
    # print('////////////////',cate)
    return render(request,'index.html',context={'bbs_list':bbs_list,'user':request.user,'bbs_category':bbs_categorys})
# 用户认证
@csrf_exempt
def acc_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username = username,password=password)
    print(username,password)
    if user is not None:
        auth.login(request,user)# 在 login 中注册cookis
        content = '''
        Welcome %s !!!
        <a href='/logout/' >Logout</a>        
        '''% user.username
        return redirect('/')
    else:
        return render(request,'login.html',context={'login_err':'用户名或者密码错误'})
def logout_view(request):

    user = request.user
    auth.logout(request)
    return redirect('/')
def login(request):
    bbs_categorys = models.Category.objects.all()
    return render(request,'login.html',context={'bbs_category':bbs_categorys})
def acc_reg(request):
    form = AuthRegisterForm(request.POST)
    username = request.POST.get('username')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    msg = ''
    if form.is_valid():
        obj = None
        try:
            obj = User.objects.get(username=username)
        except:
            pass
        if obj != None:
            msg = '用户名重复'
        elif password != password2:
            msg = '密码不一致'
        else:
            msg = '注册成功'
            user =  User.objects.create_user(username,'',password)
            models.BBS_user.objects.create(user=user)
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
        return render(request, 'register.html', context={'form': form,'msg':msg})
    else:
        return render(request, 'register.html', context={'form': form })
# 注册
def register(request):
    bbs_categorys = models.Category.objects.all()
    form = AuthRegisterForm()
    return render(request, 'register.html', context={'form': form,'bbs_category':bbs_categorys})
def updatepassword(request):
    # img = Image.open('../upload_imgs/user-1.jpg')
    # img=Image.open('upload_imgs/user-1.jpg')
    # img.show()
    return HttpResponse('OK')
# 个人信息修改
@csrf_exempt
def accounts_profile(request):
    if request.method == 'POST':
        user=request.user
        bbs_user = models.BBS_user.objects.get(user=user)
        # str2 = str(request.body, errors='ignore')
        # test = json.loads(str2)
        # print(request.POST.get('username'))
        # print(request.POST.get('file'),'--->',file)
        file = request.FILES.get('file')
        print(str(file),'--->',type(file))
        if file:
            old_name = bbs_user.photo.name
            # print(old_name)
            #  删除原文件
            if old_name != 'default.jpg':
                # print('delete!!!')
                try:
                    os.remove('upload_imgs/'+old_name)
                except:
                    pass
            # 放入新文件
            bbs_user.photo = file
            new_name = bbs_user.photo.name
            ext =  new_name.split('.')[-1]
            # print('ext:',ext) 查看图片格式
            # print('->>>>>>>',bbs_user.photo.name,ext)
            new_name = 'user-{}.{}'.format(bbs_user.id, ext)
            # print(new_name)
            # 更新新文件名
            bbs_user.photo.name = new_name
        else:
            try:
                pass
                # 更新文件 avator里要更新
                # os.remove('upload_imgs/avator/FlowerPS4.jpg') 删除文件
                # img = img=Image.open('upload_imgs/user-1.jpg')
                # img.show()
            except:
                print('err')

        #     os.remove('upload_imgs/avator/FlowerPS4.jpg')
        bbs_user.signature=request.POST.get('signature')
        bbs_user.save()
        username = user.username
        password = request.POST.get('password')
        if password =='null':
            pass
        else:
            user.set_password(password)
            user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
        # print('PSW-->',password,type(password))

        # if password!='':
        #     user.set_password(password)
        #     user.save()
        #     user = auth.authenticate(username=username, password=password)
        #     auth.login(request, user)
        # print('-------------->',bbs_user)
        # bbs_user.photo = test['signature']
        # bbs_user.signature = test['signature']
        # bbs_user.save()
    bbs_user = models.BBS_user.objects.get(user=request.user)
    bbs_category = models.Category.objects.all()
    return render(request, 'accounts_profile.html', context={'bbs_user': bbs_user, 'user': request.user,'bbs_category':bbs_category})

# showbloags 全部 将bbs_all 传给index
def category(request,cate_id,pagenum):
    # 查询数据库获取所有博文
    if cate_id == '0':
        bbs_list =  models.BBS.objects.all().order_by('-create_at')
        cate_name = '全部板块'
    else :
        bbs_list = models.BBS.objects.filter(category_id=cate_id).order_by('-create_at')  # 从BBS获取id为X的板块的所有帖子
        cate_name = models.Category.objects.get(pk=cate_id).name
    # 构建分页器对象,blogs=所有博文,2=每页显示的个数
    paginator = Paginator(bbs_list, 10)
    # 获取第n页的页面对象
    page = paginator.page(pagenum)
    # 传递的数据
    bbs_categorys = models.Category.objects.all()  # 查询板块数据让前台显示
    data = {
        # 当前页的博文对象列表
        'page': page,
        # 分页页码范围
        'pagerange': paginator.page_range,
        # 当前页的页码
        'currentpage': page.number,
        'bbs_list': bbs_list,
        'user': request.user,
        'bbs_category': bbs_categorys,
        'cate_id': int(cate_id),
        'cate_name':cate_name,
    }
    return render(request,'category.html',context=data)
# Create your views here.
def bbs_detail(request,bbs_id,pagenum):
    bbs_categorys = models.Category.objects.all()  # 查询数据让前台显示
    bbs_obj = models.BBS.objects.get(pk=bbs_id)
    try:
        bbs_user = models.BBS_user.objects.get(user=request.user)
    except:
        bbs_user=None
    comment_list = Comment.objects.filter(object_pk=bbs_id).order_by('-submit_date')

    # 分页显示
    # 构建分页器对象,blogs=所有博文,2=每页显示的个数
    paginator = Paginator(comment_list, 2)
    # 获取第n页的页面对象
    page = paginator.page(pagenum)
    data = {
        # 当前页的博文对象列表
        'page': page,
        # 分页页码范围
        'pagerange': paginator.page_range,
        # 当前页的页码
        'currentpage': page.number,
        'comment_list': comment_list,
        'user': request.user,
        'bbs_category': bbs_categorys,
        'bbs_user': bbs_user,
        'bbs_obj': bbs_obj,
    }

    # print('---->',comment_list)
    # for item in comment_list:
    #     print(item.comment,item.submit_date)
    # bbs_obj.view_count+=1 实际情况 根据IP 存储到数据库 查询 该IP是否已访问
    bbs_obj.save()
    return render(request,'bbs_detail.html',context=data)
    # return render(request,'bbs_detail.html',context={'bbs_obj':bbs_obj,'bbs_user':bbs_user,'user':request.user,
    #                                                  'bbs_category':bbs_categorys,'comment_list':comment_list})# user变量 'cate_id':int(cate_id),
def edit_bbs_detail(request):
    # 接收bbs_obj
    # cate_id = request.POST.get('cate_id')
    bbs_id = request.POST.get('bbs_id')
    bbs_obj = models.BBS.objects.get(pk=bbs_id)
    return render(request, 'edit_bbs_detail.html', context={'bbs_obj': bbs_obj})
    #return HttpResponse('这是修改内容页面')# +bbs_obj.content
# 修改数据存储接口
def update_bbs_detail(request):
    bbs_id = request.POST.get('bbs_id')
    bbs_obj = models.BBS.objects.get(pk=bbs_id)
    new_content = request.POST.get('content')
    new_title = request.POST.get('title')
    bbs_obj.content = new_content
    bbs_obj.title = new_title
    bbs_obj.update_at = timezone.now()
    bbs_obj.save()
    return redirect('/category/%s/1' % (bbs_obj.category_id))
def sub_comment(request):# 添加评论
    print(request.POST)
    # 获取帖子 id
    bbs_id = request.POST.get('bbs_id')
    # cate_id = request.POST.get('cate_id')
    # print('-------------=',cate_id)
    # 获取内容
    comment = request.POST.get('comment_content')
    Comment.objects.create(
        content_type_id=7,
        object_pk=bbs_id,
        site_id=1,
        user=request.user,
        comment=comment,
    )
    return redirect('/detail/%s/1' %(bbs_id) )#redirect('/category/%s/detail/%s/' %(cate_id,bbs_id) )

@csrf_exempt
def bbs_sub(request,cate_id):# 发帖后数据存储接口
    # print('----------!!!!!!!!!!!',cate_id)
    # print( request.POST.get('content'))
    # print(request.user) #xie
    content = request.POST.get('content')
    title = request.POST.get('title')
    # print('---------------+',content,type(content))
    pat = re.compile('>(.*?)<')
    ''.join(pat.findall(content))
    # print('----------->',cut_str,type(cut_str))
    summary=''.join(pat.findall(content))
    # print('----------!!',summary)
    if len(summary)>20:
        summary=summary[0:20]+'...'
    else:
        summary=summary
    author = models.BBS_user.objects.get(user__username=request.user)# 获取当前登录用户
    cate = models.Category.objects.get(id=str(cate_id))# 获取当前板块
    models.BBS.objects.create(
        title=title,
    # 'TEST TITLE',
        category=cate,
        summary = summary,
        # 'HAHA',
        content = content,
        author=author,
        view_count=1,
        ranking=1,
    )
    # return redirect('/category/%s/detail/%s/' % (cate_id, bbs_id))
    return redirect('/category/%s/1' %(cate_id))

def bbs_pub(request):# 发帖
    bbs_categorys = models.Category.objects.all()  # 查询数据让前台显示
    return render(request,'bbs_pub.html',context={'user':request.user,'bbs_category':bbs_categorys,'cate_id':0})

# 查看用户信息
def userinfo(request,userid):
    bbs_user = models.BBS_user.objects.get(id = userid)
    bbs_categorys = models.Category.objects.all()
    return render(request,'userinfo.html',context={'bbs_user':bbs_user,'user':request.user,'bbs_category':bbs_categorys,})

# 搜索关键字
def search_bbs(request):
    bbs_categorys = models.Category.objects.all()
    return render(request, 'search.html',
                  context={'user': request.user, 'bbs_category': bbs_categorys,'page':'search'})
def search_res(request,pagenum):
    bbs_categorys = models.Category.objects.all()
    if request.method=='POST':
        Type = request.POST.get('search_type')
        # print('=====>',Type)
        info = request.POST.get('search_info')
        if Type == '帖子':
            bbs_list = models.BBS.objects.filter(title__contains=info).order_by('-create_at')
        elif Type =='用户名':
            bbs_list = models.BBS.objects.filter(author__user__username=info).order_by('-create_at')
        # print(bbs_list)
        if bbs_list :
            # 构建分页器对象,blogs=所有博文,2=每页显示的个数
            paginator = Paginator(bbs_list, 10)
            # 获取第n页的页面对象
            page = paginator.page(pagenum)
            # 传递的数据
            bbs_categorys = models.Category.objects.all()  # 查询板块数据让前台显示
            data = {
                # 当前页的博文对象列表
                'page': page,
                # 分页页码范围
                'pagerange': paginator.page_range,
                # 当前页的页码
                'currentpage': page.number,
                'bbs_list': bbs_list,
                'user': request.user,
                'bbs_category': bbs_categorys,
            }
            return  render(request, 'search.html',
                  context=data)
        else:
            # print('NONE',bbs_list,type(bbs_list))
            return render(request, 'search.html',
                   context={'user': request.user, 'bbs_category': bbs_categorys, 'page': 'search', 'msg': '没有找到相关内容'})
