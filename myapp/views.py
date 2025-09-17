from django.shortcuts import render,redirect
from .models import *
# Create your views here.

def index(request):
    if request.session.get('email'):
        user = Citizen.objects.get(email=request.session['email'])
        if user.role == "citizen":
            complaint = Complaint.objects.filter(citizen=user)
            missing = MissingPerson.objects.filter(citizen=user)
            return render(request,'citizen.html',{'user':user,'complaint':complaint,"missing":missing})
        
        elif user.role == "inspector":
            fir = Complaint.objects.filter(Inspector=user.name)
            return render(request,'inspector.html',{'user':user,'fir':fir})
        
        elif user.role == "commissioner":
            fir = Complaint.objects.all()
            inspector = Inspector.objects.all()
            inlen = len(inspector)
            return render(request,'commissioner.html',{'fir':fir,'inspector':inspector,'inlen':inlen})
    else:
        return render(request,'visitor.html')
        

def signup(request):
    if request.method == "POST":
        try:
            user = Citizen.objects.get(email=request.POST['email'])
            msg = "This email is Already Register"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                Citizen.objects.create(
                    name = request.POST['name'],
                    email = request.POST['email'],
                    address = request.POST['address'],
                    password = request.POST['password'],
                )
                return redirect('login')
            else:
                msg = "Password and Confirm Password Not match"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')

def login(request):
    if request.method == "POST":
        try:
            user = Citizen.objects.get(email=request.POST['email'])
            if user.password == request.POST['password']:
                request.session['email']=user.email
                return redirect('index')
            else:
                msg = "Password is not Match"
                return render(request,'login.html',{'msg':msg})
                
        except Exception as e:
            msg = "Citizen Not found"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')
    
def logout(request):
    del request.session['email']
    return redirect('index')

def addfir(request):
    if request.method == "POST":
        user = Citizen.objects.get(email=request.session['email'])
        Complaint.objects.create(
            citizen = user,
            title = request.POST['title'],
            category = request.POST['category'],
            description = request.POST['description'],
            locations = request.POST['locations'],
            date = request.POST['date'],
            time = request.POST['time'],
            evidence = request.FILES['evidence'],
        )
        return redirect('index')
        
    else:
        return render(request,'addfir.html')
    
def viewfir(request,pk):
    complaint = Complaint.objects.get(pk=pk)
    return render(request,'viewfir.html',{'complaint':complaint})
    
def missingperson(request):
    if request.method == "POST":
        user = Citizen.objects.get(email=request.session['email'])
        
        MissingPerson.objects.create(
            citizen = user,
            name = request.POST['name'],
            age = request.POST['age'],
            gender = request.POST['gender'],
            description = request.POST['description'],
            date = request.POST['date'],
            photo = request.FILES['photo'],
        )
        return redirect('index')
    else:
        return render(request,'missingperson.html')
    
def commissioner(request):
    if request.method == "POST":
        Inspector.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            area = request.POST['area'],
        )
        return redirect('index')
    
    else:
        return render(request,'index.html')
    
    
def delinspector(request,pk):
    inspector = Inspector.objects.get(pk=pk)
    inspector.delete()
    return redirect(index)

def ainspector(request):
    if request.method == "POST":
        complaint = Complaint.objects.get(pk=request.POST['pk'])
        complaint.Inspector = request.POST['inspector']
        # complaint.status = "progress"
        complaint.save()
        return redirect('index')
    else:
        return render(request,'index.html')
    
def upcom(request):
    if request.method == "POST":
        try:
            complaint = Complaint.objects.get(pk=request.POST['id'])
            complaint.status = request.POST['status']
            complaint.remark = request.POST['remark']
            complaint.save()
            return redirect('index')
        except Exception as e:
            print("===================================",e)
            return redirect('index')
            
    else:
        return render(request,'index.html')
    