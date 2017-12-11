# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ExportMixin
from .resources import ProfileResource, ActivityResource
from .models import Profile, Activity

# Register your models here.

class ProfileAdmin(ImportExportModelAdmin):
	resource_class = ProfileResource
	fields = ('rollno', 'name', 'resident_hostel', 'subscribed_hostel')
	list_display = ('get_name','rollno')





class ActivityAdmin(ExportMixin, admin.ModelAdmin):
	resource_class = ActivityResource
	fields = (
		'timestamp', 
		'get_profile_name', 
		'cat_and_punct', 
		'cleanliness',
		'breakfast',
		'lunch',
		'dinner',
		'hostel'
		)
	readonly_fields = (
		'timestamp', 
		'get_profile_name', 
		'cat_and_punct', 
		'cleanliness',
		'breakfast',
		'lunch',
		'dinner',
		'hostel'
		)
	list_display = ('timestamp', 'get_profile_name')
	list_filter = ('hostel',)

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Activity, ActivityAdmin)



#Unregister the default django models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# admin.site.unregister(User)
# admin.site.unregister(Group)
