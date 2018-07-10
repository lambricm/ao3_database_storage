from ao3.search import search
from pathlib import Path
import json
import datetime
from re import sub

"""
	TODO:
		- retrieve chapter data
		- connect to db
			- add data (choose sample fandom
				- check data presence
				- check data correctness
"""


#fandom = "Ergo Proxy (Anime)"
fandom = "Crimson Cross"
db_name = "test_pub"
timestamp_file = db_name + "_timestamp.txt"

#retrieves list of works on same day/after prev. timestamp
# srch -> the search you want to view the works from
# return -> worklist item
def get_worklist(srch):									
	timestamp = format_timestamp(load_timestamp())
	srch.set_date_from(timestamp)
	save_timestamp()
	
	return srch.get_result().get_all_works()
	
#retrieves list of works on same day/after prev. timestamp
# srch -> the search you want to view the works from
# return -> worklist item
def get_work_iterator(srch):									
	timestamp = format_timestamp(load_timestamp())
	srch.set_date_from(timestamp)
	save_timestamp()
	
	return srch.get_result().get_work_iterator()

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
def add_work_data(wrkit):
	print("Adding work data...")
	try:
		wrk = wrkit.next_work()

		while (not (wrk is None)):
			
			work_id = wrk.id
			print("work id: " + str(work_id))
			
			fandoms = wrk.fandoms
			for fandom in fandoms:
				#check if exists in fandom table
				#add if it doesn't
				#get fandom id
				#connect fandom id w/ work id
				print("fandom: " + fandom)
			
			authors = wrk.author
			#for author in authors:
				#check if author exists in author table
				#add if it doesn't
				#get author id
				#connect author id w/ work id
			print("author: " + authors)
			
			tags = wrk.additional_tags
			for tag in tags:
				tag_search = search(tag).get_result()
				parent_tag = tag_search.main_tag
				#check if tag entry exists
				#add tag & parent tag if doesn't exists
				#update parent tag if needed
				#get tag id
				#connect tag & work
				print("tag: " + tag)
				print("parent tag: " + parent_tag)
				
			warnings = wrk.warnings
			for warning in warnings:
				#check exists
				#add if no
				#get id
				#connect w/ fic
				print("warning:" + warning)
				
			ratings = wrk.rating
			for rating in ratings:
				#check exists
				#add if no
				#get id
				#connect w/ fic
				print("rating:" + rating)
				
			relationships = wrk.relationship
			for relationship in relationships:
				#check exists
				#add if no
				#get id
				#connect w/ fic
				print("relationship:" + relationship)
				
			categories = wrk.category
			for categories in categories:
				#check exists
				#add if no
				#get id
				#connect w/ fic
				print("categories:" + categories)
			
			characters = wrk.characters
			for character in characters:
				#check exists
				#add if no
				#get id
				#connect w/ fic
				print("character:" + character)
				
			series = wrk.series
			if not (series is None):
				series_id = series["id"]
				series = series["title"]
				#check exists
				#add if no
				#connect w/ fic
				print("series id, name: " + series_id + ", " + series)
			
			pub_date = wrk.published
			print("publish date: " + str(pub_date))
			
			upd_date = wrk.updated
			print("update date: " + str(upd_date))
			
			words = wrk.words
			print("words: " + str(words))
			
			chapters = wrk.chapters
			total_chapters = chapters["total_chapters"]
			chapters = chapters["num_chapters"]
			print("chapters: " + chapters + "/" + total_chapters)
			
			comments = wrk.comments
			print("comments: " + str(comments))
			
			kudos = wrk.kudos
			print("kudos: " + str(kudos))
			
			bookmarks = wrk.bookmarks
			print("bookmarks: " + str(bookmarks))
			
			hits = wrk.hits
			print("hits: " + str(hits))
			
			title = wrk.title
			print("title: " + title)
			
			summary = wrk.summary
			summary = sub(r"<\/p><p>","\n",summary)
			summary = sub(r"<\/p>|<p>","",summary)
			print("summary: " + summary)

			
			wrk = wrkit.next_work()
	except Exception as e:
		print("ERROR: " + str(e))

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
	
	#with open(pth,'w') as outFile:
	#	outFile.write(json.dumps(timestamp))

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
			
	
	
it = get_work_iterator(search(fandom))
add_work_data(it)

"""
wrk = it.next_work()

while not (wrk is None):
	print(wrk.id)
	wrk = it.next_work()
	
print(len(it.total_works))
"""
