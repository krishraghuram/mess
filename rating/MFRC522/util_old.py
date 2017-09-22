#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal

# Capture and Hook the SIGINT
#def sigint(signal, frame):
#    print("Ctrl+C captured, ending read.")
#    GPIO.cleanup()
#signal.signal(signal.SIGINT, sigint)

# Capture SIGINT for cleanup when the script is aborted
def handler(signum, frame):
    GPIO.cleanup()
    raise Exception("readcard() timed out!")

def readcard(timeout=5):
    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    # Register signal function handler
    signal.signal(signal.SIGALRM, handler)

    # Alarm in timeout time
    signal.alarm(timeout)

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    continue_reading = True
    while continue_reading:

        # Scan for cards
        (status, TagType) = MIFAREReader.Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print("Card detected")

        # Get the UID of the card
        (status, uid) = MIFAREReader.Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
            print("Card read UID: " + uid)

            # This is the default key for authentication
            #key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

            # Select the scanned tag
            #MIFAREReader.SelectTag(uid)

            # Dump the data
            #text = MIFAREReader.DumpClassic1K_Text(key, uid, print_text=False)
            #text = [i for i in text if i is not '\x00']
            #text = text[5:] + text[1:5] + text[0:1]
            #text = ''.join(text)
            #print("Roll Number: "+text)

            MIFAREReader.StopCrypto1()

            continue_reading = False

    #Cancel the alarm
    signal.alarm(0)

    #Return the UID
    return uid
    
    
