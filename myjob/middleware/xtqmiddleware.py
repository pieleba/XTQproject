from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

LOGIN_REQUIRED_JSON = ["/mm_order/addtocart/","/mm_order/subfromcart/","/mm_order/makeorder/","/mm_order/changecartstate/","/mm_order/payed/"]

LOGIN_REQUIRED = ["/mm_order/cart/","/mm_order/orderdetail/","/mm_order/ordernotpay/"]


class LoginMiddleware(MiddlewareMixin):

    def process_request(self,request):
        if request.path in LOGIN_REQUIRED_JSON:
            user_id = request.session.get("user_id")
            if user_id:
                user = User.objects.get(pk=user_id)
                request.user = user
            else:
                data = {
                    "status": 302,
                }
                request.session["error_message"] = "您还未登录，请先登录！"
                return JsonResponse(data)


        if request.path in LOGIN_REQUIRED:
            user_id = request.session.get("user_id")
            if user_id:  # 如果已经登录
                user = User.objects.get(pk=user_id)
                request.user = user  # 给request对象动态添加一个user属性
            else:  # 未登录
                request.session["error_message"] = "您还未登录，请先登录！"
                return redirect(reverse("mm_order:log"))