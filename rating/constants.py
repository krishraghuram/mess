
import datetime

#We define all constants of the app "rating" here

#The hostels of IITG
hostels = (
	("Barak","Barak"),
	("Brahmaputra","Brahmaputra"),
	("Dhansiri","Dhansiri"),
	("Dibang","Dibang"),
	("Dihing","Dihing"),
	("Kameng","Kameng"),
	("Kapili","Kapili"),
	("Manas","Manas"),
	("Siang","Siang"),
	("Subansiri","Subansiri"),
	("Umiam","Umiam"),
	("Lohit","Lohit"),
	("Married Scholars","Married Scholars"),
)

#The range of allowed values of ratings.
#Note : The values rating_low and rating_high are included in allowed values.
rating_low = 1
rating_high = 5

#Time to wait for card after "Start" is pressed
read_timeout = 5

#Meal Enum
meals = (
	("Breakfast","Breakfast"),
	("Lunch","Lunch"),
	("Dinner","Dinner"),
)
meal_times = {
	"Breakfast"	:	(datetime.time(7,0,0)  , datetime.time(9,30,0)),
	"Lunch"		:	(datetime.time(12,0,0) , datetime.time(14,30,0)),
	"Dinner"	:	(datetime.time(22,0,0) , datetime.time(22,30,0)),
}