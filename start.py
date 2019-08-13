from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import os
import time
import re
import sys

# For sending emails
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Check to make sure the argument is entered and appropriately formatted
if len(sys.argv) == 1:
    print ("Enter your email address and the type of article you'd like. Like this: \npython3 start.py -[emailaddress@example.com] -[article_type] \nArticle_type options are: \"history\" and \"composers.\"")
    sys.exit()
if not re.match('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', str(sys.argv[1])): #check if email is formatted
    print ("Please input a properly formatted email address")
    sys.exit()
if not re.match('^history$|^composers$', sys.argv[2]):
    print ("Article_type options are: \"history\" and \"composers.\"")
    sys.exit()

# Start Selenium WebDriver
driver = webdriver.Chrome()

# Initialize Famous People List
famous_people_text = []
# Initialize Composer List
composer_text = []

# We utilize a data file to store our list of famous people, so we can remove people for the list as they are searched for
# This if statement checks to see if the file has been populated.
# If not, it populates it. If so, it opens it, and reads Lines into our list

if (sys.argv[2] == "history"):

    if (os.path.getsize('data/famous_people_list.txt') == 0):
        driver.get("https://www.biographyonline.net/people/famous-100.html") # open our list website
        famous_people = driver.find_elements_by_xpath("//section[@class='post-content clearfix']//ol//li/a")
        random.shuffle(famous_people) # randomize the list
        for x in famous_people:
            famous_people_text.append(x.text+ "\n") # populate list
    else:
        with open('data/famous_people_list.txt') as f:
            famous_people_text = f.readlines()

    # Open Wiki
    driver.get("https://www.wikipedia.com")
    wiki_search = driver.find_element_by_id("searchInput")
    wiki_search.send_keys(famous_people_text.pop()) # search for the end of our list on wiki and remove it

    with open('data/famous_people_list.txt', 'w') as file:
        file.writelines(famous_people_text) # rewrite our data file with new list

if (sys.argv[2] == "composers"):

    if (os.path.getsize('data/composer_list.txt') == 0):
        driver.get("https://digitaldreamdoor.com/pages/best-classic-comp.html") # open composer list website
        composers = driver.find_elements_by_xpath("//div[@class='list-classical']/span")
        random.shuffle(composers) # randomize list
        for x in composers:
            composer_text.append(x.text+ "\n") #populate list

    else:
        with open('data/composer_list.txt') as f:
            composer_text = f.readlines()

    # Open Wiki
    driver.get("https://www.wikipedia.com")
    wiki_search = driver.find_element_by_id("searchInput")
    wiki_search.send_keys(composer_text.pop()) # search for the end of our list on wiki and remove it

    with open('data/composer_list.txt', 'w') as file:
        file.writelines(composer_text) # rewrite our data file with new list


time.sleep(2) # wait for the wiki page to load

wiki_info = driver.find_elements_by_xpath("//div[@id='mw-content-text']//div[@class='mw-parser-output']/*[self::p]")

wiki_info_text = []
for x in wiki_info:
    wiki_info_text.append(re.sub('\[\d+\]|\[edit\]|See also|Notes|References|Further reading|External links', '', x.text+ "\n\n")) #pull text from elements and exclude footnotes.

# rewrite our data file with new list
with open('data/wiki_info.txt', 'w') as file:
    file.writelines(wiki_info_text)

# open file in read in order to send email
with open('data/wiki_info.txt', 'r') as file:
    text = file.read()


## Use this section to set up the email.
me = 'WikipediaOfTheDay@gmail.com'
you = sys.argv[1] # use the argument
msg = MIMEMultipart('alternative')
if (sys.argv[2] == "history"):
    msg['Subject'] = "Historical Figure of the Day"
if (sys.argv[2] == "composers"):
    msg['Subject'] = "Classical Composer of the Day"
msg['From'] = me
msg['To'] = you
body = MIMEText(text)
msg.attach(body)


try:
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login(me, 'wikiarticle1234')
    s.sendmail(me, you, msg.as_string())
    s.quit()
except:
    print ('Something went wrong...')
