Analysis
========

Even though several people have worked on RFID Systems, not a single one of those has been installed anywhere. 

Before we started working on this, we spent a lot of time analysing about the same. 

We can do better than an Arduino
--------------------------------

Dont take us wrong, we love arduino. But it is not the right fit for our aim. 

Data
````

Since we stick to Arduino, and it does not have persistent storage, we are going towards SD Card and File I/O. Thus, we are essentially using a `Flat File Database <https://en.wikipedia.org/wiki/Flat_file_database>`_. 

It is easy to see the disadvantages in using a Flat File Database. Data Integrity is not guaranteed, and we have to implement all validations ourselves. There is no strong typing of data - all data is stored as ASCII or Unicode Text. 

The world has moved towards noSQL. We have to atleast use SQL database system. 

Processing
``````````

The Arduino Uno contains a ATmega328P 8 bit micro-controller. Without going into details, an Arduino simply runs a infinitely looped block of code, in a single blocking thread.  

There are convoluted ways to run asynchronous code in an arduino, but they are esoteric and tedious. 

Networking
``````````

Once deploying a system, we would need to maintain it. It would be of great convenience if, the system was connected to network and can be remotely managed. 

This should be doable with Arduino + Ethernet Shield, but, again, it is tedious and esoteric. 

** Thus, we decided to move away from Arduino **

Towards Raspberry Pi
--------------------

Since we decided Arduino was not the right fit, Raspberry Pi was the next natural choice.

In terms of Data, we are able to run MariaDB on the Raspberry Pi, which solves the issues mentioned above. 

The Raspberry Pi 3B+ has BCM2837, a quad-core ARM processor - which leads to amazing processing capabilities. 

Rpi 3B+ has a Ethernet Port and in-built Wifi, which allows for great network connectivity.

Best of all, we are able to run a full linux distro on the raspberry pi, which allows for a great deal of functional scalability.


