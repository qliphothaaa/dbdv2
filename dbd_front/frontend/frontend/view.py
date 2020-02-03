from django.shortcuts import render
from CompanyModel import models

def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)

def list_company(request):
    company_list = models.Dbdcompany.objects.all()
    return render(request, 'company.html', {"company_list":company_list})

def list_newquery(request):
    new_query_list = models.DbdNewQuery.objects.all()
    return render(request, 'new_query.html', {"new_query_list":new_query_list})

def list_query(request):
    query_list = models.DbdQuery.objects.all()
    return render(request, 'query.html', {"query_list":query_list})
