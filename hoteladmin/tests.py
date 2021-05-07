from django.test import TestCase
from .models import *
# Create your tests here.

# Create your tests here.
class TestOrderCase(TestCase):
    def setUp(self):
        #Create some test data
        user=User.objects.create(username='test',password='test')
        Order.objects.create(order_no='ORD1',user=user,table_no=2)
        Order.objects.create(order_no='ORD2',user=user,table_no=3)
        Order.objects.create(order_no='ORD3',user=user,table_no=4)
    def test_is_equal(self):
        '''Checking whether the no of user orders match '''
        user=User.objects.get(username='test')
        self.assertEqual(user.orders.count(),3)