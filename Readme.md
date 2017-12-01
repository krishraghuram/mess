## Mess Feedback System using RFID

### License
This Project is Licensed under the GNU GENERAL PUBLIC LICENSE Version 2

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

8) Setup Date and Time Syncing
	* Raspberry Pi does not have an internal clock. Raspbian syncs time using NTP. But IITG firewall blocks this.
	* Thus, we are going to use a different method - htpdate and cron
		* Run `sudo apt-get install htpdate`
		* Run `sudo crontab -e` (If its the first time, you will be asked to choose a text editor. For beginners, nano is the easiest editor to use)
    	* Add this at the bottom of the file
    	`* * * * * /usr/sbin/htpdate -s intranet.iitg.ernet.in`
    	* Save and Exit

9) Setting up MFRC522 Reader and 3.5 Inch Screen
	* Clone https://github.com/krishraghuram/mess-rpisetup
	* Follow all instructions in "Todo" file
	* Complete it and Test it before continuing!!!

10) Install MariaDB and Create databases that will be used by django.
	* sudo apt-get install mariadb-server libmariadbclient-dev
	* sudo mysql -u root
		* CREATE DATABASE mess;
		* CREATE USER 'mess'@'localhost' IDENTIFIED BY 'mess';
		* GRANT ALL PRIVILEGES ON mess . * TO 'mess'@'localhost';
		* FLUSH PRIVILEGES;

11) Clone this repo - https://github.com/krishraghuram/mess.git
	* Go to the project folder
	* sudo -E -H pip install -r requirements.txt
	* Checkout the needed version(using git)

12) Setup and test the django project
	* Go to the project folder
	* `python manage.py makemigrations`
	* `python manage.py migrate`
	* `python manage.py createsuperuser`
	* `python manage.py runserver 0.0.0.0:8000`
	* Go to a web browser and type '127.0.0.1:8000' and test if the website is working

13) Deploy using Gunicorn and Nginx. You can follow this [link](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04).  
The guide uses postgresql, but we plan to use mariadb - so make necessary changes.  
The guide also uses virtual environments, but we dont need to use virtual environment in production - so make necessary adjustments.  
	* Run `sudo apt-get install nginx`
	* Run `sudo -E -H pip install gunicorn`
	* [The django deployment checklist](https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/)  
	The following need to be set with appropriate values.
		* TIME_ZONE - extremely important in checking if mess is open.
		* STATIC_ROOT and STATIC_URL
		* SECRET_KEY
		* Ensure that database password is taken from environment variable, instead of passing it as cleartext in the settings file.
		* DEBUG
		* ALLOWED_HOSTS
		* LOGGING
		* MEDIA_ROOT and MEDIA_URL
	* Secret Key and Database Passwords should be taken from environment.  
	However, gunicorn will not use the variables from bashrc(both user and root do not work) or /etc/environment  
	So, to set env variables for gunicorn - Follow this [link](https://www.digitalocean.com/community/questions/gunicorn-service-can-t-read-environment-variables)  
	**TL; DR instructions**
		* Create a file in `/home/pi/mess` called `django_environment_variables`, and put the following contents.  
		You might need to change the values.
		```
		SECRET_KEY="alkvno39u109jgl1knfocyr9183ryo1hfo1c8n"
		DATABASE_PASSWORD="totallymypass"
		``` 
		* Below, when we create gunicorn.service file, we will add a reference to **/home/pi/mess/django_environment_variables**
		* For running `python manage.py <somecommand>`, you need the SECRET_KEY and DATABASE_PASSWORD in the environment. The simplest way to do this is to add a `export` them from bashrc.
			* `nano ~/.bashrc`
			```
			#Django
			export SECRET_KEY="alkvno39u109jgl1knfocyr9183ryo1hfo1c8n"
			export DATABASE_PASSWORD="mess"
			```
	* Run `python manage.py collectstatic`
	* Test gunicorn by running `gunicorn --bind 0.0.0.0:8000 mess.wsgi`, and checking the website from browser.  
	The website will not have any style, since gunicorn does not know about the CSS responsible for this
	* Create a gunicorn systemd service file and enable it
		* Create a new file by typing `sudo nano /etc/systemd/system/gunicorn.service`
		* This is a sample gunicorn.service file. You might have to make necessary modifications.  
		```
		[Unit]
		Description=gunicorn daemon
		After=network.target

		[Service]
		User=pi
		Group=www-data
		WorkingDirectory=/home/pi/mess
		EnvironmentFile=/home/pi/mess/django_environment_variables
		ExecStart=/usr/local/bin/gunicorn --access-logfile - --workers 1 --bind unix:/home/pi/mess/mess.sock mess.wsgi:application

		[Install]
		WantedBy=multi-user.target
		```
		* Run `sudo systemctl start gunicorn`
		* Run `sudo systemctl enable gunicorn`
	* Setup Nginx
		* Run `sudo nano /etc/nginx/sites-available/mess`
		* This is a sample server block. You might have to make necessary modifications.  
		```
		server {
			listen 80;
			server_name <INSERT IP HERE>;

			location = /favicon.ico { access_log off; log_not_found off; }
			location /static/ {
				root /home/pi/mess;
			}

			location / {
				include proxy_params;
				proxy_pass http://unix:/home/pi/mess/mess.sock;
			}
		}
		```
		* Run `sudo ln -s /etc/nginx/sites-available/mess /etc/nginx/sites-enabled`
		* Run `sudo systemctl restart nginx`
	* Open a browser and check the website. It should be up and running on port 80.  
	If you are facing problems, please check the above link. The guide has some instructions about troubleshooting.

14) Set up RPi to run as a [Kiosk](https://fosskb.in/2017/01/14/building-a-raspberry-pi-kiosk/)
	* Im not writing specific instructions because the blog is very well written. 
	* **Notes**
		* When I tried to use the `while` loop in `.xsession`, it didnt work. 
		* For running `sudo insserv /etc/init.d/aaa` you might need to first install insserv by typing `sudo apt-get install insserv`
	* **Request** : For the splash image, use the IITG Logo
