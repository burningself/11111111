# -*- coding: utf-8 -*-
from rest_framework import routers, serializers, viewsets
from UserAndPrj.models import *
from Scc4PM.restsetings import *
from TaskAndFlow.utility import *
from UserAndPrj.utility import *
from Scc4PM import settings
from django.contrib.auth.decorators import login_required
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import *
from rest_framework import filters
import django_filters
from dss.Serializer import serializer as objtojson
from UserPrjConfig.serializers import UserRolesSerializer,UserDivisionSerializer


class MajorSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = UserMajor
        fields = '__all__'

class MajorViewSet(viewsets.ModelViewSet):
    queryset = UserMajor.objects.all()
    serializer_class = MajorSerializer
    pagination_class = SelfPagination
    authentication_classes = (CsrfExemptSessionAuthentication, )
    filter_fields = ('name',)
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name',)

    def get_queryset(self): 
        isAll = self.request.query_params.get('isAll', False)
        if not isAll:
            queryset = getMajorList()
        else:
            queryset = UserMajor.objects.all()
        return queryset


#-----------------User-------------------------
class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    companyname = serializers.ReadOnlyField(source='company.name')
    majorname = serializers.ReadOnlyField(source='major.name')
    userPrjRoles = UserRolesSerializer(many=True,read_only=True)
    userdivisions = UserDivisionSerializer(many=True,read_only=True)

    class Meta:
        model = User
        fields = '__all__'

        
def getDivisionUserlist(divisionId):
    prjMemberlist = UserDivision.objects.filter(division_id = divisionId).values_list("user_id", flat=True).distinct()
    memberList = User.objects.filter(id__in=list(prjMemberlist))
    return memberList

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = SelfPagination
    authentication_classes = (CsrfExemptSessionAuthentication, )
    filter_fields = ('company','major')
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,CustomOrderingFilter,)
    search_fields = ('name','truename')
    custom_ordering = ('truename',)
    ordering_fields = ('name','truename','company__name','major__name')


    def get_queryset(self): 
        isAll = self.request.query_params.get('isAll', False)
        getOther = self.request.query_params.get('getOther', False)

        if isAll:
            queryset = User.objects.all()
        elif getOther:
            queryset = getOtherUserlist()
        else:
            queryset = getPrjUserlist()

        divisionId = self.request.query_params.get('divisionId', None)
        if divisionId:
            divisionUserlist = UserDivision.objects.filter(division_id = divisionId).values_list("user_id", flat=True).distinct()
            queryset = queryset.filter(id__in=list(divisionUserlist))
            
        return queryset



class CompanySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Company
        fields = '__all__'

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = SelfPagination
    authentication_classes = (CsrfExemptSessionAuthentication, )
    filter_fields = ('name',)
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name',)

#-----------------------------
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    image = serializers.SerializerMethodField()

    def get_image(self,obj):
        return getPrjImage(obj)

    class Meta:
        model = Project
        fields = '__all__'

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.exclude(projecturl="")
    serializer_class = ProjectSerializer
    pagination_class = SelfPagination
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly,)

    filter_fields = ('name',)
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name',)

    def get_queryset(self): 
        curProject = self.request.query_params.get('curProject', False)
        if not curProject:
            queryset = Project.objects.exclude(projecturl="")
        else:
            queryset = Project.objects.filter(id=CURRENT_PROJECT_ID)
        return queryset



#-----------------------------
class KnowledgeHazardlistSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = KnowledgeHazardlist
        fields = '__all__'

class KnowledgeHazardlistViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeHazardlist.objects.all()
    serializer_class = KnowledgeHazardlistSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'majors', MajorViewSet)
router.register(r'companys', CompanyViewSet)
router.register(r'project', ProjectViewSet)

router.register(r'knowledgehazardlists', KnowledgeHazardlistViewSet)
