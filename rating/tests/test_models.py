# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rating.models import *
from django.db import IntegrityError

# Create your tests here.

class ProfileTests(TestCase):
	def test_user_null(self):
		profile = Profile(rollno="1", name="A", resident_hostel="Umiam", subscribed_hostel="Umiam")
		self.assert_(True)

	def test_user_delete(self):
		#Create user and profile
		user = User(username="username", password="password")
		user.save()
		profile = Profile(user=user, rollno="1", name="A", resident_hostel="Umiam", subscribed_hostel="Umiam")
		profile.save()
		#Delete user and update profile from database
		user.delete()
		profile = Profile.objects.get(rollno="1")
		#Assert
		self.assertIs(profile.user, None)

	def test_rollno_unique(self):
		#Assert
		with self.assertRaisesMessage(IntegrityError, "Duplicate entry '1' for key 'rollno'"):
			profile = Profile(rollno="1", name="A", resident_hostel="Umiam", subscribed_hostel="Umiam")
			profile.save()
			profile2 = Profile(rollno="1", name="B", resident_hostel="Barak", subscribed_hostel="Barak")
			profile2.save()

	def test_pretty_name(self):
		#Test 1
		profile = Profile(rollno="0", name="", resident_hostel="Umiam", subscribed_hostel="Umiam")
		profile.save()
		self.assertEquals(profile.pretty_name(),'New User(0)')
		#Test 2
		profile = Profile(rollno="1", name="A", resident_hostel="Umiam", subscribed_hostel="Umiam")
		profile.save()
		self.assertEquals(profile.pretty_name(),'A')
