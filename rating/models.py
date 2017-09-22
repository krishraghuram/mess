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
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	rfid = models.CharField(max_length=20, unique=True)
	rollno = models.CharField(max_length=20, unique=True)
	name = models.CharField(max_length=100)
	resident_hostel = models.CharField(max_length=20, choices=constants.hostels)
	subscribed_hostel = models.CharField(max_length=20, choices=constants.hostels)

	def __str__(self):
		s = self.name+"("+self.rollno+")"
		return '%s' % (s)





def validate_ratingrange(value):
	if value < constants.rating_low or value > constants.rating_high:
		raise ValidationError(
			'%(value)s is out of bound for rating',
			params={'value': value},
		)

class Activity(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True, unique=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.IntegerField(validators=[validate_ratingrange])

	def get_profile_name(self):
		return str(self.user.profile.name)

	class Meta:
		verbose_name="Activity"
		verbose_name_plural="Activities"