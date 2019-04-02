import xadmin
from xadmin import views

from  quan.models import QuanActive
# Register your models here.
class QuanActiveAdmin():
    list_display = ['title',
                    'vulumns',
                    'publish_date',
                    'valid_days']


xadmin.site.register(QuanActive,QuanActiveAdmin)