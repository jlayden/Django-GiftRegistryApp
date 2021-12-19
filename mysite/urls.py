from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from mysite import views

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  path('', views.Home.as_view()),
  path('registration/', views.Registration.as_view()),
  path('users/', views.Users.as_view()),
  path('gifts/', views.Gifts.as_view()),
  path('othergifts/', views.OtherGifts.as_view()),
]
