from django.urls import path
from . import views
app_name="hoteladmin"
urlpatterns = [
    path("/",views.index,name="index"),
    path("/login",views.view_login,name="login"),
    path("/register",views.register,name='register'),
    path("/orders",views.view_orders,name='orders'),
    path("/orders/<str:order_no>",views.expand_order,name='expandorder'),
    path("/logout",views.logout_view,name='logout'),
    path('/ajax/change_payment_status',views.change_payment_status,name='change_payment_status'),
    path('/reservations',views.view_reservations,name='reservations'),
    path('ajax/change_waiter_alert',views.change_waiter_alert,name='change_waiter_alert')
]

