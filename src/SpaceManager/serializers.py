# -*- coding: utf-8 -*-
from rest_framework import routers, serializers, viewsets
from SpaceManager.models import *
from UserAndPrj.models import *
from django.contrib.auth.decorators import login_required
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from dss.Serializer import serializer as objtojson
from Scc4PM.restsetings import *
from rest_framework import filters
import django_filters

class SpaceStatusSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = SpaceStatus
        fields = '__all__'

class SpaceStatusViewSet(viewsets.ModelViewSet):
    queryset = SpaceStatus.objects.all()
    serializer_class = SpaceStatusSerializer


class SpaceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    statusname = serializers.ReadOnlyField(source='status.name')
    zonename = serializers.ReadOnlyField(source='zone.name')

    class Meta:
        model = Space
        fields = '__all__'

class SpaceViewSet(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer

    filter_fields = ('id','number')
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,)
    search_fields = ('number','name')


class SpaceAsignmentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    spacename = serializers.ReadOnlyField(source='space.name')
    spacenumber = serializers.ReadOnlyField(source='space.number')
    majorname = serializers.ReadOnlyField(source='major.name')
    companyname = serializers.ReadOnlyField(source='company.name')
    username = serializers.ReadOnlyField(source='user.truename')
    statusname = serializers.ReadOnlyField(source='status.name')

    class Meta:
        model = SpaceAsignment
        fields = '__all__'

class SpaceAsignmentViewSet(viewsets.ModelViewSet):
    queryset = SpaceAsignment.objects.all()
    serializer_class = SpaceAsignmentSerializer

    filter_fields = ('id','space_id')


class SpaceIBeaconSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = SpaceIBeacon
        fields = '__all__'

class SpaceIBeaconViewSet(viewsets.ModelViewSet):
    queryset = SpaceIBeacon.objects.all()
    serializer_class = SpaceIBeaconSerializer

    def get_queryset(self):
        queryset = SpaceIBeacon.objects.all()
        uuid = self.request.query_params.get('uuid', None)
        major = self.request.query_params.get('major', None)
        minor = self.request.query_params.get('minor', None)
        if uuid and major and minor:
            queryset = queryset.filter(uuid=uuid,major=major,minor=minor)
        return queryset

router = routers.DefaultRouter()
router.register(r'spacestatuss', SpaceStatusViewSet)
router.register(r'spaces', SpaceViewSet)
router.register(r'spaceasignments', SpaceAsignmentViewSet)
router.register(r'spaceibeacons', SpaceIBeaconViewSet)