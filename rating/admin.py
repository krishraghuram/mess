# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Profile, Activity

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
	fields = ('rfid', 'rollno', 'name', 'resident_hostel', 'subscribed_hostel')
	readonly_fields = ('rfid', 'rollno')
	list_display = ('name','rollno')

	def has_add_permission(self, request):
		return False



class ActivityAdmin(admin.ModelAdmin):
	fields = ('timestamp', 'get_profile', 'rating')
	readonly_fields = ('timestamp', 'get_profile', 'rating')
	list_display = ('timestamp', 'get_profile', 'rating')
	
	def has_add_permission(self, request):
		return False



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Activity, ActivityAdmin)
