import pymysql
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from mmorder import sinaweibopy3
from mmorder.models import FoodsType, Foods, Cart, Order, Orderdetail, Knowledge
from mmorder.utils.serializers import KnowledgeSerializers
from mmorder.views_constant import ORDER_STATUS_NOT_PAY, ORDER_STATUS_NOT_SEND


# 跳转到商品页面
from myjob.dao.connet2mysql_view import connect2mysql


def shop(request):
    return redirect(reverse('mm_order:shop_message', kwargs={"typeid": 3}))


# 详细商品
def shop_message(request, typeid):
    foodtypes = FoodsType.objects.all()
    foodtype = FoodsType.objects.get(pk=typeid)
    foods_list = Foods.objects.filter(fcategory=foodtype.typename)
    for foods in foods_list:
        carts = Cart.objects.filter(foods=foods)
        if carts.exists():
            cart = carts.first()
            foods.cart_food_num = cart.cart_foods_num
    data = {
        'foodtypes': foodtypes,
        'foods_list': foods_list
    }
    return render(request, 'shop.html', data)


# 跳转到购物车
def go_cart(request):
    carts = Cart.objects.filter(user=request.user)
    data = {
        "carts": carts,
        "total_price": total_price(carts)
    }
    return render(request, 'cart.html', data)


# 添加到购物车
def add_to_cart(request):
    foodsid = request.GET.get("foodsid")
    foods = Foods.objects.filter(fid=foodsid).first()
    carts = Cart.objects.filter(user=request.user).filter(foods_id=foodsid)
    if carts:
        cart = carts.first()
        cart.cart_foods_num = cart.cart_foods_num + 1
    else:
        cart = Cart()
        cart.user = request.user
        cart.foods = foods
        cart.cart_foods_num = 1

    cart.save()
    data = {
        "cart_foods_num": cart.cart_foods_num
    }
    return JsonResponse(data)


# 购物车减去商品
def sub_from_cart(request):
    foodsid = request.GET.get("foodsid")

    carts = Cart.objects.filter(user=request.user).filter(foods=foodsid)
    cart = carts.first()

    data = {}

    if cart.cart_foods_num > 1:
        cart.cart_foods_num = cart.cart_foods_num - 1
        cart.save()
        data["cart_foods_num"] = cart.cart_foods_num
    else:
        cart.delete()
        data["cart_foods_num"] = 0

    return JsonResponse(data)


# 在购物车页面点击加号
def add_shopping(request):
    cartid = request.GET.get("cartid")
    cart = Cart.objects.get(pk=cartid)
    cart.cart_foods_num = cart.cart_foods_num + 1
    cart.save()

    user_id = request.session.get("user_id")
    user = User.objects.get(pk=user_id)
    carts = Cart.objects.filter(user=user)
    totalprice = total_price(carts)

    data = {
        "total_price": totalprice,
        "cart_foods_num": cart.cart_foods_num,
        'status': 200
    }

    return JsonResponse(data)


# 购物车点击减号
def sub_shopping(request):
    cartid = request.GET.get("cartid")
    cart = Cart.objects.get(pk=cartid)
    cart.cart_foods_num = cart.cart_foods_num-1
    cart.save()

    if cart.cart_foods_num == 0:
        cart.delete()

    user_id = request.session.get("user_id")
    user = User.objects.get(pk=user_id)
    carts = Cart.objects.filter(user=user)
    totalprice = total_price(carts)
    data = {
        "total_price": totalprice,
        "cart_foods_num": cart.cart_foods_num,
        'status': 200,
    }

    return JsonResponse(data)


# 在购物车页面点击全选
def cart_all_select(request):
    unselected = request.GET.get("cart_list")

    if unselected:
        unselected_list = unselected.split('#')
        for cartid in unselected_list:
            cart = Cart.objects.get(pk=cartid)
            cart.is_selected = True
            cart.save()

    user_id = request.session.get("user_id")
    user = User.objects.get(pk=user_id)
    carts = Cart.objects.filter(user=user)
    totalprice = total_price(carts)

    data = {
        "total_price": totalprice,
        'status': 200,
    }
    return JsonResponse(data)


# 在购物车页面点击购物车条目的选中状态
def change_cart_state(request):
    cartid = request.GET.get("cartid")
    cart = Cart.objects.get(pk=cartid)
    cart.is_selected = not cart.is_selected
    cart.save()

    carts = Cart.objects.filter(user=request.user)
    is_all_select = True
    for cart in carts:
        if not cart.is_selected:
            is_all_select = False
            break

    data = {
        "cart_is_select": cart.is_selected,
        "total_price": total_price(carts),
        "is_all_select": is_all_select,
        'status': 200,
    }

    return JsonResponse(data)


# 下单
def make_order(request):
    order = Order()
    order.user = request.user
    carts = Cart.objects.filter(user=request.user).filter(is_selected=True)
    order.price = total_price(carts)
    order.save()

    for cart in carts:
        orderdetail = Orderdetail()
        orderdetail.order = order
        orderdetail.foods = cart.foods
        orderdetail.order_foods_num = cart.cart_foods_num
        orderdetail.save()
        cart.delete()

    data = {
        'order_id': order.id,
        'status': 200,
    }
    return JsonResponse(data)


# 计算商品总价
def total_price(carts):
    total = 0.0
    for cart in carts:
        if cart.is_selected:   # 判断该记录是否被选中
            total += cart.foods.fprice * cart.cart_foods_num

    return "{:.2f}".format(total)


# 显示订单详情页面
def order_detail(request):
    orderid = request.GET.get("orderid")
    order = Order.objects.get(pk=orderid)
    data = {
        'orders': order,
        'status': 200,
    }

    return render(request, 'order_detail.html', data)


def order_not_pay(request):
    user = request.user
    orders = Order.objects.filter(user=user).filter(state=ORDER_STATUS_NOT_PAY)
    data = {
        'orders': orders,
        'status': 200
    }

    return render(request, 'order_list_not_pay.html', data)


def pay(request):
    orderid = request.GET.get('orderid')
    order = Order.objects.get(pk=orderid)
    order.state = ORDER_STATUS_NOT_SEND
    order.save()
    data = {
        'status': 200,
        'orderprice': order.price,
    }
    return JsonResponse(data)


def mine(request):
    print("**********")
    user_id = request.session.get('user_id')
    print(user_id, "******2******")
    data = {
        "is_login": False
    }
    if user_id:
        user = User.objects.get(pk=user_id)
        data["is_login"] = True
        data["username"] = user.username
        print(data, "**********")
    return render(request, 'mine.html', data)


#  注册
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        # icon = request.FILES.get("icon")
        if not all([username]):
            message = '用户名不能为空'
            return render(request, 'register.html', locals())
        name_1 = User.objects.filter(username=username)
        if name_1:  # 用户名唯一
            message = '用户名存在'
            return render(request, 'register.html', locals())
        if not all([email]):
            message = '邮箱不能为空'
            return render(request, 'register.html', locals())
        email_1 = User.objects.filter(email=email)
        if email_1:
            message = '邮箱存在'
            return render(request, 'register.html', locals())
        if not all([password]):
            message = '密码不能为空'
            return render(request, 'register.html', locals())
        User.objects.create_user(username, email, password)
        return render(request, 'login.html')


#  登录
def login(request):
    if request.method == "GET":
        # error_message =request.session.get("error_message")
        # if error_message:
        #     del request.session["error_message"]
        return render(request, 'login.html')
    elif request.method == "POST":
        errors = {'msg': ''}
        username = request.POST.get("username")
        password = request.POST.get("password")
        valid_code = request.POST.get("valid_code")  # 填写验证码
        queryset = User.objects.filter(username=username)
        if not queryset.exists():
            errors['msg'] = '%s 用户不存在，请先注册!' % username
        else:
            user = queryset.first()
            print(user.id, "*****3*****")
            # 验证口令
            if check_password(password, user.password):
                # 将登录后的信息存入到session中
                # request.session['login_user'] = {
                #     'id': user.id,
                #     'username': user.username,
                # }
                request.session["user_id"] = user.id
                return redirect(reverse('mm_order:mine'))
            else:
                errors['msg'] = '登录口令不正确！'
    return render(request, 'login.html', locals())


def louout(request):
    request.session.flush()
    return redirect(reverse("mm_order:mine"))


import webbrowser

from django.shortcuts import redirect
from django.urls import reverse


def useWeibologin(request):
    try:
        APP_KEY = '2217088527'
        APP_SECRET = '471878a0a07ccc5f8585c41217c58d1d'
        REDIRECT_URL = 'http://127.0.0.1:8000/mm_order/mine'  # 重定向到自己的网页

        # step 2 : get authorize url and code
        client = sinaweibopy3.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=REDIRECT_URL)
        url = client.get_authorize_url()
        webbrowser.open_new(url)
        # step 3 : get Access Token

        result = client.request_access_token(
            input("please input code : "))  # Enter the CODE obtained in the authorized address

        client.set_access_token(result['access_token'], result['expires_in'])

        print(client.get.account__get_uid())

        user = client.user_show(result['uid'])
        print(user.cover_image_phone)
        print("***"*8)
        print(user.name)

    except ValueError:
        print('pyOauth2Error')
    return render(request,'mine.html',{'is_login':True,'username':user.name})

class MyPageNumberPagination(PageNumberPagination):
    page_size = 2  #默认每页的条目数
    # max_page_size = 5
    page_size_query_param = 'size'
    page_query_param = 'page'




# page_size=3  # 每页最多显示的条数
class ShowAnecdote(APIView):

    def get(self,request):
        anecdotes=Knowledge.objects.get_queryset()
        page=MyPageNumberPagination()
        page_roles=page.paginate_queryset(queryset=anecdotes,request=request,view=self)
        roles_ser=KnowledgeSerializers(instance=page_roles,many=True)
        return Response(roles_ser.data,status=status.HTTP_200_OK)

    def post(self,request):
        sers = KnowledgeSerializers(data=request.data)  # 将post请求数据封装到序列化对象中
        if sers.is_valid():
            sers.save()
            return Response(sers.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)





def showranking(request):
    return render(request, 'ranking_bar.html')




def my_echart(request):
    items = connect2mysql()

    jsonData = {}
    xfname = [item[0] for item in items]
    yfpopnum = [item[1]//100 for item in items]  # 人气数字过大,减少一些数字显示

    jsonData['xfname'] = xfname
    jsonData['yfpopnum'] = yfpopnum
    return JsonResponse(jsonData)  # 转化成json格式数据



