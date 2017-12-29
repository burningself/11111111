# -*- coding: utf-8 -*-
'''
@author: pgb
'''
from django import forms
from UserAndPrj.models import *
from TaskAndFlow.models import *

class FactoryAreaForm(forms.ModelForm):
    class Meta:
        model = FactoryArea    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(FactoryAreaForm, self).__init__(*args, **kwargs)



class FactoryPositionForm(forms.ModelForm):
    class Meta:
        model = FactoryPosition    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(FactoryPositionForm, self).__init__(*args, **kwargs)



class UnitProjectForm(forms.ModelForm):
    class Meta:
        model = UnitProject    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(UnitProjectForm, self).__init__(*args, **kwargs)



class ElevationForm(forms.ModelForm):
    class Meta:
        model = Elevation    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(ElevationForm, self).__init__(*args, **kwargs)



class PBMaterialForm(forms.ModelForm):
    class Meta:
        model = PBMaterial    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(PBMaterialForm, self).__init__(*args, **kwargs)



class PBTypeForm(forms.ModelForm):
    class Meta:
        model = PBType    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(PBTypeForm, self).__init__(*args, **kwargs)



class PBStatusForm(forms.ModelForm):
    class Meta:
        model = PBStatus    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(PBStatusForm, self).__init__(*args, **kwargs)



class PrecastBeamForm(forms.ModelForm):
    class Meta:
        model = PrecastBeam    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(PrecastBeamForm, self).__init__(*args, **kwargs)



class User2PBStatusForm(forms.ModelForm):
    class Meta:
        model = User2PBStatus    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(User2PBStatusForm, self).__init__(*args, **kwargs)



class PBStatusRecordForm(forms.ModelForm):
    class Meta:
        model = PBStatusRecord    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(PBStatusRecordForm, self).__init__(*args, **kwargs)



class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(TaskTypeForm, self).__init__(*args, **kwargs)



class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = TaskStatus    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(TaskStatusForm, self).__init__(*args, **kwargs)



class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(ProjectTaskForm, self).__init__(*args, **kwargs)



class User2TaskStatusForm(forms.ModelForm):
    class Meta:
        model = User2TaskStatus    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(User2TaskStatusForm, self).__init__(*args, **kwargs)



class TaskStatusRecordForm(forms.ModelForm):
    class Meta:
        model = TaskStatusRecord    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(TaskStatusRecordForm, self).__init__(*args, **kwargs)



class FlowTypeForm(forms.ModelForm):
    class Meta:
        model = FlowType    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(FlowTypeForm, self).__init__(*args, **kwargs)



class FlowTemplateForm(forms.ModelForm):
    class Meta:
        model = FlowTemplate    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(FlowTemplateForm, self).__init__(*args, **kwargs)



class FlowTemplateStepForm(forms.ModelForm):
    defaultcomment = forms.CharField(label='审批意见',widget=forms.Textarea(attrs={ 'rows':'2'}))
    class Meta:
        model = FlowTemplateStep
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(FlowTemplateStepForm, self).__init__(*args, **kwargs)

class FlowTemplateUpdateStepForm(forms.ModelForm):
    defaultcomment = forms.CharField(label='审批意见',widget=forms.Textarea(attrs={ 'rows':'2'}))
    class Meta:
        model = FlowTemplateStep    
        exclude = ['isautotransfer','istimeouttransfer'] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(FlowTemplateUpdateStepForm, self).__init__(*args, **kwargs)
        self.fields['template'].required = False
        self.fields['sequence'].required = False

class FlowStepUserForm(forms.ModelForm):
    class Meta:
        model = FlowStepUser    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(FlowStepUserForm, self).__init__(*args, **kwargs)



class ActorTypeForm(forms.ModelForm):
    class Meta:
        model = ActorType    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(ActorTypeForm, self).__init__(*args, **kwargs)



class FlowStepOperationForm(forms.ModelForm):
    class Meta:
        model = FlowStepOperation    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(FlowStepOperationForm, self).__init__(*args, **kwargs)




class EventstepForm(forms.ModelForm):
    class Meta:
        model = Eventstep    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(EventstepForm, self).__init__(*args, **kwargs)



class EventStepOperationForm(forms.ModelForm):
    class Meta:
        model = EventStepOperation    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(EventStepOperationForm, self).__init__(*args, **kwargs)



class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(DirectoryForm, self).__init__(*args, **kwargs)



class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)



class Doc2RelateForm(forms.ModelForm):
    class Meta:
        model = Doc2Relate    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(Doc2RelateForm, self).__init__(*args, **kwargs)



class CMTypeForm(forms.ModelForm):
    class Meta:
        model = CMType    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(CMTypeForm, self).__init__(*args, **kwargs)



class CMStatusForm(forms.ModelForm):
    class Meta:
        model = CMStatus    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(CMStatusForm, self).__init__(*args, **kwargs)



class ConstructionMachineForm(forms.ModelForm):
    class Meta:
        model = ConstructionMachine    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(ConstructionMachineForm, self).__init__(*args, **kwargs)



class User2CMStatusForm(forms.ModelForm):
    class Meta:
        model = User2CMStatus    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(User2CMStatusForm, self).__init__(*args, **kwargs)



class CMStatusRecordForm(forms.ModelForm):
    class Meta:
        model = CMStatusRecord    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(CMStatusRecordForm, self).__init__(*args, **kwargs)



class HazardTypeForm(forms.ModelForm):
    class Meta:
        model = HazardType    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(HazardTypeForm, self).__init__(*args, **kwargs)



class HazardStatusForm(forms.ModelForm):
    class Meta:
        model = HazardStatus    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(HazardStatusForm, self).__init__(*args, **kwargs)


class User2HazardStatusForm(forms.ModelForm):
    class Meta:
        model = User2HazardStatus    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(User2HazardStatusForm, self).__init__(*args, **kwargs)



class HazardStatusRecordForm(forms.ModelForm):
    class Meta:
        model = HazardStatusRecord    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(HazardStatusRecordForm, self).__init__(*args, **kwargs)



class MessageTypeForm(forms.ModelForm):
    class Meta:
        model = MessageType    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(MessageTypeForm, self).__init__(*args, **kwargs)



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice    
        exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)

class Upload_Status_Form(forms.Form):
    goujian = forms.CharField(max_length=50, required=True, error_messages={'required':u'元素编号不能为空'})
    duichang = forms.CharField(max_length=10, required=False, error_messages={'required':u'请选择堆场'})
    zhijian = forms.CharField(max_length=100, required=False)
    beizhu = forms.CharField(max_length=100, required=False)
    status = forms.CharField(max_length=10, required=True, error_messages={'required':u'请选择状态'})
    
    def clean(self):
        cleaned_data = super(Upload_Status_Form, self).clean()
        return cleaned_data
    
    
class Upload_Photo_Form(forms.Form):
    goujian = forms.CharField(max_length=50, required=True, error_messages={'required':u'元素编号不能为空'})
    title = forms.CharField(max_length=40)
    content=forms.CharField(max_length=200,required=True)
    
    def clean(self):
        cleaned_data = super(Upload_Status_Form, self).clean()
        status_msg = u"请选择够级"
        self._errors["status"] = self.error_class([status_msg])
        return cleaned_data


class projecteventForm(forms.ModelForm):
    photoUrl = forms.CharField(required=False,label=u"添加附件",widget=forms.TextInput({"placeholder":"选取附件","readonly":"true"}))
    relateNum = forms.CharField(required=False,label=u"关联元素")
    describe = forms.CharField(required=True,label=u"问题描述",widget=forms.Textarea({"rows":3}))
    class Meta:
        model = projectevent 
        
        exclude = [] # uncomment this line and specify any field to exclude it from the form
        fields = ['number', 'template','relateNum','curflowstep','priority','deadline','describe','photoUrl','issave']  
        
    def __init__(self, *args, **kwargs):
        super(projecteventForm, self).__init__(*args, **kwargs)
        self.fields['curflowstep'].required = False
        self.fields['deadline'].required = False
        self.fields['deadline'].widget.attrs["readonly"]="true";
    
    def clean_curflowstep(self):
        return 0
    
    def clean_relateNum(self):
        return self.cleaned_data["relateNum"]
    
    def clean(self):
        cleaned_data = super(projecteventForm, self).clean()
        cleaned_data["curflowstep"] = FlowTemplateStep.objects.get(template=self.cleaned_data["template"],isstartstep=True)

        return cleaned_data

class editProjecteventForm(forms.ModelForm):
    relateNum = forms.CharField(required=False,label=u"关联元素")
    class Meta:
        model = projectevent 
        
        exclude = [] # uncomment this line and specify any field to exclude it from the form
        fields = ['number', 'template','relateNum','curflowstep','priority','deadline','describe']  
        
    def __init__(self, *args, **kwargs):
        super(editProjecteventForm, self).__init__(*args, **kwargs)
        self.fields['curflowstep'].required = False
        self.fields['deadline'].required = False
        self.fields['deadline'].widget.attrs["readonly"]="true";
    
    def clean(self):
        cleaned_data = super(editProjecteventForm, self).clean()
        cleaned_data["relateNum"] = PrecastBeam.objects.filter(sign=cleaned_data["relateNum"])[0].id
        return cleaned_data
    
    def full_clean(self):
        super(editProjecteventForm, self).full_clean()
        print self._errors


class Upload_Status_Form(forms.Form):
    goujian = forms.CharField(max_length=50, required=True, error_messages={'required':u'元素编号不能为空'})
    duichang = forms.CharField(max_length=10, required=False, error_messages={'required':u'请选择堆场'})
    zhijian = forms.CharField(max_length=100, required=False)
    beizhu = forms.CharField(max_length=100, required=False)
    status = forms.CharField(max_length=10, required=True, error_messages={'required':u'请选择状态'})
    
    def clean(self):
        cleaned_data = super(Upload_Status_Form, self).clean()
        return cleaned_data
    
    
class Upload_Photo_Form(forms.Form):
    goujian = forms.CharField(max_length=50, required=True, error_messages={'required':u'构件编号不能为空'})
    title = forms.CharField(max_length=40)
    content=forms.CharField(max_length=200,required=True)
    
    def clean(self):
        cleaned_data = super(Upload_Status_Form, self).clean()
        status_msg = u"请选择够级"
        self._errors["status"] = self.error_class([status_msg])
        return cleaned_data