# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Profile, Activity
import constants
from django.db import IntegrityError
import datetime

def get_card():
	try:
		from MFRC522python import util
		try:
			data = util.readcard(constants.read_timeout)
			if data and len(data)==2:
				rfid = data[0]
				rollno = data[1]
				return (rfid, rollno)
			else:
				messages.error(request, "Could not read card. Try again later.")
				return render(request, 'rating/error.html')
		except: #Any kind of exception
			messages.error(request, "Error while reading card. Try once more.")
			return render(request, 'rating/error.html')
	except: #Not running on R-Pi
		rfid = "1"
		rollno = "1"
		return (rfid, rollno)

# Create your views here.

class ReadView(View):
	def get(self, request, *args, **kwargs):
		#Logout if logged in
		if request.user.is_authenticated: 
			logout(request)

		#Try to read card.
		(rfid,rollno) = get_card()

		#Search for card in Users
		try:
			user = User.objects.get(username=rollno)
			try:
				profile = user.profile
			except Profile.DoesNotExist:
				try:
					profile = Profile.objects.get(rollno=rollno)
					profile.user = user
					profile.save()
				except Profile.DoesNotExist:
					messages.error(request, "HAB Profile does not exist for roll number : "+rollno)
					return render(request, 'rating/error.html')
		#Create User
		except User.DoesNotExist: 
			user = User.objects.create_user(username=rollno,password=rfid)
			user.save()
			try:
				profile = Profile.objects.get(rollno=rollno)
				profile.user = user
				profile.save()
			except Profile.DoesNotExist:
				messages.error(request, "HAB Profile does not exist for roll number : "+rollno)
				return render(request, 'rating/error.html')

		#Validate user and profile
		#Check if user tampered with card
		if not user.check_password(rfid): 
			messages.error(request, "Roll Number or RFID incorrect. Did you tamper with your card?")
			return render(request, 'rating/error.html')
		#Check if subscribed hostel is set properly
		if profile.subscribed_hostel not in dict(constants.hostels).values():
			messages.error(request, "Subscribed Hostel incorrect in HAB Profile")
			return render(request, 'rating/error.html')

		#Login the user
		login(request, user)

		#Redirect to Rating View
		return HttpResponseRedirect(reverse('rating:rating'))





class RatingView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated: 
			return render(request, 'rating/submitrating.html')
		else:
			messages.error(request, "You are not authorized to view this page.")
			return render(request, 'rating/error.html')

	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			#Get the data to be saved
			cat_and_punct  =   request.POST.get("catering_and_punctuality")
			cleanliness    =   request.POST.get("cleanliness")
			breakfast      =   request.POST.get("breakfast")
			lunch          =   request.POST.get("lunch")
			dinner         =   request.POST.get("dinner")
			hostel = request.user.profile.subscribed_hostel

			#Save it in activity
			temp = Activity(
				profile=request.user.profile, 
				cat_and_punct=cat_and_punct, 
				cleanliness=cleanliness,
				breakfast=breakfast,
				lunch=lunch,
				dinner=dinner,
				hostel=hostel
				)
			temp.save()
			
			#Logout the user
			logout(request)
			#Render a thank you page
			return render(request, 'rating/thankyou.html')





class StartView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'rating/start.html')
