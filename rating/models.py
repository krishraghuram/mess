# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import constants

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
	rollno = models.CharField(max_length=20, unique=True)
	name = models.CharField(max_length=100)
	resident_hostel = models.CharField(max_length=20, choices=constants.hostels)
	subscribed_hostel = models.CharField(max_length=20, choices=constants.hostels)

	def get_name(self):
		if self.name=="" or self.name is None:
			return "New User"+"("+self.rollno+")"
		else: 
			return self.name
	get_name.short_description = "Name"





def validate_ratingrange(value):
	if value < constants.rating_low or value > constants.rating_high:
		raise ValidationError(
			'%(value)s is out of bound for rating',
			params={'value': value},
		)

class Activity(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True, unique=True)
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	# user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	cat_and_punct =   models.IntegerField("Catering and Punctuality" , validators=[validate_ratingrange])
	cleanliness   =   models.IntegerField("Cleanliness"              , validators=[validate_ratingrange])
	breakfast     =   models.IntegerField("Breakfast"                , validators=[validate_ratingrange])
	lunch         =   models.IntegerField("Lunch"                    , validators=[validate_ratingrange])
	dinner        =   models.IntegerField("Dinner"                   , validators=[validate_ratingrange])

	hostel = models.CharField(max_length=20, choices=constants.hostels)

	def get_profile_name(self):
		return str(self.profile.name)
	get_profile_name.short_description = "Profile Name"

	class Meta:
		verbose_name="Activity"
		verbose_name_plural="Activities"