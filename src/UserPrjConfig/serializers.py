# -*- coding: utf-8 -*-
from rest_framework import routers, serializers, viewsets
from UserPrjConfig.models import *
from Scc4PM.restsetings import *
from django.contrib.auth.decorators import login_required
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import *
from rest_framework import filters
import django_filters
from dss.Serializer import serializer as objtojson


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Author
        fields = ('id','name','classify')

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = SelfPagination
    authentication_classes = (CsrfExemptSessionAuthentication, )
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name',)


class RoleAuthorSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    rolename = serializers.ReadOnlyField(source='role.name')
    authname = serializers.ReadOnlyField(source='auth.name')
    authid = serializers.ReadOnlyField(source='auth.id')

    class Meta:
        model = RoleAuthor
        fields = '__all__'

class RoleAuthorViewSet(viewsets.ModelViewSet):
    queryset = RoleAuthor.objects.all()
    serializer_class = RoleAuthorSerializer
    pagination_class = SelfPagination
    authentication_classes = (CsrfExemptSessionAuthentication, )
    filter_fields = ('role','auth')

#-----------------UserRole-------------------------
class RoleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    roleAuthors = RoleAuthorSerializer(many=True,read_only=True)

    class Meta:
        model = Role
        fields = '__all__'

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = SelfPagination
    authentication_classes = (CsrfExemptSessionAuthentication, )
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name',)


#-----------------------------
class UserRolesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    rolename = serializers.ReadOnlyField(source='role.name')
    
    class Meta:
        model = UserRoles
        fields = '__all__'

class UserRolesViewSet(viewsets.ModelViewSet):
    queryset = UserRoles.objects.all()
    serializer_class = UserRolesSerializer
    pagination_class = SelfPagination
    authentication_classes = (CsrfExemptSessionAuthentication, )


#-----------------------------division------------------
class DivisionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Division
        fields = '__all__'

class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    pagination_class = SelfPagination
    authentication_classes = (CsrfExemptSessionAuthentication, )
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name',)


#-----------------------------
class UserDivisionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    divisionname = serializers.ReadOnlyField(source='division.name')
    
    class Meta:
        model = UserDivision
        fields = '__all__'

class UserDivisionViewSet(viewsets.ModelViewSet):
    queryset = UserDivision.objects.all()
    serializer_class = UserDivisionSerializer
    pagination_class = SelfPagination
    authentication_classes = (CsrfExemptSessionAuthentication, )


#------------------NoticeTemplate-------------------------------
class NoticeCategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = NoticeCategory
        fields = '__all__'

class NoticeCategoryViewSet(viewsets.ModelViewSet):
    queryset = NoticeCategory.objects.all()
    serializer_class = NoticeCategorySerializer
    pagination_class = SelfPagination
    authentication_classes = (CsrfExemptSessionAuthentication, )
    filter_fields = ('typetag','subtypetag')
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('typetag','subtypetag')
    ordering_fields = ('typetag','subtypetag')

class NoticeTemplateSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = NoticeTemplate
        fields = '__all__'

class NoticeTemplateViewSet(viewsets.ModelViewSet):
    queryset = NoticeTemplate.objects.all()
    serializer_class = NoticeTemplateSerializer
    pagination_class = SelfPagination
    authentication_classes = (CsrfExemptSessionAuthentication, )
    filter_fields = ('category__typetag','category__subtypetag')
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('category__typetag','category__subtypetag')
    ordering_fields = ('category__typetag','category__subtypetag')


class NoticeSlotSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = NoticeSlot
        fields = '__all__'

class NoticeSlotViewSet(viewsets.ModelViewSet):
    queryset = NoticeSlot.objects.all()
    serializer_class = NoticeSlotSerializer
    pagination_class = SelfPagination
    authentication_classes = (CsrfExemptSessionAuthentication, )
    filter_fields = ('typetag','subtypetag')
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('typetag','subtypetag')
    ordering_fields = ('typetag','subtypetag')


router = routers.DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'userroles', UserRolesViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'userroleauths', RoleAuthorViewSet)
router.register(r'divisions', DivisionViewSet)
router.register(r'userdivisions', UserDivisionViewSet)

router.register(r'noticecategorys', NoticeCategoryViewSet)
router.register(r'noticetemplates', NoticeTemplateViewSet)
router.register(r'noticeslots', NoticeSlotViewSet)


