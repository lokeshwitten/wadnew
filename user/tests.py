from unittest import TestCase
from .decorators import *
from hoteladmin.models import *
from django.contrib.auth.models import User

#Tests for Orders
class TestOrder(TestCase):

    def setUp(self):
        User.objects.create(username='test1',password='test',email='gurorkrupa@gmail.com')
        #Creating Some Dishes
        Dish.objects.create(name='Paneer Butter Masala',price=250)
        Dish.objects.create(name='Paneer Tikka Masala',price=230)
        Dish.objects.create(name='Veg Biryani',price=200)

        pbm=Dish.objects.get(pk=1)
        Item.objects.create(dish=pbm,quantity=2)
        test=User.objects.get(username='test1')
        Order.objects.create(order_no='DEF001',user=test)
        
    def test_order_existing(self):
        '''Tests whether the order_exists functions works properly or not'''
        test=User.objects.get(username='test')
        self.assertFalse(order_exists(test))
