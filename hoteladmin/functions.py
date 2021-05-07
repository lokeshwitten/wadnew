from .models import *
def get_number(Global):
    no=Global.objects.get(pk=1)
    number=no.rest_no
    no.rest_no+=1
    no.save()
    return number