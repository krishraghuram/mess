#!/usr/bin/env python
# -*- coding: utf8 -*-

##################################
#In this program, we use SPI Bus 0 Channel 1
##################################

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522(dev='/dev/spidev0.1', spd=1000000)

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
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
        print("Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))

        # This is the default key for authentication
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        # Select the scanned tag
        MIFAREReader.SelectTag(uid)

        # Dump the data
        # if your terminal can't display xterm256 colors, use either
        # PrettyDumpClassic1K(key, uid, pretty=False)
        # or
        # DumpClassic1K(key, uid)
        #MIFAREReader.PrettyDumpClassic1K(key, uid)
        text = MIFAREReader.DumpClassic1K_Text(key, uid, print_text=False)
        text = [i for i in text if i is not '\x00']
        text = text[5:] + text[1:5] + text[0:1]
        text = ''.join(text)
        print("Roll Number: "+text)

        MIFAREReader.StopCrypto1()

        continue_reading = False
