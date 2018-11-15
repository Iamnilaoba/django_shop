import xadmin
from .models import UserFav

class Userfavadmin(object):

    list_display=['goods','user','id']


xadmin.site.register(UserFav,Userfavadmin)


