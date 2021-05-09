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
    path('/editprofile',views.edit_profile,name='edit_profile'),
    path('/viewprofile',views.view_profile,name='view_profile'),
    path('/view_feedback',views.view_feedback,name='view_feedback'),
    path('/menu',views.menu,name='menu'),
    path('/changedish/<int:pk>',views.edit_dish,name='edit_dish'),
    path('/ajax_validate_username',views.validate_username,name='validate_username'),
    path('ajax/change_waiter_alert',views.change_waiter_alert,name='change_waiter_alert'),
    path('ajax_delete_reservation',views.ajax_delete_reservation,name='delete_reservation')
]

