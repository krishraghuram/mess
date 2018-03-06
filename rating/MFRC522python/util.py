#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import time

def readcard(timeout=5):
	#Get starting time
	start = time.time()
	
	#Give power to the RFID reader
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(33, GPIO.OUT)
	GPIO.output(33, True)

	# Create an object of the class MFRC522
	MIFAREReader = MFRC522.MFRC522(dev='/dev/spidev1.2')

	# This loop keeps checking for chips. If one is near it will get the UID and stop
	continue_reading = True
	while continue_reading:
		#Check the time
		if time.time()-start > timeout:
			continue_reading = False

		#Sleep for a sometime so that we dont hog the CPU
		time.sleep(0.1)

		# Scan for cards
		(status, TagType) = MIFAREReader.Request(MIFAREReader.PICC_REQIDL)

		# If a card is found
		if status == MIFAREReader.MI_OK:
			print("Card detected")
		
		# Get the UID of the card
		(status, uid) = MIFAREReader.Anticoll()
		
		# If we have the UID, continue
		if status == MIFAREReader.MI_OK:
			#UID is a list of 4 elements
			#Each element is 8 bit number represented in decimal. 
			#That is, a number between 0-255            
			rfid = uid[0:4]
			
			# This is the default key for authentication
			key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
		
			# Select the scanned tag
			MIFAREReader.SelectTag(uid)
		
			# Dump the data
			text = MIFAREReader.DumpClassic1K_Text(key, uid, print_text=False)
			text = [i for i in text if i!='\x00']
			text = text[5:] + text[1:5] + text[0:1]
			rollno = ''.join(text)

			MIFAREReader.StopCrypto1()
			
			continue_reading = False
			GPIO.output(33, False)
			return (rfid,rollno)

	return None

