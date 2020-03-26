from django.shortcuts import render
#from CompanyModel import models
#from django.core.paginator import Paginator


'''
def list_company(request):
    company_list = models.Dbdcompany.objects.all()
    return render(request, 'company.html', {"company_list":company_list})
#


def list_newquery(request):
    new_query_list = models.DbdNewQuery.objects.all()
    return render(request, 'new_query.html', {"new_query_list":new_query_list})

def list_query(request):
    query_list = models.DbdQuery.objects.all()
    return render(request, 'query.html', {"query_list":query_list})



def list_company(request):
    company_list = models.Dbdcompany.objects.all()
    limit = 10
    paginator = Paginator(company_list, limit)
    page = request.GET.get('page','1')
    result = paginator.page(page)

    return render(request, 'company.html', {"company_list":result})

def search(request):
    query = request.GET.get('query')
    error_msg = ''
    if not query:
        error_msg = 'please input key word'
        return render(request, 'errors.html', {'error_msg': error_msg})

    companys = models.Dbdcompany.objects.filter(dbd_id__exact=query)
    return render(request, 'company_detail.html', {'error_msg':error_msg,'companys': companys})
'''
