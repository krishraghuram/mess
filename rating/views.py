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
		rfid = '2'
		rollno = '2'

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
		#Check user.password == rfid 
		if not user.check_password(rfid):
			messages.error(request, "RFID incorrect. Did you tamper with your card?")
			return render(request, 'rating/error.html')
		#Check profile.subscribed_hostel!=None or profile.subscribed_hostel!=''
		if profile.subscribed_hostel==None or profile.subscribed_hostel=='':
			messages.error(request, "Subscribed Hostel empty in HAB Profile")
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
