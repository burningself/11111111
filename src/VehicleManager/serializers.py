# -*- coding: utf-8 -*-
from rest_framework import routers, serializers, viewsets
from VehicleManager.models import *
from UserAndPrj.models import *
from TaskAndFlow.serializers import *
from django.contrib.auth.decorators import login_required
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from dss.Serializer import serializer as objtojson
from Scc4PM.restsetings import *
from rest_framework import filters
import django_filters

class VehicleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    companyname = serializers.ReadOnlyField(source='company.name')
    class Meta:
        model = Vehicle
        fields = '__all__'

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, )


class AlarmInfoPlateSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    company = serializers.SerializerMethodField()
    image = DocumentSerializer(read_only=True)
    imageplate = DocumentSerializer(read_only=True)

    def get_company(self,obj):
        company = u"未知"
        try:
            company = Vehicle.objects.get(plate=obj.license).company.name
        except Exception as e:
            pass
        return company

    class Meta:
        model = AlarmInfoPlate
        fields = '__all__'

class AlarmInfoPlateViewSet(viewsets.ModelViewSet):
    queryset = AlarmInfoPlate.objects.all()
    serializer_class = AlarmInfoPlateSerializer
    
    filter_fields = ('license','recotime','parkdoor')

    



router = routers.DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'alarmInfoplates', AlarmInfoPlateViewSet)
