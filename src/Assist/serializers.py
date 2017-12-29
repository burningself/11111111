# -*- coding: utf-8 -*-
from rest_framework import routers, serializers, viewsets
from TaskAndFlow.models import *
from UserAndPrj.models import *
from Assist.models import *
from django.contrib.auth.decorators import login_required
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from dss.Serializer import serializer as objtojson
from rest_framework import filters
import rest_framework_filters 
import django_filters

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

#表单相关 pgb
class BiaoDanTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = BiaoDanType
        fields = '__all__'

class BiaoDanTypeViewSet(viewsets.ModelViewSet):
    queryset = BiaoDanType.objects.all()
    serializer_class = BiaoDanTypeSerializer


class BiaoDanMuBanSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = BiaoDanMuBan
        fields = '__all__'

class BiaoDanMuBanViewSet(viewsets.ModelViewSet):
    queryset = BiaoDanMuBan.objects.all()
    serializer_class = BiaoDanMuBanSerializer


class BiaoDanSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = BiaoDan
        fields = '__all__'

class BiaoDanViewSet(viewsets.ModelViewSet):
    queryset = BiaoDan.objects.all()
    serializer_class = BiaoDanSerializer

#文档相关 潘古兵

class DirectorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Directory
        fields = '__all__'

class DirectoryViewSet(viewsets.ModelViewSet):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Document
        fields = '__all__'

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class Doc2RelateSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Doc2Relate
        fields = '__all__'

class Doc2RelateViewSet(viewsets.ModelViewSet):
    queryset = Doc2Relate.objects.all()
    serializer_class = Doc2RelateSerializer

#通知
class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    sendername = serializers.ReadOnlyField(source='sender.truename')
    timeformat = serializers.SerializerMethodField()
    expireformat = serializers.SerializerMethodField()
    relatefilelist = serializers.SerializerMethodField()
    
    def get_timeformat(self,obj):
        return obj.time.strftime('%Y-%m-%d')

    def get_expireformat(self,obj):
        return obj.time.strftime('%Y-%m-%d')

    def get_relatefilelist(self,obj):
        return [objtojson(each.document) for each in Doc2Relate.objects.filter(relatetype="公告", relateid=obj.id)]

    class Meta:
        model = Notice
        fields = '__all__'

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by("-expire")
    serializer_class = NoticeSerializer

#会议
class MeetingroomSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Meetingroom
        fields = '__all__'

class MeetingroomViewSet(viewsets.ModelViewSet):
    queryset = Meetingroom.objects.all()
    serializer_class = MeetingroomSerializer

class MeetingtypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Meetingtype
        fields = '__all__'

class MeetingtypeViewSet(viewsets.ModelViewSet):
    queryset = Meetingtype.objects.all()
    serializer_class = MeetingtypeSerializer
    filter_fields = ('name',)
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name',)

class MeetingSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    hostusername = serializers.ReadOnlyField(source='hostuser.truename')
    meetingtypename = serializers.ReadOnlyField(source='meetingtype.name')
    meetingusers = serializers.SerializerMethodField()

    def get_meetingusers(self,obj):
        return [ {"name":each.user.truename,"isattend":each.isattend,"reason":each.reason,} for each in MeetingUser.objects.filter(meeting_id=obj.id)]

    class Meta:
        model = Meeting
        fields = '__all__'

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def get_queryset(self):
        queryset = Meeting.objects.all()
        meetingid = self.request.query_params.get('id', None)
        if meetingid is not None:
            queryset = queryset.filter(id=meetingid)
        return queryset

class MeetingUserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField(source='user.truename')
    class Meta:
        model = MeetingUser
        fields = '__all__'

class MeetingUserViewSet(viewsets.ModelViewSet):
    queryset = MeetingUser.objects.all()
    serializer_class = MeetingUserSerializer

    def get_queryset(self):
        queryset = MeetingUser.objects.all()
        meetingid = self.request.query_params.get('meetingid', None)
        if meetingid is not None:
            queryset = queryset.filter(meeting_id=meetingid)
        return queryset



router = routers.DefaultRouter()
router.register(r'notices', NoticeViewSet)

router.register(r'directorys', DirectoryViewSet)
router.register(r'documents', DocumentViewSet)

router.register(r'biaodantypes', BiaoDanTypeViewSet)
router.register(r'biaodanmubans', BiaoDanMuBanViewSet)
router.register(r'biaodans', BiaoDanViewSet)

#会议
router.register(r'meetingrooms', MeetingroomViewSet)
router.register(r'meetingtypes', MeetingtypeViewSet)
router.register(r'meetings', MeetingViewSet)
router.register(r'meetingusers', MeetingUserViewSet)

