Architecture
============



NEED TO REWRITE BELOW TEXT




Once we cemented Rpi as the choice of hardware, we had to make other choices.

We decided to use Python, because,

1. It is a good language
2. Has a large community
3. Lot of open source libraries and softwares

For accessing the GPIO pins of Raspberry Pi, we decided to go with RPi.GPIO library.

For communicating with MFRC522 Reader, we are using `this <https://github.com/mab5vot9us9a/MFRC522-python>`_ library.

For the User Interface, we decided to go with a Web interface. That would be easy to build, and it provides the option of remote access.

For the web interface, we decided to use django. 