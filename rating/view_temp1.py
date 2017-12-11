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
# from MFRC522python import util
import constants
from django.db import IntegrityError
import datetime

# Create your views here.

class ReadView(View):
	def get(self, request, *args, **kwargs):
		#Logout if logged in
		if request.user.is_authenticated: 
			logout(request)

		# #Try to read card.
		# try:
		# 	data = util.readcard(constants.read_timeout)
		# 	if data and len(data)==2:
		# 		rfid = data[0]
		# 		rollno = data[1]
		# 	else:
		# 		messages.error(request, "Could not read card. Try again later.")
		# 		return render(request, 'rating/error.html')
		# except: #Any kind of exception
		# 	messages.error(request, "Error while reading card. Try once more.")
		# 	return render(request, 'rating/error.html')
		rfid = '1'
		rollno = '130102051'

		#User and Profile creation
		try:
			user = User.objects.get(username=rollno)
		except User.DoesNotExist: 
			try:
				profile = Profile.objects.get(rollno=rollno)
				# If profile exists,
				newuser = User.objects.create_user(username=rollno, password=rfid)
				newuser.save()
				#Set profile.user
				profile.user = newuser
				profile.save()
				#If everything went correctly, set user=newuser, so that we can Login the user below
				user = newuser
			except Profile.DoesNotExist: #If profile does not exist, 
				# Return an error page
				messages.error(request, "HAB Profile not found roll number : "+rollno)
				messages.error(request, "Please contact HAB.")
				return render(request, 'rating/error.html')	

		#Check if the user's profile is proper
		try:
			profile = user.profile
			if profile.rollno!=user.username: 
				messages.error(request, "Roll Number Incorrect in HAB Profile. Please Contact HAB.")
				return render(request, 'rating/error.html')	
			if profile.subscribed_hostel is None:
				messages.error(request, "Subscribed Hostel Empty in HAB Profile. Please Contact HAB.")
				return render(request, 'rating/error.html')	
		except Profile.DoesNotExist: 
			messages.error(request, "HAB Profile not found roll number : "+rollno)
			messages.error(request, "Please contact HAB.")
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
				user=request.user, 
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
