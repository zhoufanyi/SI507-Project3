from bs4 import BeautifulSoup
import unittest
import requests
import re
import csv

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.

def get_html(title,html = None):
    try:
        page = open(title +'.html','r',encoding = 'utf-8').read()
    except:
        page = requests.get(html).text
        f = open(title +'.html','w',encoding='utf-8')
        f.write(page)
        f.close()
    return page 

# ursulav1_data = get_html('http://newmantaylor.com/gallery.html','ursulav1_data')

# soup1 = BeautifulSoup(ursulav1_data, 'html.parser')
# some_img_elements = soup1.find_all('img')
# for tag in some_img_elements:
# 	if 'alt' in tag.attrs:
# 		print(tag['alt'])
# 	else:
# 		print('No alternative text provided!')

######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable 
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to do this scraping and caching yourself, that is OK.

main_page_data = get_html('nps_gov_data', 'https://www.nps.gov/index.htm')
main_page = BeautifulSoup(main_page_data, 'html.parser')

search_bar = main_page.find(
    'ul', {'class': "dropdown-menu SearchBar-keywordSearch"})
states_information = search_bar.find_all('li')
for information in states_information:
    link = information.find('a')
    if link.text.strip() in ['Arkansas', 'California', 'Michigan']:
        web_address = 'https://www.nps.gov'+link['href']
        file_name = link.text.strip().replace(' ', '_').lower() + '_data'
        get_html(file_name, web_address)


# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure 
# that the rest of the program can access.

# TRY: 
# To open and read all 3 of the files

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data 
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, instead of the full li objects

# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements


# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.


## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's is "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?


# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)


# And then, write each set of data to a file so this won't have to run again.







######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...





## Define your class NationalSite here:
class NationalSite:

    def __init__(self, site_bs):
        self.site = site_bs
        self.location = self.get_location()
        self.name = self.get_name()
        self.type = self.get_type()
        self.description = self.get_description()

    def get_location(self):
        location = self.site.find('h4').text.strip()
        return location

    def get_name(self):
        name = self.site.find('h3').find('a').text.strip()
        return name

    def get_type(self):
        park_type = self.site.find('h2').text.strip()
        return park_type

    def get_description(self):
        description = re.sub('\s',' ',self.site.find('p').text.strip())
        return description

    def get_mailing_address(self):
        web_address = self.site.find_all('a')[1]['href']
        tiltle = self.name.replace(' ', '_').lower() + '_basic_information'
        information_soup = BeautifulSoup(
            get_html(tiltle, web_address), 'html.parser')
        try:
        	post_office_box_number = re.sub('\s',' ',information_soup.find(
            'div', {'class': 'mailing-address'}).find('span',{'itemprop': 'streetAddress'}).text.strip())
        except:
        	post_office_box_number = None
        try:
        	street_address = re.sub('\s',' ',information_soup.find(
            'div', {'class': 'mailing-address'}).find('span',{'itemprop': 'postOfficeBoxNumber'}).text.strip())
        except:
        	street_address = None
        address_locality = re.sub('\s',' ',information_soup.find(
            'div', {'class': 'mailing-address'}).find('span',{'itemprop': 'addressLocality'}).text.strip())
        address_region = re.sub('\s',' ',information_soup.find(
            'div', {'class': 'mailing-address'}).find('span',{'itemprop': 'addressRegion'}).text.strip())
        postal_code = re.sub('\s',' ',information_soup.find(
            'div', {'class': 'mailing-address'}).find('span',{'itemprop': 'postalCode'}).text.strip())
        return ' / '.join(filter(None,[street_address,post_office_box_number,address_locality,address_region,postal_code]))

    def __str__(self):
    	return '{} | {}'.format(self.name,self.location)

    def __contains__(self,input):
    	return input in self.name
        

# f = open("sample_html_of_park.html", 'r', encoding='utf-8')
# soup_inst = NationalSite(BeautifulSoup(f.read(), 'html.parser'))
# print(soup_inst.name)
# print(soup_inst.type)
# print(soup_inst.location)
# print(type(soup_inst.description.encode))
#print('Isle' in soup_inst)
#print(str(soup_inst))
#print(soup_inst.get_mailing_address())
# f.close()



## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:

# f = open("sample_html_of_park.html",'r')
# soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
# sample_inst = NationalSite(soup_park_inst)
# f.close()


######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.

def get_national_site(state_bs):
	stateSite = []
	nationalSiteCollection = state_bs.find('ul', {'id':'list_parks'})
	for nationalSite in nationalSiteCollection.find_all('li',{'class':'clearfix'}):
		stateSite.append(NationalSite(nationalSite))
	return stateSite

arkansas_bs = BeautifulSoup(get_html('arkansas_data'),'html.parser')
california_bs = BeautifulSoup(get_html('california_data'),'html.parser')
michigan_bs = BeautifulSoup(get_html('michigan_data'),'html.parser')

 
arkansas_natl_sites = get_national_site(arkansas_bs)
california_natl_sites = get_national_site(california_bs)
michigan_natl_sites = get_national_site(michigan_bs)

def csv_writer(file_name,site_list):
	with open(file_name,'w', encoding = 'utf-8',newline = '') as csvfile:
		csv_file = csv.writer(csvfile,delimiter = ',')
		csv_file.writerow(['Name','Location','Type','Address','Description'])
		for site in site_list:
			csv_file.writerow([site.name,site.location,site.type,site.get_mailing_address(),site.description])
csv_writer('arkansas.csv',arkansas_natl_sites)
csv_writer('california.csv',california_natl_sites)
csv_writer('michigan.csv',michigan_natl_sites)





##Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)



######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!

