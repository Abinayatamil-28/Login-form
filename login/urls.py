from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='index'), 
    path('login/', views.login_view, name='login'),
    path('password_rest/', views.password_reset, name='password_reset'),
    
]