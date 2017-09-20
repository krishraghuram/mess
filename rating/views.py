# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Activity
from MFRC522python import util

# Create your views here.

class ReadView(View):
	def get(self, request, *args, **kwargs):
		#Logout if logged in
		if request.user.is_authenticated: 
			logout(request)

		#Try to read card.
		try:
			# rfid = util.readcard()
			# rfid = "2294023316" #Raghu
			rfid = "19711232168" #MAK
		except Exception as e:
			messages.error(request, "Could not read card. Try again later.")
			return render(request, 'rating/error.html')

		#Search for card in Users
		try:
			user = User.objects.get(profile__rfid=rfid)
		except User.DoesNotExist: #New User
			messages.error(request, "User does not exist")
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
			#Get the rating
			print request.POST
			rating = request.POST.get("rating")
			#Save it in activity
			temp = Activity(user=request.user, rating=rating)
			temp.save()
			#Logout the user
			logout(request)
			#Render a thank you page
			return render(request, 'rating/thankyou.html')





class StartView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'rating/start.html')
