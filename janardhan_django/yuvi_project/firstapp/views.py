from django.shortcuts import render,HttpResponse,redirect
from firstapp.models import Wear,Cart,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
import razorpay
import random
from django.core.mail import send_mail
from django.db import migrations
from django.contrib import messages




# Create your views here.
def filterByCategory(request,caname):
     context={}
     C1 = Q(category=caname)
     C2 = Q(price__gte = 200.00)
     allwe = Wear.objects.filter(C1 & C2)
     print('number of prod:',len(allwe))
     context['wear']=allwe
     return render(request,'new_index.html',context)
     
     

def rangeSearch(request):
     context={}
     min = request.GET['min']
     max = request.GET['max']
     # ex2. select * from student where percent between 60.00 and 70.00;
     # select * from student where percent >= min and percent <= max;
     c1 = Q(price__gte = min)
     c2 = Q(price__lte = max)
     allwe = Wear.objects.filter(c1 & c2)
     context['wear']=allwe
     return render(request,'new_index.html',context)

def sortStudents(request,ord):
     context={}
     if ord == '0':
          # print('ascending sort')
          col='price'
     else:
          # print('decending sort')
          col='-price'  
     allwe = Wear.objects.all().order_by(col)
     context['wear']=allwe
     return render(request,'new_index.html',context)
def index_pg(request):

     #return render(request,'index.html')

     # index.html off/layout.html on
     #return render(request,'layout.html')
     context={}
     allwe = Wear.objects.all()
     context['wear']=allwe
     return render(request,'new_index.html',context)
     #return render(request,'register.html')

def home_fn(request):
    return render(request,"home.html")


def Wear_Details(request):
    if request.method=="GET":
        print('within get()')
        return render(request,"studtls.html")
    else:
        print('within post')
        n =request.POST['name']
        b =request.POST['wecategory']
        p =request.POST['weprice']
        we =Wear.objects.create(name=n,category=b,price=p)
        we.save()
        #print('received:' ,n,b,p)
        #return render(request,'home.html')
        return redirect('/index')

def dashboard(request):
    data = Wear.objects.all()
    print(type(data))
    context={}
    context['wedata']=data
    return render(request,'dashboard.html',context)

def delWear(request,rid):
     print('delete Wear:',rid)
     data = Wear.objects.filter(id=rid)
     print('TYPE:',type(data))
     print('received data:',data)
     data.delete()
     return redirect('/index')

def register(request):
     if request.method == "GET":
          return render(request,'register.html')
     else:
          context={}
          n= request.POST['username']
          p= request.POST['userpassword']
          c= request.POST['confirmpassword']
          e=request.POST['useremail']
          if n=='' or p=='' or e=='':
               context['errorMsg']='Kindly enter all fields'
               return render(request,'register.html',context)
          elif p!=c :
               context['errorMsg']='Password and confirm password is not same'
               return render(request,'register.html',context)
          else:
               # u = User.objects.create(username=n,password=p,email=e)
               # u.save()
               u = User.objects.create(username=n,email=e)
               u.set_password(p)# encrypted password
               u.save()
               #print('received registered data:',n,p)
               context['success']='Registered successfully!!'
               return render(request,'login.html')

def userlogin(request):
     if request.method=='GET':
          return render(request,'login.html')
     else:
          context={}
          u = request.POST['username']
          p = request.POST['userpassword']
          #print('login details:',u,p)
          if u=='' or p=='':

               context['errorMsg']='plz provide all details'
               return render(request,'login.html',context)
          else:
               u = authenticate(username=u, password=p)
               if u is not None:
                    login(request,u)
                    print(request.user.is_authenticated)
                    return render(request,'new_index.html')
               else:
                    context['errorMsg']='plz provide correct credentials'
                    return render(request,'login.html',context)

def user_logout(request):
     logout(request)
     return redirect('/index')

def showDetails(request,sid):
     we = Wear.objects.filter(id=sid)
     context={}
     context['wear']=we[0]
     return render(request,'details.html',context)

def addToCart(request,sid):
     userid = request.user.id
     if userid:
          user = User.objects.filter(id=userid)
          #print(user[0])
          we = Wear.objects.filter(id=sid)
          #print(stu[0])
          c = Cart.objects.create(sid=we[0],uid=user[0])
          c.save()
          return HttpResponse('cart added')
     else:
          return render(request,'login.html')

def viewcart(request):
     userid = request.user.id
     if userid:
          user = User.objects.filter(id=userid)
          mycart = Cart.objects.filter(uid=user[0])
          context={}
          context['cart']=mycart
          count = len(mycart)
          total = 0
          for cart in mycart:
               total += cart.quantity*cart.sid.price
               context['count'] = count
               context['total'] = total
          return render(request,'viewcart.html',context)
     else:
          return render(request,'login.html')
     

def deleteFromCart(request,sid):
     cart = Cart.objects.filter(id = sid)
     cart.delete()
     return redirect('/viewcart')

def updateQuantity(request,incr,cid):
     # print(incr, cid)
     c = Cart.objects.filter(id = cid)
     if incr=='0': #decr qty
          new_qunat = c[0].quantity -1
     else: #incr qty
          new_qunat = c[0].quantity +1
     c.update(quantity = new_qunat)
     return redirect('/viewcart')
          

def placeOrder(request):
     context={}
     userid = request.user.id
     order_id = random.randrange(1000,9999)
     # fetch current cart
     mycart = Cart.objects.filter(uid = userid)
     # add the cart items to order
     for cart in mycart:
               ord = Order.objects.create(order_id=order_id,
                         sid = cart.sid,uid = cart.uid,quantity=cart.quantity)
               ord.save()
     mycart.delete() # clear cart table for current user
     mycart = Order.objects.filter(uid=userid) # fetch order details
     
     # calculate count and total
     count = len(mycart)
     billAmount = 0
     for cart in mycart:
          billAmount += cart.sid.price*cart.quantity
     context['count'] = count
     context['billamount'] = billAmount
     context['mycart']=mycart
     return render(request,'placeorder.html',context)

     
def makePayment(request):

     userid = request.user.id
     ordDetails = Order.objects.filter(uid = userid)


     bill=0
     for ord in ordDetails:
          bill += ord.sid.price * ord.quantity
          ordId = ord.order_id
     client = razorpay.Client(auth=("rzp_test_mMoMXGQg9McTXh", "lysYWbP10fJjDTBSZ6ei9dPK"))

     data = { "amount":bill*100, "currency": "INR", "receipt": str(ordId) }

     payment = client.order.create(data=data)
     #print(payment)
     #return HttpResponse('sucess')
     context={}
     context['data']=payment
     return render(request,'pay.html',context)


def sendemail(request):
     msg = "order details are:"
     email = request.user.email
     print(request.user.id)
     send_mail(
     "Ekart order Placed Successfully",
     msg,
     "yuvrajpokharkar111@gmail.com",
     [email],
     fail_silently=False
          
     )
     #print(request.user.email)
     return HttpResponse('mail sent Successfully')

def set_default_value(apps, schema_editor):
    YourModel = apps.get_model('firstapp', 'YourModel')
    YourModel.objects.filter(image__isnull=True).update(image='default_image.jpg')

class Migration(migrations.Migration):


    dependencies = [
        ('firstapp', 'previous_migration_file'),  # Replace with actual dependency
    ]

    operations = [
        migrations.RunSQL(set_default_value),
    ]

def Contact_us(request):
     context={}
     return render(request,'contactus.html',context)