# Web_Scraper_Job_Brazilian_websites
Job offers search engine on 4 Brazilian websites.

# What the project does
Perform web scraping of 4 web pages:
https://www.trabalhabrasil.com.br
https://www.vagascertas.com/vagas/vagas/
https://br.indeed.com/
https://www.contratoimediato.com/

For the web scraping of the trabalhabrasil site, selenium is used since the navigation through the page is interactive. Beautiful soup is used for the other websites.

The information is filtered according to a list of keywords.
The links selected by WhatsApp are sent to a phone number. To send messages by WhatsApp,
use selenium as the website is also interactive.

For a good use of the code you must edit the list of keywords that you want to search on the websites and you must enter the phone number to which you want to send the job offers found.

# You need the following libraries:

import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import csv
import random
import re
import pandas as pd
