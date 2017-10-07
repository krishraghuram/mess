## Mess Feedback System using RFID

### Instructions

1) Hardware used
	* Raspberry Pi 3
	* 16 GB SD Card
	* Power supply cable for Pi
	* 3.5 inch screen for RPi
	* MFRC522 RFID card reader
	* HDMI Display, Keyboard and Mouse (For initial setup)

2) Install [Raspbian Stretch](https://www.raspberrypi.org/downloads/raspbian/) on the 16GB SD Card.

3) Open a terminal and run `sudo raspi-config`
	* Change Password to some strong password
	* Localisation Options
		* Change Timezone to "Asia/Kolkata"
		* Change Keyboard Layout to "Dell 101 Key PC". Language is English US. Set defaults for everything else. 
		* Change Wifi Country to India
	* Interfacing Options
		* Enable SSH
		* Enable SPI
	* Advanced Options
		* Expand filesystem
	* Finish and Reboot

4) Setup Networking 
	* Wifi - Just use the GUI to connect
	* Static IP for Ethernet Connection can be set in /etc/dhcpcd.conf
	* For the IP address, you will have to ask your local network admin.
	* Just for good measure, Reboot after these changes

5) Set up proxy
	* In /etc/apt/apt.conf
	* In ~/.bashrc

6) SSH
	* Test SSH
	* Setup key based SSH
	* Disable password based SSH

7) Setup Firewall
	* `sudo apt-get install ufw`
	* Set default rule for incoming data to deny
	* Allow http, https, openssh, and port 8000
	* Enable ufw

8) Setting up MFRC522 Reader and 3.5 Inch Screen
	* Clone https://github.com/krishraghuram/mess-rpisetup
	* Follow all instructions in "Todo" file
	* Complete it and Test it before continuing!!!

9) Install MariaDB and Create databases that will be used by django.
	* sudo apt-get install mariadb-server libmariadbclient-dev
	* sudo mysql -u root
		* CREATE DATABASE mess;
		* CREATE USER 'mess'@'localhost' IDENTIFIED BY 'mess';
		* GRANT ALL PRIVILEGES ON mess . * TO 'mess'@'localhost';
		* FLUSH PRIVILEGES;

10) Clone this repo - https://github.com/krishraghuram/mess.git
	* Go to the project folder
	* sudo -E -H pip install -r requirements.txt
	* Checkout the needed version(using git)

11) Setup and test the django project
	* Go to the project folder
	* python manage.py makemigrations
	* python manage.py migrate
	* python manage.py createsuperuser
	* python manage.py runserver 0.0.0.0:8000
	* Go to a web browser and type '127.0.0.1:8000' and test if the website is working

