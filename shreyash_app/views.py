from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

## for model perdiction liabraries 
import pickle
from sklearn.preprocessing import StandardScaler


# Create your views here.
def index(request):
    #for showing card in home page(index page)
    queryset = courses.objects.all()
    context = {'courses' : queryset}
    return render(request, 'website/index.html', context)# we have to say django where we store our templates 
#so we create a folder name templates and store and in settings.py there is one templates section there we mention the name(templates) 

def about (request):
    return HttpResponse('this is about page')

def contact(request):
    return render(request, 'website/contact_page.html')

#post method 
@login_required(login_url="/login/")
def create_courses(request):
    if request.method == "POST":
        data = request.POST# it is optional if we doesnt write this we have to write everywhere request.POST insted of data 
        course_image = request.FILES.get("cours/")  # Match the input field name in your template

        # Extract form data and give to the variables
        course_name = data.get('course_name')
        course_price = data.get('course_price')
        course_date = data.get('course_date')
        course_batch_student_numbers = data.get('course_batch_student_numbers')
        course_image = data.get('cours/')
        course_description = data.get('course_description')

        # Save data to the database through found varibles from the above code
        courses.objects.create(
            course_name=course_name,
            course_price=course_price,
            course_date=course_date,
            course_batch_student_numbers=course_batch_student_numbers,
            course_image=course_image,
            course_description= course_description, 
        )
        return redirect('/')


    # get method
    # it is used to show the data in the table which is in the course.html page
    queryset = courses.objects.all()
    context = {'courses' : queryset}
    return render(request, 'website/courses.html', context)

# writting a delete api 
@login_required(login_url="/login/")
def delete_(request,id):
    queryset = courses.objects.get(id = id)
    queryset.delete()
    return redirect('/')

#writing update api
@login_required(login_url="/login/")
def update(request, id):
    queryset = courses.objects.get(id=id)
    context = {'course': queryset}
    return render(request, 'website/update.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password  = request.POST.get('password')

        ### it checks user from database user is in database or not 
        user = User.objects.filter(username = username)
        if not user.exists():
            messages.error(request , "user doesnt exists")
            return redirect("/login/")
        
        ### check if user is not none then login the user and print massage user login succesfully
        user = authenticate(username = username, password = password )
        if user is not None:
            login(request , user)
            messages.success(request, "user login succesfully")
            return redirect("/")
            
        
        else :
            messages.error(request, "invalid password")
            return redirect("/login/")
        # else invelid user and redirect it to same page 

    return render (request , 'website/login.html')


def logout_page(request):
    logout(request)
    return redirect('/')


def register(request):
### geting data from form 
    if request.method == 'POST':
        data = request.POST

        first_name =  data.get('firstname')
        last_name  =  data.get('lastname')
        username =  data.get('username')
        password  =  data.get('password')


### it checks if user is exists in database then it doesnt throw error 
## it shows massage to user that user already exists 
# other wise account created succesfully 
        user = User.objects.filter(username = username)# it save user in database 
        if user.exists(): 
           messages.info(request, "the account is already exists")
           return redirect("/register/")
        else :
            messages.info(request, "account created succesfully")
### it simply redirect to register page again which is not possible if we dont write this


### save data to data base 
        user = User.objects.create (
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save()

        return redirect ('/login/')



    return render(request, 'website/register.html')
    
@login_required(login_url="/login/")
def purchase(request ,id):
    queryset = courses.objects.get(id=id)
    context = {'course': queryset}
    return render(request, 'website/purchase.html',context)



def course_detail(request, id):
    queryset = courses.objects.get(id = id)
    context = {'course': queryset}
    return render(request, 'website/card_details.html', context)



#for getting data from the pkl file
import os 

model_path = os.path.join(os.path.dirname(__file__), 'pkl/model.pkl')
scaler_path = os.path.join(os.path.dirname(__file__), 'pkl/scaler.pkl')

ridge = pickle.load(open(model_path, 'rb'))
standardization = pickle.load(open(scaler_path, 'rb'))


def prediction(request):
    if request.method == 'POST':
        data = request.POST
        # save float data into variables  #float data becuse data is in int formate our model wants float to predict the data
        MedInc = float(data.get('MedInc'))
        HouseAge = float(data.get('HouseAge'))
        AveRooms = float(data.get('AveRooms'))
        AveBedrms = float(data.get('AveBedrms'))
        Population = float(data.get('Population'))
        AveOccup = float(data.get('AveOccup'))
        Latitude = float(data.get('Latitude'))
        Longitude = float(data.get('Longitude'))

        #fitting data into staenderd_scler and then predict it which is geting from form 
        new_data_scaled = standardization.transform([[MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude]])  # we don't fit the data because of data leak, we only transform
        result = ridge.predict(new_data_scaled)
        # and after successfull predction we show the result to same page(html form)
        return render(request, 'website/predction.html', {'result': result})

    return render(request, 'website/predction.html')