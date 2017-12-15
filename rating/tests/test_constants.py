# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rating.views import *
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# Create your tests here.

class ConstantsTests(TestCase):
	def test_current_hostel_valid(self):
		from rating import constants
		hostels = dict(constants.hostels).values()
		self.assertIs(constants.current_hostel in hostels, True)
		