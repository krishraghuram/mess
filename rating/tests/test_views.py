# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rating.views import *
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# Create your tests here.

class ReadTests(TestCase):
	###########################################
	###General Tests
	###########################################
	def test_logout_if_logged_in(self):
		#Setup
		user = User(username="username", password="password")
		user.save()
		self.client.login(username="username", password="password")
		#Test
		response = self.client.get(reverse("rating:start"), follow=True)
		#Assert
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "Start")


	###########################################
	###User Profile Relation Tests
	###########################################
	#User Does Not Exist, Profile Does Not Exist
	def test_user_dne_profile_dne(self):
		#Client Action
		response = self.client.get(reverse("rating:read")+"?rfid=1&rollno=1", follow=True)
		#Assert profile not found error
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "HAB Profile does not exist for roll number : 1")
		#Asser user created
		user = User.objects.get(username="1")
		self.assertIsNotNone(user)

	#User Does Not Exist, Profile Exists	
	def test_user_dne_profile_e(self):
		#Client Action
		profile = Profile(rollno="1", name="A", resident_hostel="Umiam", subscribed_hostel="Umiam")
		profile.save()
		response = self.client.get(reverse("rating:read")+"?rfid=1&rollno=1", follow=True)
		#Assert no error
		self.assertEquals(response.status_code, 200)
		#Assert user profile relation
		user = User.objects.get(username="1")
		profile = Profile.objects.get(rollno="1")
		self.assertEquals(user, profile.user)
		self.assertEquals(profile, user.profile)

	#User Exists, User.profile Exists
	def test_user_e_userprofile_e(self):
		#Client Action
		profile = Profile(rollno="1", name="A", resident_hostel="Umiam", subscribed_hostel="Umiam")
		profile.save()
		response = self.client.get(reverse("rating:read")+"?rfid=1&rollno=1", follow=True)
		#Assert no error
		self.assertEquals(response.status_code, 200)
		#Assert user profile relation
		user = User.objects.get(username="1")
		profile = Profile.objects.get(rollno="1")
		self.assertEquals(user, profile.user)
		self.assertEquals(profile, user.profile)
		#Client Action
		response = self.client.get(reverse("rating:read")+"?rfid=1&rollno=1", follow=True)
		#Assert no error
		self.assertEquals(response.status_code, 200)

	#User Exists, User.profile Does Not Exist, Profile Does Not Exist
	def test_user_e_userprofile_dne_profile_dne(self):
		#Client Action
		profile = Profile(rollno="1", name="A", resident_hostel="Umiam", subscribed_hostel="Umiam")
		profile.save()
		response = self.client.get(reverse("rating:read")+"?rfid=1&rollno=1", follow=True)
		#Assert no error
		self.assertEquals(response.status_code, 200)
		#Assert user profile relation
		user = User.objects.get(username="1")
		profile = Profile.objects.get(rollno="1")
		self.assertEquals(user, profile.user)
		self.assertEquals(profile, user.profile)
		#Client Action
		profile.delete()
		response = self.client.get(reverse("rating:read")+"?rfid=1&rollno=1", follow=True)
		#Assert profile not found error
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "HAB Profile does not exist for roll number : 1")

	#User Exists, User.profile Does Not Exist, Profile Exists
	def test_user_e_userprofile_dne_profile_e(self):
		#Client Action
		profile = Profile(rollno="1", name="A", resident_hostel="Umiam", subscribed_hostel="Umiam")
		profile.save()
		response = self.client.get(reverse("rating:read")+"?rfid=1&rollno=1", follow=True)
		#Assert no error
		self.assertEquals(response.status_code, 200)
		#Assert user profile relation
		user = User.objects.get(username="1")
		profile = Profile.objects.get(rollno="1")
		self.assertEquals(user, profile.user)
		self.assertEquals(profile, user.profile)
		#Client Action
		profile.delete()
		response = self.client.get(reverse("rating:read")+"?rfid=1&rollno=1", follow=True)
		#Assert profile not found error
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "HAB Profile does not exist for roll number : 1")
		#Client Action
		profile = Profile(rollno="1", name="B", resident_hostel="Barak", subscribed_hostel="Barak")
		profile.save()		
		response = self.client.get(reverse("rating:read")+"?rfid=1&rollno=1", follow=True)
		#Assert no error
		self.assertEquals(response.status_code, 200)
		#Asser user profile relation
		user = User.objects.get(username="1")
		profile = Profile.objects.get(rollno="1")
		self.assertEquals(user, profile.user)
		self.assertEquals(profile, user.profile)



	###########################################
	###Profile Validation in ReadView
	###########################################
	def test_resident_hostel_empty(self):
		#Client Action
		profile = Profile(rollno="1", name="A", resident_hostel="", subscribed_hostel="Umiam")
		profile.save()
		response = self.client.get(reverse("rating:read")+"?rfid=1&rollno=1", follow=True)
		#Assert field cannot be blank
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "This field cannot be blank")

	def test_subscribed_hostel_empty(self):	
		#Client Action
		profile = Profile(rollno="1", name="A", resident_hostel="Umiam", subscribed_hostel="")
		profile.save()
		response = self.client.get(reverse("rating:read")+"?rfid=1&rollno=1", follow=True)
		#Assert field cannot be blank
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "This field cannot be blank")

	def test_resident_hostel_invalid(self):
		#Client Action
		profile = Profile(rollno="1", name="A", resident_hostel="INVALID", subscribed_hostel="Umiam")
		profile.save()
		response = self.client.get(reverse("rating:read")+"?rfid=1&rollno=1", follow=True)
		#Assert invalid choice
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "is not a valid choice.")

	def test_subscribed_hostel_invalid(self):	
		#Client Action
		profile = Profile(rollno="1", name="A", resident_hostel="Umiam", subscribed_hostel="INVALID")
		profile.save()
		response = self.client.get(reverse("rating:read")+"?rfid=1&rollno=1", follow=True)
		#Assert invalid choice
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "is not a valid choice.")

















class RatingTests(TestCase):
	###########################################
	###Get Requests
	###########################################
	def test_get_logged_out(self):
		#Test
		response = self.client.get(reverse("rating:rating"), follow=True)
		#Assert
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "You are not authorized to view this page")

	def test_get_logged_in(self):
		#Setup
		user = User.objects.create_user(username="username", password="password")
		self.client.login(username="username", password="password")
		#Test
		response = self.client.get(reverse("rating:rating"), follow=True)
		#Assert
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "Welcome")

	###########################################
	###Post Requests
	###########################################
	def test_post_logged_out(self):
		#Test
		data = {
		"catering_and_punctuality" : "1",
		"cleanliness" : "1",
		"breakfast" : "1",
		"lunch" : "1",
		"dinner" : "1"
		}
		response = self.client.post(reverse("rating:rating"), data, follow=True)
		#Assert
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "You are not authorized to access this")

	def test_post_logged_in(self):
		#Setup
		user = User.objects.create_user(username="1", password="password")
		profile = Profile(user=user, rollno="1", name="A", resident_hostel="Umiam", subscribed_hostel="Umiam")
		profile.save()
		self.client.login(username="1", password="password")
		#Test
		data = {
		"catering_and_punctuality" : "1",
		"cleanliness" : "1",
		"breakfast" : "1",
		"lunch" : "1",
		"dinner" : "1"
		}
		response = self.client.post(reverse("rating:rating"), data, follow=True)
		#Assert
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "Thank you")

	###########################################
	###Activity Validation Tests
	###########################################
	def test_rating_range(self):
		#Setup
		n_test_cases = 1000
		user = User.objects.create_user(username="1", password="password")
		profile = Profile(user=user, rollno="1", name="A", resident_hostel="Umiam", subscribed_hostel="Umiam")
		profile.save()
		
		#Tests
		fields = ["catering_and_punctuality", "cleanliness", "breakfast", "lunch", "dinner"]		
		correct_inputs = ['0', '5']
		wrong_inputs = ['-1', '6', '', 'ASD', None]
		inputs = correct_inputs + wrong_inputs
		import itertools
		values = list(itertools.product(inputs, inputs, inputs, inputs, inputs))
		import random
		choices = random.sample(range(len(values)), n_test_cases)
		values = [values[i] for i in choices]
		for (index,i) in enumerate(values):
			data = dict(zip(fields, i))
			data = dict([(j,data[j]) for j in data if data[j] is not None])
			self.client.login(username="1", password="password")
			response = self.client.post(reverse("rating:rating"), data, follow=True)
			if any(j in wrong_inputs for j in data.values()):
				self.assertEquals(response.status_code, 200)
				self.assertContains(response, "Activity Validation Error")
			elif len(data)==5 and all(j in correct_inputs for j in data.values()):
				self.assertEquals(response.status_code, 200)
				self.assertContains(response, "Thank you")












class RatingTests(TestCase):
	def test_get(self):
		#Test
		response = self.client.get(reverse("rating:start"), follow=True)
		#Assert
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "Start")
