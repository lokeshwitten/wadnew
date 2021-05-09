from django.urls import path
from . import views
app_name='user'
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path("/",views.index,name="index"),
    path("/login",views.view_login,name="login"),
    path("/signup",views.signup,name="signup"),
    path("/contact",views.contact,name="contact"),
    path("/test",views.test,name="test"),
    path("/restaurant/<str:rest_id>",views.view_restaurant,name='view_restaurant'),
    path("/booking/",views.booking,name='booking'),
    path("/booking/confirmreservation",views.confirm_res,name='confirmres'),
    path("/qrcode",views.qrcode,name='qrcode'),
    path("/logout",views.logout_view,name='logout'),
   
    path('cart',views.cart,name='cart'),
    path('/orderconf',views.order_conf,name='orderconf'),
    path('rest/',views.rest,name='rest'),
    path('ajax/validate_username',views.validate_username,name='validate_username'),
    path('ajax/validate_table_no',views.validate_table_no,name='validate_table_no'),
    path('order/<str:order_no>',views.view_order,name='view_order'),
    path('/myorders',views.myorders,name='myorders'),
    path('/myreservations',views.myreservations,name='myreservations'),
    path('/reservations/<str:conf_code>',views.view_reservation,name='view_reservation'),
    path('/pastorders',views.view_past_orders,name='past_orders'),
    path('/feedback/<str:order_no>',views.feedback,name='feedback'),
    path('feedback_success',views.feedback_success,name='feedback_success'),
    path('/send_ajax_request_waiter',views.ajax_request_waiter,name='ajax_request_waiter'),
    path('/ajax_request_parcel',views.ajax_request_parcel,name='ajax_request_parcel')

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
