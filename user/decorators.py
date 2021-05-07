from hoteladmin.models import *
import qrcode
import cv2

def get_code(Restaurant):
    city=Restaurant.address.city
    street=Restaurant.address.street
    pincode=Restaurant.address.pincode
    name=Restaurant.name
    id=Restaurant.rest_id
    code= name+'-'+street+'-'+city+'-'+str(pincode)+'-'+id
    return code

#Decoding the string and converting it into a dictionary
def decode(string):
    resdict={}
    con=''
    for i in range(len(string)):
        if (string[i]=='+' or string[i]=='-'):
            if(string[i]=='+'):
                if int(con) in resdict:
                    resdict[int(con)]+=1
                    con=''
                else:
                    resdict[int(con)]=1
                    con=''
            if(string[i]=='-'):
                resdict[int(con)]-=1
                con=''
        else:
            if(string[i]=='q'):
                i+=1
            else:
                con+=string[i]
    return resdict



def readqr():
# initalize the cam
    cap = cv2.VideoCapture(0)
    #initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cap.read()
        # detect and decode
        data, bbox, _ = detector.detectAndDecode(img)
        # check if there is a QRCode in the image
        if bbox is not None:
            # display the image with lines
            for i in range(len(bbox)):
                # draw all lines
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
            if data:
                print("[+] QR Code detected, data:", data)
                break
        # display the result
            cv2.imshow("img", img)    
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    return data

'''Universal Functions(Important methods on dicts and lists)'''
def populate(list,no):
    for i in range(1,no+1):
        list.append(i)
def Diff(li1, li2):
    li3=li2
    for i in li1:
        li3.remove(i)
    return li3

def extract_min(l,no):
    list=l
    ret=[]
    for i in range(0,no):
        a=min(list)
        ret.append(a)
        list.remove(a)
    return ret
#Common Keys between Dictionaries
def common(a,b):
    common=[]
    for i in a.keys():
        for j in b.keys():
            if(i==j):
                common.append(i)
    return common
#Merging Two Dictionaries(OrderData(if previous order is present) and Cart Items)
def merge_dict(a,b):
    #Find the common keys
    ret={}
    com=common(a,b)
    for key in com:
        ret[key]=a[key]+b[key]
    
    #Populate the merged dictionary with values that are not common
    for key in a.keys():
        if key not in com:
            ret[key]=a[key]
    for key in b.keys():
        if key not in com:
            ret[key]=b[key]

    return ret


'''Functions for placing Order'''
#Get Order Code
def get_order_no():
    return 'ORD'+str(Global.objects.get(pk=1).order_no)
#Update Global Code
def update_global_order():
    glob=Global.objects.get(pk=1)
    glob.order_no+=1
    glob.save()
#Create Order Items



    
#Checking if the user has an existing order
def order_exists(user):
    orders=user.orders.all()
    latest_order=orders.last()
    if latest_order is None:
        return False
    if(latest_order.bill_status == 'PEND'):
        return True
    else:
        return False
def latest_order(user):
    orders=user.orders.all()
    latest_order=orders.last()
    return latest_order
    

#Get Price of the order from the dictionary
def get_price(dict):
    price=0
    for key in dict.keys():
        quantity=dict[key]
        dish=Dish.objects.get(pk=key)
        price+=int(dish.price*quantity)
    return price

#Get Price of the order from the items
def get_order_price(Order):
    items=Order.items.all()
    price=0
    for item in items:
        price+=item.get_price()
    return price

def create_order_items(Order,dict):
    items=Order.items.all()
    if items.count() == 0:   #This indicates that its the first order by the user
        for key in dict.keys():
            dish=Dish.objects.get(pk=int(key))
            quantity=dict[key]
            item=Item.objects.create(dish=dish,quantity=quantity)
            if item is not None:
                Order.items.add(item)
        Order.save()
    #The user is adding items to his order
    else:
        common=[] #Contains keys of common dishes
        for key in dict.keys():
            for item in items:
                if item.dish.pk==int(key):
                    item.quantity=dict[key]
                    item.save()
                    common.append(int(key))
        new_keys=Diff(common,list(dict.keys()))
        for key in new_keys:
            #Create Items as they've not been ordered before
            dish=Dish.objects.get(pk=int(key))
            quantity=dict[key]
            item=Item.objects.create(dish=dish,quantity=quantity)
            if item is not None:
                Order.items.add(item)
        Order.save()
            
            
def get_avg_time(Order):
    avg_time=0
    items=Order.items.all()
    if items.count() == 0:
        return avg_time 
    else:
        for item in items:
            avg_time+=item.dish.avg_time
        return avg_time

def build_previous_order(Order):
    ret={}
    items=Order.items.all()
    if items.count()!=0:
        for item in items:
            key=item.dish.pk
            quantity=item.quantity
            ret[key]=quantity
    return ret
    return ret
            

'''Functions for reservations'''

#Return the tables available 
def tables_avail(Restaurant):
    avail_capacity=Restaurant.capacity
    reservations=Restaurant.reservations.all()
    if reservations is None:
        return avail_capacity
    else: 
        for reservation in reservations:
            avail_capacity-=reservation.tables
        return avail_capacity
def set_tableno(Reservation):
    restaurant=Reservation.restaurant
    reservations=restaurant.reservations.all()
    list=[]
    populate(list,restaurant.capacity)
    #If this is the first reservation
    if(restaurant.reservations.count()==1):
        table_no=extract_min(list,int(Reservation.tables))
        table_no= [str(element) for element in table_no]
        string=",".join(table_no)
        string+=','
        Reservation.table_no=string
        Reservation.save()
    else:
        avail_tables=[]
        string=''
        for reservation in reservations:
            string+=reservation.table_no
        string=string[:len(string)-1]
        tables_occupied=string.split(",")
        tables_occupied=[int(element) for element in tables_occupied ]
        tables_avail=Diff(tables_occupied,list)
        table_no=extract_min(tables_avail,int(Reservation.tables))
        table_no= [str(element) for element in table_no]
        table_no=",".join(table_no)
        table_no+=','
        Reservation.table_no=table_no
        Reservation.save()



        
        