import pymongo
from pymongo import MongoClient
import re
client = MongoClient()
#this will work on the local database
db = client.FYP_Airtel_Storage
collect = db.FYP_Capped_Data
new_collection = db.FYP_USSD_Codes
#connect to the database and the correct collection
percent = 0.0
count = 334050000.0
# there was an error with the cursor id not being found this was worked around
#by skipping to the % where it last failed
# I think the failure was due to putting the laptop when it had to be closed
cursor = collect.find().skip(334050000)
ussdarray = cursor[:]
total = cursor.count()
for i in ussdarray:
	count+=1
	code = i["USSD"] 
	if code.startswith('*') and code.endswith('#'): #make sure it is a valid ussd code
		if code.count("*")>1:
			new_code = code.split("*")
			#some codes contained vouchers and were not in the format *xxx# 
			#this has to be adjusted for so the original number xxx can be got and saved
			code = new_code[1]
			code = code.strip("#") #there a few entries where users had mistakingly entered incorrect values which included an extra #
			substringsearch = re.compile(code)
			#search for the number in the USSD collection to ensure no duplicates are entered in the database
			if new_collection.find({"USSD":{'$regex':substringsearch}}).count()==0:
				new_collection.update({"USSD":code},{"USSD":code}, True)
		else:
			code = code.strip('*')
			code = code.strip('#')
			substringsearch = re.compile(code)
			if new_collection.find({"USSD":{'$regex':substringsearch}}).count()==0:
				new_collection.update({"USSD":code},{"USSD":code}, True)
		#the next few lines which should be tidied up into a function, 
		#calculate the % completed 
		if int((count/total)*100) != int(percent): 
			percent = (count/total)*100
			print int(percent), '%'
client.close()

