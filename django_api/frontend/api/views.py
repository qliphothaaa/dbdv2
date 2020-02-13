from CompanyModel.models import Dbdcompany, DbdNewQuery, DbdQuery
from api.serializers import CompanySerializer, NewQuerySerializer, QuerySerializer

from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Dbdcompany.objects.all()
    serializer_class = CompanySerializer
    
class NewQueryViewSet(viewsets.ModelViewSet):
    queryset = DbdNewQuery.objects.all()
    serializer_class = NewQuerySerializer
    permission_classes = (IsAuthenticated,)

class QueryViewSet(viewsets.ModelViewSet):
    queryset = DbdQuery.objects.all()
    serializer_class = QuerySerializer
    permission_classes = (IsAuthenticated,)


class UnfinishedList(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        province = self.kwargs['province']
        queryset = Dbdcompany.objects.filter(dbd_province=province)
        return  queryset
