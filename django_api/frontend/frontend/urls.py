"""frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
#from . import view
#from api import views
#from rest_framework.routers import DefaultRouter

#router = DefaultRouter()
#router.register(r'company', views.CompanyViewSet)
#router.register(r'newquery', views.NewQueryViewSet)
#router.register(r'query', views.QueryViewSet)
#router.register(r'unfinished', views.UnfinishedList, basename='')

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('company/', view.list_company),
    #path('newquery/', view.list_newquery),
    #path('query/', view.list_query),
    #path('api/', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('func/', include('upload.urls')),
    #path('search/', view.search)
]
