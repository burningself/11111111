# -*- coding: utf-8 -*-
from rest_framework import routers, serializers, viewsets
from TaskAndFlow.models import *
from TaskAndFlow.utility import *
from UserAndPrj.models import *
from Assist.serializers import *
from Scc4PM.restsetings import *
from TaskAndFlow.utility_hazard import *
from django.contrib.auth.decorators import login_required
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters
import rest_framework_filters 
import django_filters




class ZoneSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Zone
        fields = '__all__'

class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    filter_fields = ('major_id','elevations')
    pagination_class = SelfPagination


class UnitProjectSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = UnitProject
        fields = '__all__'

class UnitProjectViewSet(viewsets.ModelViewSet):
    queryset = UnitProject.objects.all()
    serializer_class = UnitProjectSerializer

class ElevationSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Elevation
        fields = '__all__'

class ElevationViewSet(viewsets.ModelViewSet):
    queryset = Elevation.objects.all().order_by('level')
    serializer_class = ElevationSerializer
    pagination_class = SelfPagination
    filter_fields = ('unitproject',)


class StatusCountTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = StatusCountType
        fields = '__all__'

class StatusCountTypeViewSet(viewsets.ModelViewSet):
    queryset = StatusCountType.objects.all()
    serializer_class = StatusCountTypeSerializer


class PBMaterialSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = PBMaterial
        fields = '__all__'

class PBMaterialViewSet(viewsets.ModelViewSet):
    queryset = PBMaterial.objects.all()
    serializer_class = PBMaterialSerializer


class PBTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    majorname = serializers.ReadOnlyField(source='major.name')
    class Meta:
        model = PBType
        fields = '__all__'

class PBTypeViewSet(viewsets.ModelViewSet):
    queryset = PBType.objects.all()
    serializer_class = PBTypeSerializer
    pagination_class = SelfPagination
    filter_fields = ('major','isprebuilt')
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,CustomOrderingFilter,)
    search_fields = ('name',)
    custom_ordering = ('name',)
    ordering_fields = ('name','major','isprebuilt')



class PBStatusSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = PBStatus
        fields = '__all__'

class PBStatusViewSet(viewsets.ModelViewSet):
    queryset = PBStatus.objects.all()
    serializer_class = PBStatusSerializer
    pagination_class = SelfPagination
    filter_fields = ('pbtype__major','pbtype')
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('statusname',)
    ordering_fields = ('sequence',)


class ModelfileSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    relatedunitprojectid = serializers.ReadOnlyField(source='relatedunitproject.id')
    relatedmajorid = serializers.ReadOnlyField(source='relatedmajor.id')
    unitprojectname = serializers.ReadOnlyField(source='relatedunitproject.name')
    majorname = serializers.ReadOnlyField(source='relatedmajor.name')
    class Meta:
        model = Modelfile
        fields = '__all__'

class ModelfileViewSet(viewsets.ModelViewSet):
    queryset = Modelfile.objects.all()
    serializer_class = ModelfileSerializer
    pagination_class = SelfPagination


class PrecastBeamSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    unitprojectname = serializers.ReadOnlyField(source='elevation.unitproject.name')
    elevationname = serializers.ReadOnlyField(source='elevation.name')
    pbtypename = serializers.ReadOnlyField(source='pbtype.name')
    majorname = serializers.ReadOnlyField(source='pbtype.major.name')
    curstatusname = serializers.ReadOnlyField(source='curstatus.statusname')
    class Meta:
        model = PrecastBeam
        fields = '__all__'

class PrecastBeamViewSet(viewsets.ModelViewSet):
    queryset = PrecastBeam.objects.all()
    serializer_class = PrecastBeamSerializer
    pagination_class = SelfPagination

    filter_fields = ('pbtype','pbtype__major','elevation','elevation__unitproject','curstatus')
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('drawnumber','number')
    ordering_fields = ('number', 'pbtype','pbtype__major','elevation','elevation__unitproject','curstatus')
    def get_queryset(self):
        setpb =([each.relatedid for each in Monitoringelement.objects.filter(typetable='构件')])
        queryset = PrecastBeam.objects.filter(id__in=list(setpb))
        return queryset


class PBStatusRecordSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    precastbeam_id = serializers.ReadOnlyField()
    pbnumber = serializers.ReadOnlyField(source='precastbeam.number')
    unitprojectname = serializers.ReadOnlyField(source='precastbeam.elevation.unitproject.name')
    elevationname = serializers.ReadOnlyField(source='precastbeam.elevation.name')
    pbtypename = serializers.ReadOnlyField(source='precastbeam.pbtype.name')
    majorname = serializers.ReadOnlyField(source='precastbeam.pbtype.major.name')
    statusname = serializers.ReadOnlyField(source='status.statusname')
    actorname = serializers.ReadOnlyField(source='actor.truename')
    class Meta:
        model = PBStatusRecord
        fields = '__all__'


class PBStatusRecordFilter(rest_framework_filters.FilterSet):
    class Meta:
        model = PBStatusRecord
        fields = {
            'time': ['lte','gte'],
            'precastbeam__pbtype':['exact'],
            'precastbeam__pbtype__major':['exact'],
            'precastbeam__elevation':['exact'],
            'precastbeam__elevation__unitproject':['exact'],
            'status':['exact'],
        }

class PBStatusRecordViewSet(viewsets.ModelViewSet):
    queryset = PBStatusRecord.objects.all()
    serializer_class = PBStatusRecordSerializer
    
    #filter_fields = ('precastbeam__pbtype','precastbeam__pbtype__major','precastbeam__elevation','precastbeam__elevation__unitproject','status')
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('precastbeam__number',)
    ordering_fields = ('precastbeam__number', 'precastbeam__pbtype','precastbeam__pbtype__major','precastbeam__elevation','precastbeam__elevation__unitproject','status','time')
    filter_class = PBStatusRecordFilter
    pagination_class = SelfPagination

#进度管理相关 pgb
class ConstructiondiarySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField(source='user.truename')
    update_timeformat = serializers.SerializerMethodField()
    related_form = serializers.PrimaryKeyRelatedField(read_only=True)
    related_form_name = serializers.ReadOnlyField(source='related_form.name')
    #related_form = BiaoDanSerializer(read_only=True)
    file = DocumentSerializer(read_only=True)
    
    def get_update_timeformat(self,obj):
        return obj.update_time.strftime('%Y-%m-%d')

    class Meta:
        model = Constructiondiary
        fields = '__all__'

class ConstructiondiaryViewSet(viewsets.ModelViewSet):
    queryset = Constructiondiary.objects.all().order_by("-diary_date")
    pagination_class = SelfPagination
    serializer_class = ConstructiondiarySerializer

    def get_queryset(self):
        queryset = Constructiondiary.objects.all().order_by("-diary_date")
        filterval = self.request.query_params.get('filterval', None)
        if filterval is not None:
              filterval = eval(filterval)
              if filterval["diarytime"]:
                startdate, enddate = GetDateRange(filterval["diarytime"])
                queryset = queryset.filter(diary_date__range=(startdate,enddate))
        return queryset


#------------------------------TaskType-------------------------
class TaskTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = TaskType
        fields = '__all__'

class TaskTypeViewSet(viewsets.ModelViewSet):
    queryset = TaskType.objects.all()
    serializer_class = TaskTypeSerializer

class ProjectTaskSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = ProjectTask
        fields = '__all__'

class ProjectTaskViewSet(viewsets.ModelViewSet):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer


#流程事件
class FlowTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = FlowType
        fields = '__all__'

class FlowTypeViewSet(viewsets.ModelViewSet):
    queryset = FlowType.objects.all()
    serializer_class = FlowTypeSerializer


class FlowTemplateStepSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = FlowTemplateStep
        fields = '__all__'

class FlowTemplateStepViewSet(viewsets.ModelViewSet):
    queryset = FlowTemplateStep.objects.all().order_by('sequence')
    serializer_class = FlowTemplateStepSerializer
    filter_fields = ('template',)
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,)
    search_fields = ('name',)
    authentication_classes = (CsrfExemptSessionAuthentication, )


class FlowTemplateSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    templateSteps = FlowTemplateStepSerializer(many=True,read_only=True)
    class Meta:
        model = FlowTemplate
        fields = '__all__'

class FlowTemplateViewSet(viewsets.ModelViewSet):
    queryset = FlowTemplate.objects.all()
    serializer_class = FlowTemplateSerializer
    filter_fields = ('major','major__name','flowtype','flowtype__name')
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('major', 'flowtype',)
    authentication_classes = (CsrfExemptSessionAuthentication, )


class projecteventSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    createusername = serializers.ReadOnlyField(source='createuser.truename')
    class Meta:
        model = projectevent
        fields = '__all__'

class projecteventViewSet(viewsets.ModelViewSet):
    queryset = projectevent.objects.all()
    serializer_class = projecteventSerializer

    filter_fields = ('id',)
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('number','describe')
    ordering_fields = ('number', 'createtime','deadline')
    authentication_classes = (CsrfExemptSessionAuthentication, )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        #删除文件夹
        dirRelated = getTypeDirectory('quality',instance)
        if dirRelated:
            dirRelated.delete()

        #删除关联文档
        oprlist = EventStepOperation.objects.filter(eventstep__projectevent=instance).values_list('id', flat=True)
        doclist = Doc2Relate.objects.filter(relatetype='事件步骤操作',relateid__in=oprlist).values_list('document_id', flat=True)
        Document.objects.filter(id__in=doclist).delete()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)




#危险源
class HazardlisthistorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Hazardlisthistory
        fields = '__all__'

class HazardlisthistoryViewSet(viewsets.ModelViewSet):
    queryset = Hazardlisthistory.objects.all()
    serializer_class = HazardlisthistorySerializer


class HazardStatusSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = HazardStatus
        fields = '__all__'

class HazardStatusViewSet(viewsets.ModelViewSet):
    queryset = HazardStatus.objects.all()
    serializer_class = HazardStatusSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, )


class HazardeventSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    majorname = serializers.ReadOnlyField(source='major.name')
    statusname = serializers.ReadOnlyField(source='curstatus.statusname')
    weixianyuan = serializers.SerializerMethodField()
    guanlianyuansu = serializers.SerializerMethodField()
    
    def get_weixianyuan(self,obj):
        return objtojson(KnowledgeHazardlist.objects.get(hazard_code=obj.hazard_code))

    def get_guanlianyuansu(self,obj):
        kjys,val = getkjname(obj)
        return kjys

    class Meta:
        model = Hazardevent
        fields = '__all__'

class HazardeventViewSet(viewsets.ModelViewSet):
    queryset = Hazardevent.objects.all()
    serializer_class = HazardeventSerializer

    filter_fields = ('id','curstatus__statusname')
    filter_backends = (filters.DjangoFilterBackend,)
    authentication_classes = (CsrfExemptSessionAuthentication, )

    def get_queryset(self):
        queryset = Hazardevent.objects.all().exclude(curstatus__statusname=u'关闭')
        return queryset


#其他
class MonitoringelementSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Monitoringelement
        fields = '__all__'

class MonitoringelementViewSet(viewsets.ModelViewSet):
    queryset = Monitoringelement.objects.all()
    serializer_class = MonitoringelementSerializer


class TechnicalSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Technical
        fields = '__all__'

class TechnicalViewSet(viewsets.ModelViewSet):
    queryset = Technical.objects.all()
    serializer_class = TechnicalSerializer
    pagination_class = SelfPagination
    filter_fields = ('id',)
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,)
    search_fields = ('name',)

#提醒

class PbstatusremindSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    pbstatusname = serializers.ReadOnlyField(source='pbstatus.statusname')
    pbtypename = serializers.ReadOnlyField(source='pbstatus.pbtype.name')
    next_statusname = serializers.ReadOnlyField(source='next_status.statusname')
    class Meta:
        model = Pbstatusremind
        fields = '__all__'

class PbstatusremindViewSet(viewsets.ModelViewSet):
    queryset = Pbstatusremind.objects.all()
    serializer_class = PbstatusremindSerializer
    filter_fields = ('pbstatus','pbstatus__pbtype')
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('pbstatus__statusname',)
    ordering_fields = ('pbstatus', 'pbstatus__pbtype','next_status')


class AcceptancetypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Acceptancetype
        fields = '__all__'

class AcceptancetypeViewSet(viewsets.ModelViewSet):
    queryset = Acceptancetype.objects.all()
    serializer_class = AcceptancetypeSerializer


class AcceptanceRemindSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    pbstatusname = serializers.ReadOnlyField(source='pbstatus.statusname')
    pbtypename = serializers.ReadOnlyField(source='pbstatus.pbtype.name')
    acceptancetypename = serializers.ReadOnlyField(source='acceptancetype.name')
    class Meta:
        model = AcceptanceRemind
        fields = '__all__'

class AcceptanceRemindViewSet(viewsets.ModelViewSet):
    queryset = AcceptanceRemind.objects.all()
    serializer_class = AcceptanceRemindSerializer
    filter_fields = ('pbstatus','pbstatus__pbtype')
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('pbstatus__statusname',)
    ordering_fields = ('pbstatus', 'pbstatus__pbtype')



router = routers.DefaultRouter()
router.register(r'zones', ZoneViewSet)
router.register(r'unitprojects', UnitProjectViewSet)
router.register(r'elevations', ElevationViewSet)
router.register(r'modelfiles', ModelfileViewSet)
router.register(r'pbstatuss', PBStatusViewSet)
router.register(r'pbmaterials',  PBMaterialViewSet)
router.register(r'pbtypes',  PBTypeViewSet)
router.register(r'statuscounttypes',  StatusCountTypeViewSet)
router.register(r'precastbeam',  PrecastBeamViewSet)
router.register(r'pbstatusrecords',  PBStatusRecordViewSet)


#taskmanager
router.register(r'constructiondiarys', ConstructiondiaryViewSet)
router.register(r'tasktype', TaskTypeViewSet)
router.register(r'projecttaskrest', ProjectTaskViewSet)


#流程事件
router.register(r'flowtypes', FlowTypeViewSet)
router.register(r'flowtemplatesteps', FlowTemplateStepViewSet)
router.register(r'flowtemplates', FlowTemplateViewSet)
router.register(r'projectevents', projecteventViewSet)

#危险源
router.register(r'hazardlisthistorys', HazardlisthistoryViewSet)
router.register(r'hazardevents', HazardeventViewSet)
router.register(r'hazardstatuss', HazardStatusViewSet)

#其他
router.register(r'monitoringelements', MonitoringelementViewSet)
router.register(r'technicals', TechnicalViewSet)

router.register(r'pbstatusreminds', PbstatusremindViewSet)
router.register(r'acceptancetypes', AcceptancetypeViewSet)
router.register(r'acceptancereminds', AcceptanceRemindViewSet)