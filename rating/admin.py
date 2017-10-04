# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Profile, Activity

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
	fields = ('rfid', 'rollno', 'name', 'resident_hostel', 'subscribed_hostel')
	readonly_fields = ('rfid', 'rollno')
	list_display = ('get_name','rollno')

	def has_add_permission(self, request):
		return False



class ActivityAdmin(admin.ModelAdmin):
	fields = (
		'timestamp', 
		'get_profile_name', 
		'cat_and_punct', 
		'cleanliness',
		'breakfast',
		'lunch',
		'dinner',
		'hostel', 
		'meal'
		)
	readonly_fields = (
		'timestamp', 
		'get_profile_name', 
		'cat_and_punct', 
		'cleanliness',
		'breakfast',
		'lunch',
		'dinner',
		'hostel', 
		'meal'
		)
	list_display = ('timestamp', 'get_profile_name')
	list_filter = ('hostel','meal')

	def has_add_permission(self, request):
		return False



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Activity, ActivityAdmin)



#Unregister the default django models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)
