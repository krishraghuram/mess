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
import multiprocessing
import time
import constants
from django.db import IntegrityError
import datetime

# Create your views here.

class ReadView(View):
	def get(self, request, *args, **kwargs):
		#Logout if logged in
		if request.user.is_authenticated: 
			logout(request)

		#Try to read card.
		# q = multiprocessing.Queue()
		# p = multiprocessing.Process(target=util.readcard, args=(q,))
		# p.start()
		# # Wait for timeout seconds or until process finishes
		# p.join(constants.read_timeout)
		# # If thread is still active
		# if p.is_alive():
		# 	# Terminate
		# 	p.terminate()
		# 	p.join()
		# 	messages.error(request, "Could not read card. Try again later.")
		# 	return render(request, 'rating/error.html')
		# #Get the card from queue
		# (rfid,rollno) = q.get()
		rfid = 1
		rollno = 1

		#Search for card in Users
		try:
			user = User.objects.get(profile__rfid=rfid)
		except User.DoesNotExist: #If new user
			try:
				#Create a new user object for him
				newuser = User.objects.create_user(username=rollno,password="USELESS_PASS")
			except IntegrityError: #Edge case that occurs when there is inconsistency between Users and Profiles.
				newuser = User.objects.get(username=rollno)
			#We do this so that the user's password can never be used. User's password for all purposes will be the RFID card.
			newuser.set_unusable_password()
			newuser.save()
			#Create a new profile object for the user
			newprofile = Profile(user=newuser, rfid=rfid, rollno=rollno)
			newprofile.save()
			#Send a message to the user and render the error page
			messages.error(request, "New user created. Contact hostel authorities for approval.")
			return render(request, 'rating/error.html')

		#Make sure user has registered with hostel authorities
		p = request.user.profile
		if p.name=='' or p.resident_hostel=='' or p.subscribed_hostel=='':
			messages.error(request, "User details empty. Contact hostel authorities for approval.")
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
			rating = request.POST.get("rating")
			hostel = request.user.profile.subscribed_hostel
			t = datetime.datetime.now()
			if datetime.time(7,0,0) < t.time() < datetime.time(9,30,0):
				meal = "Breakfast"
			elif datetime.time(12,0,0) < t.time() < datetime.time(14,30,0):
				meal = "Lunch"
			elif datetime.time(20,0,0) < t.time() < datetime.time(22,30,0):
				meal = "Dinner"
			else: #User is trying to fill feedback when mess is closed
				messages.error(request, "Mess is closed. Please come back during next meal.")
				return render(request, 'rating/error.html')
			#Save it in activity
			temp = Activity(user=request.user, rating=rating, hostel=hostel, meal=meal)
			temp.save()
			
			#Logout the user
			logout(request)
			#Render a thank you page
			return render(request, 'rating/thankyou.html')





class StartView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'rating/start.html')
