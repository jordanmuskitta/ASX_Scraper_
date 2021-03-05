#Import Library:

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tika import parser
from bs4 import BeautifulSoup as soup
import datetime
import time
from urllib.request import urlretrieve
from urllib.request import urlopen as uReq
import requests
import os
import re
import glob
import pathlib
import io
import tweepy
from numba import jit


def first_scrape():
    #Make original url variable. Make header (to stop anti-scraping software)

    my_url = "https://www.asx.com.au/asx/v2/statistics/todayAnns.do"

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }


    req = requests.get(my_url, headers, allow_redirects = True)

    page_soup = soup(req.content, 'html.parser')
    page_soup

    #Scrape original webpage for specific pdf link redirect:

    link_form = "/asx/statistics/displayAnnouncement.do?display=pdf&idsId="
    links_with_text = []
    for a in page_soup.find_all('a', href=True):
        if a.text:
            links_with_text.append(a['href'])

    filt_links = []

    for i in links_with_text:
        if link_form in i:
            filt_links.append('http://asx.com.au' + i)

    return filt_links

def sec_scrape(filt_links):
    #Get first files and name them dynamically to local.
    #These local files will be block due to auth. However, there is redirect url in these files so...

    filename_list = []

    for i in filt_links:
        filename = i[74:82]
        filename_list.append(filename)
        response = requests.get(i)

        with open(r'pdfs/auth_txt/{}.txt'.format(filename), 'wb') as f:
            f.write(response.content)
            f.close
    return filename_list

def third_scrape(filename_list):


    #Go through each file in the directory and check for the the start of the real url

    real_links = []
    start_search = ('/asxpdf/')

    for i in filename_list:
        with open(r'pdfs/auth_txt/{}.txt'.format(i), 'r') as reader:
            read_txt = reader.readlines()

            for i in read_txt:
                if start_search in i:
                    real_links.append(i)

    #Real url cleaning and appending:

    refined_links = []
    for i in real_links:
        refined_links.append('http://asx.com.au' + i[29:68])

    return refined_links

def download_real_pdf(refined_links, current_date):
    #Save the real pdf to the directory:

    for i in refined_links:
        try:
            pathlib.Path(r'pdfs/raw_pdfs/{}'.format(current_date)).mkdir(parents=True, exist_ok=True)
            refined_filename = i[38:-4]
            urlretrieve(i, r'pdfs/raw_pdfs/{}/{}.pdf'.format(current_date, refined_filename))
        except Exception as err:
            continue
def glob_group(current_date):
    #return all pdfs in folder with glob

    pdfs = glob.glob(r'pdfs/raw_pdfs/{}/*.pdf'.format(current_date))

    return pdfs

def pdf2txt(pdfs, current_date):

    for i in pdfs:
        raw_text = parser.from_file(i, requestOptions={'timeout': 300})
        raw_list = raw_text['content'].splitlines()
        raw_string = ''.join(raw_list)
        refined_filename_txt = i[:-4]
        refined_filename_new = i[-18:-4:]
        pathlib.Path(r'pdfs/txt/{}'.format(current_date)).mkdir(parents=True, exist_ok=True)

        with io.open(r'pdfs/txt/{}/{}.txt'.format(current_date, refined_filename_new), 'w', encoding="utf-8") as txt_read:
            txt_read.write(raw_string)

def vader_analysis(current_date, current_txt_final):

    vader_sent = []

    for i in current_txt_final[-35:]:
        filename_vader = i[-18:-4]

        with open(i, 'r', encoding="utf-8" ) as f:

            analyzer = SentimentIntensityAnalyzer()
            vs = analyzer.polarity_scores(f)
            vader_sent.append('Sentiment for http://asx.com.au/asxpdf/{}/pdf/{}.pdf : {}'.format(current_date,filename_vader, vs))
            f.close()

    return vader_sent

def tweet(vader_sent):
    ##Search a text file for credentials
    #make a for loop
    # Consume:
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''

    # Access:
    ACCESS_TOKEN = ''
    ACCESS_SECRET = ''

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Create API object
    api = tweepy.API(auth)
    hash_tags =  '\n#ASX #trading #fintech #NLP #machinelearning'
    for i in vader_sent:
        try:
            link = i[13:52]
            i = i + hash_tags
            api.update_status(i)

        except tweepy.TweepError as error:
            continue

#Set Current Date:

state = True
while state:
    current_date = datetime.date.today().strftime('%Y%m%d')
    current_time = datetime.datetime.now().strftime('%H%M%S')

    if current_time > '193000':
        print('***ASX Closed: Shutting Down***')
        state = False
    else:
        print('------------------------------')
        filt_links = first_scrape()
        print('***First Scrape Complete***')

        filename_list = sec_scrape(filt_links)
        print('***Second Scrape Complete***')

        refined_links = third_scrape(filename_list)
        print('***Third Scrape Complete***')
        print('\n***Downloading PDFs To Local Drive***')

        download_real_pdf(refined_links, current_date)
        print('***Downloading Complete***')

        pdfs = glob.glob(r'pdfs/raw_pdfs/{}/*.pdf'.format(current_date))
        print('\n***Converting PDF To Text***')

        pdf2txt(pdfs, current_date)
        current_txt_final = glob.glob(r'pdfs/txt/{}/*.txt'.format(current_date))

        print('\n***Performing Sentiment Analysis***')
        sent_list = vader_analysis(current_date, current_txt_final)

        print('***Analysis Complete***')
        tweet(sent_list)

        print('\n***Sending To Twitter***')
        print('***Refreshing Now***\n')
        print('Runtime Completed @ {} {}'.format(current_date, current_time))
        print('------------------------------')
        print('\n'*5)
        time.sleep(5)

        if current_time > '193000':
            print('***ASX Closed: Shutting Down***')
            files = glob.glob(r'pdfs/auth_txt/*')
            for file in files:
                os.remove(file)

            state = False
