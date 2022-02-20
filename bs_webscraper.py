# bs_webscraper.py
# Author: Rob Dunsmuir
# Date: February 10, 2022
# Purpose: Scrape blog web clients information from local file

from bs4 import BeautifulSoup
import requests, csv, re, os

PATH = os. getcwd() # path for current working directory
output_file = "output.csv" # filename for output
source_file = PATH + '/source.html' # filename for input file

page = open(source_file, encoding="utf8") # load page source
soup = BeautifulSoup(page.read(), features="lxml") # parse page source HTML 


def gather_post_data(post):

	post_data = []

	# data to collect from each post
	post_id = post['id'].split("-")[1] # eg: post_id is post-1654
	post_title = post.h1.text
	post_summary = post.p.text.split(". ")[0] # collect the first sentence of the summary fo simplicity
	post_img = post.img['src'] # collect the post image
	post_url = post.div.h1.a['href'] # collect the url to the post

	# post_date data is contained within 2 divs, need to parse each one and combine
	date_data = post.find("ul", class_="date")
	day = date_data.find("li", class_="day").text
	month = date_data.find("li", class_="month").text
	# no year value was assigned to posts, using 2021 for default
	post_date = f"{month}-{day}-2021"

	post_tags = post.find("li", class_="post_category").text # collect post tags as a comma separated list

	# push all data to list
	post_data.extend((post_id, post_title, post_summary, post_img, post_url, post_date, post_tags))

	return post_data



if __name__ == "__main__":
	csv_file = open(output_file, 'w', newline="") # open output csv file
	csv_writer = csv.writer(csv_file) # set up writer object
	# create heading row for csv file
	csv_writer.writerow(['post_id', 'post_title', 'post_summary', 'post_img', 'post_url', 'post_date', 'post_tags'])

	# collect all client post divs from the page source
	all_posts = soup.find_all("div", attrs={"id": re.compile('post-\d+')})
	# loop through the posts and parse data. return the client post data as a list, and write to the csv
	for post in all_posts:
		csv_writer.writerow(gather_post_data(post))
