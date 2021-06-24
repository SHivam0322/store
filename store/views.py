from django.shortcuts import render
from django.http import HttpResponse
from . models import Product,Contact
from math import ceil

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
    return render(request,'store/tracker.html')

def search(request):
    return render(request,'store/search.html')

def productView(request,myid):
    product = Product.objects.filter(id=myid)
  
    return render(request,'store/productView.html',{'product':product[0]})

def checkout(request):
    return render(request,'store/checkout.html')