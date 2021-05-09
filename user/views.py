from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.http  import HttpResponseRedirect,HttpResponse,JsonResponse
from django.urls import reverse
# Create your views here.
from hoteladmin.models import *
from .decorators import *
from django.contrib.auth.decorators import login_required

from datetime import datetime
from wad.settings import BASE_DIR


def index(request):
    request.session.set_expiry(0)
    user=request.user
    if  user.groups.filter(name='HotelAdmin').exists():
        return HttpResponseRedirect(reverse('user:login'))
        
    if request.user.is_authenticated:
        username=request.user.username.capitalize()
        return render(request,"user/index.html",{
            "username":username
        })
    else: #Ask the user to login
        return render(request,"user/index.html")

def signup(request):
    if(request.method=="POST"):
        
        #Error messages
        usernameexists="Username already exists.Choose a new username"
        userexists="Account already exists.Please sign in to continue"
        passerror="The passwords don't match.Please enter again"
       
        #POST data
        username=request.POST['username']
        password=request.POST.get('password')
        passverify=request.POST.get('password1')
        email=request.POST.get('email')

        #Checking whether the entered two passwords match
        if password != passverify:
            return render(request,"user/signup.html",{
                "message":passerror
            })
            #Checking if the user is a hoteladmin:
            
        
        #Checking if the username or the user already exists
        allusers=User.objects.all()
        for user in allusers:
            if(user.username==username):
                if(user.email==email):
                    return render(request,"user/signup.html",{
                        "message":userexists
                    })
                
                return render(request,"user/signup.html",{
                    "message":usernameexists
                })
        user=User.objects.create_user(username=username,password=password,email=email)
        user.save()
        userauth=authenticate(username=username,password=password)
        if userauth:
            #Redirect to login view
            return HttpResponseRedirect(reverse('user:login'))
        else:
            return HttpResponse(request,"Cant create user")
    return render(request,"user/signup.html")
def view_login(request):
    if(request.method=="POST"):
        errormessage="Incorrect crendetials or the account doesnt exist"
        passmismatch="Passwords don't match.Please enter again."
        permsenied='Permission Denied'
        username=request.POST['username']
        password=request.POST['password']
       
        user=authenticate(request,username=username,password=password)
        if user.groups.filter(name='HotelAdmin').exists():
            return render(request,"user/login.html",{
                "message":permsenied
            })
        if user is not None:    
            login(request,user)
            #Redirect to index view
            
            return HttpResponseRedirect(reverse('user:index',))

        else:
           return  render(request,"user/login.html",{
               "message":errormessage
           })
    return render(request,"user/login.html")
def contact(request):
    return render(request,"user/contact.html")

#For reserving a table based on time,date and restaurant entered
def booking(request,):
    if request.method=="POST":
        request.session['rests']=request.POST['rest']
        rest_code=request.session['rests']
        restaurant=Restaurant.objects.get(rest_id=rest_code)
        date=request.POST['date']
        time=request.POST['time']
        resdate=datetime.strptime(date,'%Y-%m-%d')
        resdate=resdate.date()
        restime=datetime.strptime(time,'%H:%M')
        restime=restime.time()
        request.session['reserdate']=date
        request.session['resertime']=time
        capacity=get_capacity(restaurant,resdate,restime)
        return render(request,"user/booking.html",{
            "no":capacity,"name":restaurant.name
            
        })
    return HttpResponseRedirect(reverse('user:test'))
def test(request):
    return render(request,"user/test.html",{
        "restaurants":Restaurant.objects.all()
    })
def confirm_res(request):
    if request.method=="POST":
        tables=request.POST['no'] #No of the tables
        name=request.POST['name'] #Name of the customer
        date=request.session['reserdate'] #date of reservation
        time=request.session['resertime'] #Time
        #Coverting strings into time and date objects
        resdate=datetime.strptime(date,'%Y-%m-%d')
        resdate=resdate.date()
        restime=datetime.strptime(time,'%H:%M')
        restime=restime.time()
        
        rest_code=request.session['rests']
        restaurant=Restaurant.objects.get(rest_id=rest_code)
        glob=Global.objects.get(pk=1)
        cnf_code='CNF'+str(glob.cnf_no)
       
        rest_id=request.session['rests']
        reservation=Reservations.objects.create(conf_code=cnf_code,user=request.user,cust_name=name,date=resdate,
        tables=tables,time=restime,restaurant=restaurant)
        if reservation is not None:
            glob.cnf_no +=1
            glob.save()
            set_tableno(reservation)
            return render(request,"user/resconfirm.html",{
                "reservation":reservation
            })
        else:
            return HttpResponse('Reservation cant be made ')
    
    return HttpResponseRedirect(reverse('user:test'))   
    
#@login_required(redirect_field_name='/usertest1',login_url='/user/login')
def view_restaurant(request,rest_id):
    if request.method=="POST":
        orderdata=request.POST['orderdata']
        request.session['cart']=decode(orderdata) #First time the user orders
        return HttpResponseRedirect(reverse('user:orderconf'))
    restaurant=Restaurant.objects.get(rest_id=rest_id)
    request.session['rest']=rest_id
    return render(request,"user/menu.html",{
        "restaurant":restaurant,"dishes":restaurant.dishes.all(),"username":request.user.username
    })
def qrcode(request):
    data=readqr()
    return HttpResponseRedirect(data)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('user:login'))
#Order Confirmation page view based on the items ordered
def order_conf(request):
    
    if request.method=="POST":
        if(order_exists(request.user)):
                ordlatest=latest_order(request.user)
                cartdata=request.session['cart']
                if 'previous_order' not in request.session:
                    request.session['previous_order']=build_previous_order(ordlatest)
                    
                previous_order=request.session['previous_order']
                new_order_data=merge_dict(cartdata,previous_order)
                
                try:
                    create_order_items(ordlatest,new_order_data)
                except:
                    HttpResponseRedirect(reverse('user:index'))
                #Update the previous order
                ordlatest.price=get_order_price(ordlatest)
                ordlatest.avg_time=get_avg_time(ordlatest)
                ordlatest.save()
                request.session['previous_order']=merge_dict(cartdata,previous_order)
                
                
                return HttpResponseRedirect(reverse('user:view_order',args=[ordlatest.order_no]))
                
        else:
            table_no=request.POST['table_no']
            cartdata=request.session['cart']
            order_no=get_order_no()
            rest_code=request.session['rest']
            restaurant=Restaurant.objects.get(rest_id=rest_code)
            date=datetime.today().date()
            time=datetime.now().time()
            ord1=Order.objects.create(order_no=order_no,user=request.user,restaurant=restaurant,date=date,time=time,table_no=table_no)
            if ord1 is not None:
                create_order_items(ord1,cartdata)
                ord1.price=get_order_price(ord1)
                ord1.avg_time=get_avg_time(ord1)
                ord1.save()
                request.session['previous_order']=request.session['cart']
            update_global_order()
            restaurant.orders.add(ord1)
            return HttpResponseRedirect(reverse('user:view_order',args=[ord1.order_no]))
            
    #For 'GET' method of accessing the page
    if 'cart' not in request.session:
        return HttpResponseRedirect(reverse('user:index'))
    #Display Order Confirmation Page
    orderdata=request.session['cart']
    rest_code=request.session['rest']
    items={}
    price=get_price(orderdata)
    for key in orderdata.keys():
        dish=Dish.objects.get(pk=key)
        quantity=orderdata[key]
        items[dish]=quantity
    return render(request,"user/orderconf.html",{
        "dishes":items,"price":price,"code":rest_code
    })
        
#Display Cart Items
def cart(request):
    orderdata=request.session['cart']
    items=[]
    for key in orderdata.keys():
        dish=Dish.objects.get(pk=key)
        quantity=orderdata[key]
        items.append(dish.name+ str(quantity)+ 'X'+ '-' +str(dish.price*quantity) )
    return render(request,"user/cart.html",{
        "items":items
    })
    

def view_order(request,order_no):
    order=Order.objects.get(order_no=order_no)
    rest_code=order.restaurant.rest_id
    
    if(order.bill_status=='PEND'):
        flag=True
    else:
        flag=False
    return render(request,"user/endpage.html",{
        "order":order,"code":rest_code,"flag":flag
    })

def myorders(request):
    user=request.user
    active_orders=user.orders.filter(bill_status='PEND')
    return render(request,"user/myorders.html",{
        "orders":active_orders
    })
def view_past_orders(request):
    orders=Order.objects.filter(bill_status='PD')
    return render(request,"user/pastorders.html",{
        "orders":orders
    })
def myreservations(request):
    user=request.user
    reservations=user.reservations.all()
    return render(request,"user/reservations.html",{
        'reservations':reservations
    })

def view_reservation(request,conf_code):
    reservation=Reservations.objects.get(conf_code=conf_code)
    return render(request,"user/resexpand.html",{
        "reservation":reservation
    })
    
def rest(request):
    restaurants=Restaurant.objects.all()
    return render(request,"user/rest.html",{
        "restaurants":restaurants
    })   
    
#Feedback form

def feedback(request,order_no):
    if request.method =='POST':
        food_rating=request.POST['rate']
        service_rating=request.POST['rate2']
        app_rating=request.POST['rate3']
        app_message=request.POST['app_message']
        service_message=request.POST['service_message']
        food_message=request.POST['food_message']
        order=Order.objects.get(order_no=order_no)
        feedback=Feedback.objects.create(food_message=food_message,food_rating=food_rating,app_message=app_message,app_rating=app_rating,
                                         service_message=service_message,service_rating=service_rating,order=order)
        if feedback is not None:
            return HttpResponseRedirect(reverse('user:feedback_success'))
        else:
            return HttpResponse('FeedBack Cant be sent')
    return render(request,"user/feedback.html",{"order_no":order_no})

def feedback_success(request):
    return render(request,"user/feedback_success.html")
    
    
'''AJAX Validation views'''

#Validate username check if the username already exists. If so send a pop up
def validate_username(request):
    username=request.GET['username']
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

#Check Whether the table no entered is valid or not
def validate_table_no(request):
    table_no=request.GET['table_no']
    rest_code=request.session['rest']
    restaurant=Restaurant.objects.get(rest_id=rest_code)
    max_capacity=restaurant.seating_capacity+restaurant.capacity
    flag=False
    try:
        table_no=int(table_no)
    except:
         data={"is_valid":flag}
         return JsonResponse(data)
    
    if isinstance(table_no,int):
        flag=True
    else:
        data={"is_valid":flag}
        return JsonResponse(data)
    if int(table_no)  > max_capacity:
        flag=False
        data={"is_valid":flag}
        return JsonResponse(data)
    else:
        flag=True
        data={"is_valid":flag}
        return JsonResponse(data)
    
#Request Waiter
def ajax_request_waiter(request):
    order_no=request.GET.get('order_no',None)
    if order_no is None:
        flag=False
        data={"flag":flag}
        return JsonResponse(data)
    else:
        try:
            order=Order.objects.get(order_no=order_no)
            order.waiter_alerted=True
            order.save()
            data={"flag":True}
            return JsonResponse(data)
        except:
            flag=False
            data={"flag":flag}
            return JsonResponse(data)
            
def ajax_request_parcel(request):
    order_no=request.GET.get('order_no',None)
    if order_no is None:
        flag=False
        data={"flag":flag}
        return JsonResponse(data)
    else:
        try:
            order=Order.objects.get(order_no=order_no)
            order.parcel_request=True
            order.save()
            data={"flag":True}
            return JsonResponse(data)
        except:
            flag=False
            data={"flag":flag}
            return JsonResponse(data)
    
 