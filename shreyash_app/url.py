from django.contrib import admin
from django.urls import path
from shreyash_app import views
from django.conf import settings
from django.conf.urls.static import static  


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name = 'home' ),
    path('food/',views.index, name = 'index' ),
    path('about/',views.about , name = 'about'),
    path('contact/',views.contact, name = 'contact'),
    path('courses/',views.create_courses, name = 'courses'), 
    path('delete/<id>/', views.delete_, name = "delete"),
    path('update/<id>/', views.update, name = "update"),
    path('login/', views.login_page, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.logout_page, name = 'logout'),
    path('purchase/<id>/', views.purchase, name = 'purchase'),
    path('card_details/<id>/', views.course_detail, name = 'card_details'),
    path('predction/', views.prediction, name = 'predction'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)# for storing image in databases you have to define url path