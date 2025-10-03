"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from apps.users.forms import CustomAuthenticationForm
from django.contrib.auth import views as auth_views
from .views import dashboard

urlpatterns = [
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),

    #API
    path('api/user/', include('apps.users.urls')),

    # Apps métiers
    path('sites/', include('apps.sites.urls')),
    path('activite/', include('apps.activite_quotidien.urls')),
    path('fournisseurs/', include('apps.fournisseurs.urls')),
    path('aliment/', include('apps.stocks.urls')),

    # Utilisateurs
    path('users/', include('apps.users.urls')),

    #Admin
    path('admin/', admin.site.urls),

]
