# first of all define models in models.py (create class of main data)
# then update settings.py if you are adding image or store imag in database
# then django autometically create one intial file in migration when you command in cmd or terminal make migration (your file name)
# then you have to intialize or define where is link store for that you have to do in url.py(app not in project url)
#then you have to register models in admin.py

from django.db import models
from django.utils import timezone #added by me 
from django.contrib.auth.models import User

# Create your models here.
# this model will  pass value from frontend to database
class food(models.Model):
    FOOD_TYPE_CHOICE = [
        ('mld', 'masala_dosa'), 
        ('pld', 'plain_dosa'),
        ('cd', 'chesse_dosa'),
    ]
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='food/')
    date_added= models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=3, choices= FOOD_TYPE_CHOICE) # untill this 

    def __str__(self):
        return self.name
    

# here we submit this model via django shell using through from appname.model import *(all) then submitt the value according to model
# students2 = student(name = "xyz", email_id = "xyz@gmail.com" , roll_no = 12 , contect = 22584245 , address = "hii")

class student(models.Model):
    name= models.CharField(max_length=100)
    email_id = models.EmailField( max_length=254)
    roll_no = models.IntegerField(max_length=10)
    contect = models.IntegerField(max_length=10)
    address = models.CharField(max_length=100)

class courses (models.Model):
    course_name = models.CharField(max_length=50)
    course_price = models.IntegerField(max_length=10)
    course_date = models.DateField(auto_now=False, auto_now_add=False)
    course_batch_student_numbers = models.IntegerField(max_length = 100)
    course_image = models.ImageField(upload_to="cours/")
    course_description = models.TextField(max_length=500,default = "This is course description")

    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True,)# for user pass auth, 
