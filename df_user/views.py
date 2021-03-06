# coding:utf-8
from django.shortcuts import render,redirect
from hashlib import sha1
from .models import *
from django.http import *
from df_order.models import *
from df_goods.models import *
# from django.template import RequestContext, loader
from df_user import user_decorator # 登陆装饰器
# sys.path.append('..')
from df_goods.models import *
from django.core.paginator import *
import re


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
    # print('path：',request.path)
    # print('fullpath：',request.get_full_path())
    uname = ''
    if request.COOKIES.has_key('uname'):
        uname = request.COOKIES['uname']
    # uname = request.COOKIES.get('uname','')  # 上边可用一句话代替，第二个参数为默认值
    context1 = {'title':'登录','uname':uname}
    # t1 = loader.get_template('df_user/login.html')
    # context2 = RequestContext(request,context1)
    # resp = HttpResponse(t1.render(context2))
    # resp.set_cookie('url2',request.get_full_path())
    # return resp
    return render(request,'df_user/login.html',context1)

'''
# ajax+form框的验证方式
# 验证登录信息是否正确(通过ajax),返回json值，让form进行提交
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
    # 设置session用于状态保持，只要页面没有关，都可以通过其查找对应的数据.数据是存储在
    print('存储会话session...')
    request.session['user_id'] = user.id
    request.session['user_name'] = uname    # 可写可不行，可直接由id得到，但是使用量大，可以先获得，缓存起来。
    request.session.set_expiry(0)  # 设置会话过期时间,0为浏览器关闭后清除

    url = request.COOKIES.get('url','/')  # 得到存储的链接cookie，有返回原链接，没有回首页。

    resp = HttpResponseRedirect(url)   # 要反向的地址，这里先做定义，还未return
    # 根据rember的值，进行判定是否要设置cookie进行自动填充
    # 传过来为1，那么设置cookie记住用户名。这里只负责设置，提取在登陆界面时进行使用。
    if remember == u'1':
        print('更新cookie...')
        resp.set_cookie('uname',uname)
    return resp
'''

# 利用ajax加上前端页面跳转，进行实现。
def login_handle_3(request):
    uname = request.POST['uname']
    upwd = request.POST['upwd']
    remember = request.POST.get('remember',0)  # 第二个参数为设置默认值，不设置的话等同于POST['rember']
    url = request.COOKIES.get('url','/')  # 得到存储的链接cookie，有返回原链接，没有回首页。
    print('name=%s , pwd=%s' % (uname, upwd))

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
        resp = JsonResponse({'pwd_num': '1','url':url})
        request.session['user_id'] = user.id
        request.session['user_name'] = uname  # 可写可不行，可直接由id得到，但是使用量大，可以先获得，缓存起来。
        request.session.set_expiry(0)  # 设置会话过期时间,0为浏览器关闭后清除
        if remember == u'1':
            print('更新cookie、设置session...')
            resp.set_cookie('uname', uname)
        else:
            resp.delete_cookie('uname') # 有删除；没有的话，什么也不发生。
        return resp



# 用户中心界面（三合一）=================================
@user_decorator.login
def user_center_info(request):  # 默认界面-用户中心-个人信息
    # 防止直接链接的访问。还可以添加登陆的选项
    # try:
    #     user_id = request.session['user_id']
    # except KeyError:
    #     print('user_id不存在，转向登陆界面...')
    #     return redirect('/user/login/')
    user_id = request.session['user_id']
    uname = request.session.get('user_name')
    user = UserInfo.objects.get(id=user_id)

    # 得到浏览记录的cookie,进行界面数据的更新。
    goods_ids = request.COOKIES.get('goods_ids','')
    goods = []
    if goods_ids != '':
        goods_ids2 = goods_ids.split(',')  # 字符串分割为列表
        print('goods_history',goods_ids2)   # 浏览过的商品id
        for i in goods_ids2:
            num_id = int(i)
            goods.append(GoodsInfo.objects.filter(id=num_id)[0])  # filter得到的就是一个列表，为了提取到数据，把元素取出来，放在统一的列表中。
        # print('goodsinfo',goods)  # 得到的数据列表

    context = {
        'title': '用户中心',
        'loadin': 1,
        'uname':uname,
        'user': user,
        'goods':goods,  # 浏览商品的记录
    }

    return render(request,'df_user/user_center_info.html',context)

 # 用户中心-全部订单
@user_decorator.login
def user_center_order(request,pIndex):  # pIndex为页码指针
    if pIndex == '':  # 不写页码，默认第一页
        pIndex = 1
    user_id = request.session['user_id']
    uname = request.session.get('user_name')
    user = UserInfo.objects.get(id = user_id)
    order_list = user.orderinfo_set.all() # 根据用户得到所有的订单信息，再由订单信息得到具体的订单详情
    # order_list2 = order_list[::-1]  # 反过来排序，最新的数据在第一页。(默认按得oid排序)
    order_list3 = order_list.order_by('-otime')  # 按订单的时间倒序
    # detail = order_list[0].orderdetailinfo_set.all()  #根据外键归类的查询方法。
    # print(detail[0].goods.gprice)
    # 数据展示实现分页
    p = Paginator(order_list3,2) # 一页展示两个订单，根据这个进行分页
    page = p.page(int(pIndex))  # 点击页码的数据


    context = {
        'title':'用户中心',
        'loadin':1,
        'uname':uname,
        'user':user,
        'p':p,
        'page':page,
    }
    return render(request,'df_user/user_center_order.html',context)

# 用户中心-收货地址
@user_decorator.login
def user_center_site(request):
    user_id = request.session['user_id']
    uname = request.session.get('user_name')
    user = UserInfo.objects.get(id = user_id)
    if request.method == 'POST':
        user.ucustomer = request.POST['ucustomer']   # name为键，value为值
        user.uaddr = request.POST['uaddr']
        user.uzipcode = request.POST['uzipcode']
        user.uphone = request.POST['uphone']
        user.save()
        url = request.COOKIES.get('url', '')  # 判断是不是订单页跳转的，是？跳回去；不是?刷新页面。
        if re.match('/order/place_order/', url).group() != None:
            return HttpResponseRedirect(url)
    context = {
        'title':'用户中心',
        'loadin':1,
        'uname':uname,
        'user':user,
    }

    return render(request,'df_user/user_center_site.html',context)

# 退出登陆
def login_out(request):
    # 点击退出后，删除session
    # del request.session['user_id']  # 删除服务器存储的会话
    # del request.session['user_name']  # 这个为了安全照相，
    # 以上两句可以直接用flush删除就行，并没有需要保存的会话数据，uname的cookie是登陆界面存的，更会话没有关系。
    request.session.flush()  #删除当前的会话数据并删除会话的Cookie

    res = HttpResponseRedirect('/')
    res.delete_cookie('url')    # 删除存储在客户端的url的cookie
    res.delete_cookie('goods_ids')
    return res