from import_export import resources, fields
from .models import Profile, Activity

class ProfileResource(resources.ModelResource):
	rollno 				= fields.Field(attribute = 'rollno', column_name = 'Roll Number') #Ensure rollno cannot be imported
	name 				= fields.Field(attribute = 'name', column_name = 'Name')
	resident_hostel 	= fields.Field(attribute = 'resident_hostel', column_name = 'Resident Hostel')
	subscribed_hostel 	= fields.Field(attribute = 'subscribed_hostel', column_name = 'Subscribed Hostel')

	class Meta:
		model = Profile
		skip_unchanged = True #Dont import unchanged fields
		fields = ('rollno', 'name', 'resident_hostel', 'subscribed_hostel') #Whitelist fields to be import/exported
		export_order = ('rollno', 'name', 'resident_hostel', 'subscribed_hostel') #Needed because we are using column_name(s)
		import_id_fields = ('rollno',) #Use rollno as primary key while importing





class ActivityResource(resources.ModelResource):
	timestamp 			= fields.Field(attribute = 'timestamp', column_name = 'Time Stamp', readonly = True)
	get_profile_name 	= fields.Field(attribute = 'get_profile_name', column_name = 'Profile Name', readonly = True)
	hostel 				= fields.Field(attribute = 'hostel', column_name = 'Hostel', readonly = True)
	cat_and_punct 		= fields.Field(attribute = 'cat_and_punct', column_name = 'Catering and Punctuality', readonly = True)
	cleanliness 		= fields.Field(attribute = 'cleanliness', column_name = 'Cleanliness', readonly = True)
	breakfast 			= fields.Field(attribute = 'breakfast', column_name = 'Breakfast', readonly = True)
	lunch 				= fields.Field(attribute = 'lunch', column_name = 'Lunch', readonly = True)
	dinner 				= fields.Field(attribute = 'dinner', column_name = 'Dinner', readonly = True)

	class Meta:
		model = Activity
		skip_unchanged = True
		fields = ('timestamp', 'get_profile_name', 'hostel', 'cat_and_punct', 'cleanliness', 'breakfast', 'lunch', 'dinner')
		export_order = ('timestamp', 'get_profile_name', 'hostel', 'cat_and_punct', 'cleanliness', 'breakfast', 'lunch', 'dinner')

	def dehydrate_timestamp(self, activity):
		return activity.timestamp.strftime('%Y%m%d%H%M%S')