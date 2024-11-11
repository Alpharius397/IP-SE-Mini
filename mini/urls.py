"""
URL configuration for mini project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'asd'
urlpatterns = [
    path('super_admin/', admin.site.urls, name='super-admin'),
    path('', views.home_view,name='home'),
    path('<str:error>', views.home_view,name='home'),
    path('login/',views.login_view,name='login'),
    path('login/<str:error>/',views.login_view,name='login'), 
    path('register/',views.register_view,name='register'), 
    path('logout/',views.logout_user,name='logout'),
    path('camp/<int:id>/', views.camp_view,name='camp'),
    path('camp/<int:id>/<str:error>', views.camp_view,name='camp'),
    path('regCamp/<int:id>/',views.regCamp,name='camp_reg'),
    path('registerCamp/<int:id>/',views.donor_reg,name='donor_reg'),
    path('confirm/<int:donor>/<int:camp>/',views.confirm_reg,name='confirm'),
    path('camps_by/<int:id>/',views.camps_all,name='camps_all')
]

admin.site.site_header = "System Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Blood Bank Management Admin Portal"