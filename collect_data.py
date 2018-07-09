from ao3.search import search
from pathlib import Path
import json
import datetime

"""
	TODO:
		- add work note retrieval to 'works' class
		- retrieve chapter data
			- also clear up any problems & add new data retrieval if needed in chapter class
		- connect to db
			- add data
				- check data presence
				- check data correctness
"""


#fandom = "Ergo Proxy (Anime)"
fandom = "Undertale (Video Game)"
db_name = "ergo_proxy_pub"
timestamp_file = db_name + "_timestamp.txt"

#retrieves list of works on same day/after prev. timestamp
# srch -> the search you want to view the works from
# return -> worklist item
def get_worklist(srch):									
	timestamp = format_timestamp(load_timestamp())
	srch.set_date_from(timestamp)
	save_timestamp()
	
	return srch.get_result().get_all_works()

# prints all ids in worklist (used for testing)
def print_work_ids(wrklst):
	try:
		wrk = wrklst.next_work

		while (not (wrk is None)):
			print(wrk.id)
			wrk = wrklst.next_work
	except:
		print("Error: no works in worklist")
	
#CURRENTLY ONLY RETRIEVES DATA
# wrklst -> retrieved worklist from search
def add_work_data(wrklst):
	try:
		wrk = wrklst.next_work

		while (not (wrk is None)):
			id = wrk.id
			fandoms = wrk.fandoms
			authors = wrk.author
			tags = wrk.additional_tags
			warnings = wrk.warnings
			ratings = wrk.rating
			relationships = wrk.relationship
			characters = wrk.characters
			series = wrk.series
			series_id = series["id"]
			series = series["title"]
			pub_date = wrk.published
			upd_date = wrk.updated
			words = wrk.words
			chapters = wrk.chapters
			total_chapters = chapters["total_chapters"]
			chapters = chapters["num_chapters"]
			comments = wrk.comments
			kudos = wrk.kudos
			bookmarks = wrk.bookmarks
			hits = wrk.hits
			title = wrk.title
			#note1
			#note2
			summary = wrk.summary
						
	except:
		print("Error: no works in worklist")

#ensures file exists
# pth -> file to check
def check_file(pth):
	return Path(pth).is_file()

#loads previous timestamp - don't want to get data that hasn't been updated since our last data retrieval
# return - timestamp
def load_timestamp():
	ret = None
	pth = "./" + timestamp_file
	
	if check_file(pth):
		with open(pth, 'r') as inFile:
			try:
				json_data = json.loads(inFile.read())
				if "timestamp" in json_data:
					ret = json_data["timestamp"]
			except:
				ret = None
	
	return ret
	
#saves current date as timestamp
def save_timestamp():
	pth = "./" + timestamp_file
	
	curr_date = datetime.date.today()
	timestamp = {"timestamp":{"year":curr_date.year, "month":curr_date.month, "day":curr_date.day}}
	
	with open(pth,'w') as outFile:
		outFile.write(json.dumps(timestamp))

#formats the timestamp for ao3 search compatability
# timestamp -> loaded timestamp
# return -> text ready for ao3 search class
def format_timestamp(timestamp):
	date_str = ""
	
	if not (timestamp is None):
		try:
			year = str(timestamp["year"])
			month = str(timestamp["month"])
			day = str(timestamp["day"])
			
			while len(month) < 2:
				month = "0" + month
			while len(day) < 2:
				day = "0" + day
				
			date_str = year + "-" + month + "-" + day
		except:
			return ""
			
	return date_str
			
	
res = get_worklist(search(fandom))
