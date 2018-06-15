# coding:utf-8
from django.shortcuts import render,redirect
from hashlib import sha1
from .models import *
from django.http import *
from django.template import RequestContext, loader

# 所有的url是按着寻找路径来做.render是链接文件位置。redirect是重新对url进行定向。

# 注册页面
def register(request):
    context = {'title':'注册'}
    return render(request,'df_user/register.html',context)

# ajax检测填写的用户名是否存在
def check_uname(request):
    # 利用ajax在接收数据之前，进行判定用户名是否存在
    uname = request.GET.get('uname')
    # print(uname)
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

# 注册数据接受处理
def register_handle(request):
    # 接受注册数据(统一设置密码为用户名加上‘123456’，邮箱为 ‘用户名@163.com’ ，方便查阅)
    uname = request.POST['user_name']
    upwd = request.POST['pwd']
    upwd2 = request.POST['cpwd']
    uemail = request.POST['email']
    # 验证输入的密码是否相等
    if upwd != upwd2:
        return redirect('/user/register/')   # 不相等，直接返回注册页面，重新注册。
    # 密码匹配，进行密码的加密
    m = sha1()
    m.update(upwd)  # 注意是变量还是字符串
    upwd3 = m.hexdigest()
    # 数据写入数据库
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    # return HttpResponse('恭喜,注册成功！')
    return redirect('/user/login/')

# 登陆界面
def login(request):
    uname = ''
    if request.COOKIES.has_key('uname'):
        uname = request.COOKIES['uname']
    context = {'title':'登录','uname':uname}
    return render(request,'df_user/login.html',context)
# 验证登录信息是否正确
def login_handle(request):
    uname = request.POST['uname']
    upwd = request.POST['upwd']
    print('name=%s , pwd=%s' % (uname, upwd))
    # 得到database中用户数据
    # try:
    #     user = UserInfo.objects.get(uname=uname)
    # except DoesNotExist:
    #     print('不存在这个用户名')
    # except MultipleObjectsReturned:
    #     print('这个用户名存在多个')
    count = UserInfo.objects.filter(uname=uname).count()  # filter若获取不到为空[]
    # print('过滤到的名字的数量：',count)
    if count == 0:
        print('不存在传来的uname！')
        return JsonResponse({'uname_num': '0'})  # 0代表用户名不存在
    user = UserInfo.objects.get(uname=uname)  # 上边已经确定存在，这里直接获取就行。
    upwd1 = user.upwd
    # 对得到的用户密码进行sha1加密，并与upwd1进行对比
    m = sha1()
    m.update(upwd)  # 注意是变量还是字符串
    upwd2 = m.hexdigest()
    if upwd2 != upwd1:
        print('用户名正确，但是密码错误！')
        return JsonResponse({'pwd_num': '0'})  # 0代表密码错误
    else:
        print('登陆成功！')
        # print('%s登陆成功...' % test)   # 不知道为什么这里放了这个语句，就总是报错！！！！
        # 这里不能再次获取通过ajax传送过来的数据
        return JsonResponse({'pwd_num': '1'})
# 通过验证,直接提交数据,进行处理。
def login_handle_2(request):
    uname = request.POST['username']
    # upwd = request.POST['pwd'] #已经验证通过，密码可以不用再占用空间进行缓存了。
    remember = request.POST.get('remember',0)  # 第二个参数为设置默认值，不设置的话等同于POST['rember']
    # print('rember=',remember)
    user = UserInfo.objects.get(uname=uname)
    uemail = user.uemail
    ucustomer = user.ucustomer
    context1 = {'loadin': 1, 'uname': uname, 'uemail': uemail, 'ucustomer': ucustomer}
    t1 = loader.get_template('df_user/user_center_info.html')
    context2 = RequestContext(request, context1)
    response = HttpResponse(t1.render(context2))
    # 根据rember的值，进行判定是否要设置cookie进行自动填充
    # 传过来为1，那么设置cookie记住用户名。这里只负责设置，提取在登陆界面时进行使用。
    # response = HttpResponse()
    if remember == u'1':
        print('更新cookie...')
        response.set_cookie('uname',uname)
    # else:     # 若是不勾选应该不从操作，不改变、也不参与cookie的内容。
    #     print('删除刚登陆用户的cookie...')
    #     response.delete_cookie('uname')
    return response
    # return render(request,'df_user/user_center_info.html',context)




# 用户中心界面（三合一）====================================只有第一页info显示是正常的
def user_center_info(request):  # 默认界面-用户中心-个人信息
    context = {'title':'用户中心','loadin':0}
    return render(request,'df_user/user_center_info.html',context)

def user_center_order(request):    # 用户中心-全部订单
    context = {'title':'用户中心','loadin':0}
    return render(request,'df_user/user_center_order.html',context)

def user_center_site(request):      # 用户中心-收货地址
    context = {'title':'用户中心','loadin':0}
    return render(request,'df_user/user_center_site.html',context)
def user_center_site_handle(request):
    pass
