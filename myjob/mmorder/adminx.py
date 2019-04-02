import xadmin
from mmorder.models import Foods
from xadmin import views

class FoodsAdmin():
    list_display = [
        "fname",
        "fcategory",
        "fprice",
    ]

xadmin.site.register(Foods,FoodsAdmin)