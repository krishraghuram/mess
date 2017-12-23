7) UFW
	```
	sudo ufw default deny incoming
	sudo ufw allow 22/tcp
	sudo ufw allow 80/tcp
	sudo ufw allow 443/tcp
	sudo ufw allow 8000/tcp
	echo "y" | sudo ufw enable
	sudo ufw status
	```

8) HTPDATE
	```
	sudo apt-get --assume-yes install htpdate
	echo "* * * * * /usr/sbin/htpdate -s intranet.iitg.ernet.in" > mycron
	sudo crontab mycron
	rm mycron
	```