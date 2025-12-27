from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from electronix import views # make sure to import your views

urlpatterns = [
    path('admin/', admin.site.urls),
    

    path('accounts/', include('allauth.urls')),
    
    path('', include('electronix.urls')),
    path('setup-admin-99/', views.create_admin_account),
    
]