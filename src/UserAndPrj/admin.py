#coding: utf-8
from django.contrib import admin
from django import forms
from UserAndPrj.models import *
from TaskAndFlow.utility import createWXUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

admin.site.disable_action('delete_selected')

# Register your models here.
# 新增用户表单
class UserCreateForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('name', 'contract','truename')

    def clean_password2(self):
        # Check that the two password entries matchauthauth
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        if user.contract:
            createWXUser(user.truename,user.contract,user.company.name)
            
        return user

# 修改用户表单
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        exclude = ()

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserChangeForm, self).save(commit=False)
        user.save()
        if user.contract:
            createWXUser(user.truename,user.contract,user.company.name)
            
        return user

# 注册用户
class MyUserAdmin(UserAdmin):

    form = UserChangeForm
    add_form = UserCreateForm

    list_display = ('name','truename', 'contract','company', 'major','is_admin')
    #list_editable = ('company', 'major',)
    search_fields = ('name','truename')
    list_filter = ('is_admin','major')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {'fields': ('name', 'company','contract', 'password','truename')}),
        ('Personal info', {'fields': ('created_at',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('name', 'password1', 'password2','truename','company','major','contract',),
            }
        ),
    )
    ordering = ('name',)
    filter_horizontal = ()



    
class UserMajorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent',)
    list_editable = ('parent', )
    
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'manager','projecturl')


    

class KnowledgeClassficationAdmin(admin.ModelAdmin):
    list_display = ('classify_name', 'classification_code', 'alias_name','parent','rel_cbim_code','rel_qb_code',)

class KnowledgeHazardlistAdmin(admin.ModelAdmin):
    list_display = ('hazard_code', 'hazard_name', 'hazard_grade','parent','threshold_value','related_property','major','related_classfication_code')


admin.site.register(User, MyUserAdmin)
admin.site.register(UserMajor, UserMajorAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Project, ProjectAdmin)

admin.site.register(KnowledgeClassfication, KnowledgeClassficationAdmin)
admin.site.register(KnowledgeHazardlist, KnowledgeHazardlistAdmin)
