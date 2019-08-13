WIKIPEDIA OF THE DAY

Using Selenium to pull lists of prominent figures, search Wikipedia with a randomly selected element of that list, and send the text of the article as an email

Dependencies:
  Selenium Webdriver - pip install selenium
  chromedriver - Download and add to PATH (https://sites.google.com/a/chromium.org/chromedriver/downloads)
  email.mime - pip install mime

Usage:
  1) Navigate to Repo in Command line
  2) Run python3 start.py -[emailaddress@example.com] -[list type]
  3) The email address argument designates the recipient
  4) The list type designates what type of article you want searched. Current options are "history" and "composers". 
  
 
