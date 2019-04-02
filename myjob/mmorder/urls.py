from django.urls import path

from mmorder.views import *
from mmorder.api_views import *


app_name = 'mmorder'

urlpatterns = [
    path('log/', login, name='log'),
    path('reg/', register, name='reg'),
    path('mine/', mine, name='mine'),
    path('louout/', louout, name='louout'),
    path('shop/', shop, name='shop'),
    path('shop_message/<typeid>', shop_message, name='shop_message'),
    path('addcart/', add_shopping),
    path('addtocart/',add_to_cart),
    path('subcart/', sub_shopping),
    path('subfromcart/',sub_from_cart),
    path('cart/', go_cart,name='go_cart'),
    path('payed/',pay),
    path('makeorder/',make_order),
    path('orderdetail/',order_detail),
    path('ordernotpay/',order_not_pay,name='ordernotpay'),
    path('changecartstate/',change_cart_state),
    path('allselect/',cart_all_select),
    path('index/', index),
    path('update_order/', update_order),
    path('pay_result/', pay_result),
    path('useWeibologin/',useWeibologin,name='useWeibologin'),

    path('anecdote/', ShowAnecdote.as_view()),
    path('showranking/', showranking, name='rank'),
    path('getData/', my_echart, name='echarts'),
]
