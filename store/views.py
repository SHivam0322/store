from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Product,Contact,Orders,OrderUpdate
from math import ceil
from django.contrib.auth.models import User
import json
from django.contrib import messages
import  re
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
def index(request):
    # products = Product.objects.all()
    
    # params={'no_of_slides': nSlides,'range':range(1,nSlides),'product' : products}
    # allProds = [[products , range(1,nSlides),nSlides],[products , range(1,nSlides),nSlides]]
   
    allProds=[]
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil(n/4)-(n//4)
        allProds.append([prod,range(1,nSlides),nSlides])
    params={'allProds':allProds}
    return render(request,'store/index.html', params)

def about(request):
    return render(request,'store/about.html')

def contact(request):
    if request.method == "POST":
          print(request)
          name = request.POST.get('name','')
          email = request.POST.get('email','')
          number = request.POST.get('number','')
          issue = request.POST.get('issue','')
          contact=Contact(name=name,email=email,number=number,issue=issue)
          contact.save()
    return render(request,'store/contact.html')

def tracker(request):
    if request.method =="POST":
         orderId = request.POST.get('orderId','')
         phone = request.POST.get('phone','')
         try:
            order = Orders.objects.filter(order_id=orderId,phone=phone)
            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response=json.dumps({"status":"success" , "updates":updates,"itemsJson":order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
         except Exception as e:
             return HttpResponse('{"status":"error"}')
    return render(request,'store/tracker.html')

def searchMatch(query, item):
    if query in item.product_name.lower() or query in item.product_name or query in item.category.lower() or query in item.category or query in item.desc.lower() or query in item.desc or query in item.subcategory.lower() or query in item.subcategory:
        return True
    else:
        return False
    
def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<3:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'store/search.html', params)

def productView(request,myid):
    product = Product.objects.filter(id=myid)
  
    return render(request,'store/productView.html',{'product':product[0]})

def checkout(request):
     if request.method == 'POST':
         items_json=request.POST.get('items_Json','')
         name = request.POST.get('name','')
         amount = request.POST.get('amount','')
         phone = request.POST.get('phone1','') 
         email = request.POST.get('email','')
         address = request.POST.get('address1','') + " " + request.POST.get('address2','')
         city = request.POST.get('city','')
         state = request.POST.get('state','')
         zip_code = request.POST.get('zip','')
         order = Orders(items_json=items_json,name=name,phone=phone,address=address, city=city, state=state, zip_code=zip_code,amount=amount)
         order.save()
         update=OrderUpdate(order_id=order.order_id,update_desc="Order has been placed successfully !!")
         update.save()
         thank= True
         id= order.order_id
         return render(request,'store/checkout.html',{'thank':thank,'id':id})
         
     return render(request,'store/checkout.html')


def handleSignup(request):
    if request.method == 'POST':
      fname = request.POST.get('fname')
      lname = request.POST.get('lname')
      email = request.POST.get('email')
      phone = request.POST.get('phone')
      password1 = request.POST.get('password1')
      password2 = request.POST.get('password2')

      if password1 != password2:
          messages.error(request,"Passwords do not match")
          return redirect('/store')
     
      if (len(phone)!=10):
          messages.error(request,"Invalid Phone Number")
          return redirect('/store')

    #   if (isinstance(fname, str)):
    #       messages.error(request,"Invalid First Name")
    #       return redirect('/store')
    #   if (isinstance(lname, str)):
    #       messages.error(request,"Invalid Last Name")
    #       return redirect('/store')
      myuser = User.objects.create_user(email,phone,password1)
      myuser.first_name = fname
      myuser.last_name= lname
      myuser.phone = phone
      myuser.save()
      messages.success(request,"Account created successfully !!")
      return redirect('/store')
    else:
        return HttpResponse('404 - Not Found')
 
def handleLogin(request):
     if request.method == 'POST':
      loginemail = request.POST.get('loginemail')
      loginpass = request.POST.get('loginpass')
      user=authenticate(username=loginemail, password=loginpass)
      if user is not None:
          login(request, user)
          messages.success(request,"Logged In Successfully")
          return redirect('/store')
     else:
         messages.error(request,"Please Provide valid credentials")
         return redirect('/store')
def handleLogout(request):
        logout(request)
        messages.success(request,"Logged out successfully")
        return redirect('/store')
