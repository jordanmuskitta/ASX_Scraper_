## Welcome to my ASX Announcement Scraper + Sentiment Analysis Twitter Bot
_Authors: Jordan Muskitta_

### Program Objectives: 

- Decipher the structure and content of HTML
- Use Beautiful Soup to parse HTML
- Download pdfs locally
- Convert pdf to txt
- Analyze text for sentiment

### Introduction

This project uses a wide array of third-party python libraries. However, the bulk of the project will be using in-built python functions and common coding approaches such as loops, string and list manipulations methods.

Some of the choices for parsing and handling pdfs forced due to errors been thrown with use of other more popular pdf extraction libraries such as PyPDF2 and PDFminer. These errors were due to the PDF's encryption? Even though the PDF is accessible, there is an underlying encryption that stops PDFminer and PyPDF2 from extracting text.

Documentation for imported libraries: 

- Vader Sentiment: https://github.com/cjhutto/vaderSentiment
- Tika: https://github.com/chrismattmann/tika-python
- Glob: https://docs.python.org/3/library/glob.html
- Requests: https://requests.readthedocs.io/en/master/

Other links: 

- Tika Parse Method: https://www.geeksforgeeks.org/parsing-pdfs-in-python-with-tika/

Below is the initial scrape of the program: 

```markdown

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
```
### Intial Obstacles: 

The links that have just been scraped are actually links to a redirection page. This redirection will send to an authentification page that will force the user to sccept the T+C's before allowing access to the company's pdf announcement. The question becomes how do bypass this webpage to access this information. 

I'm sure that there are more sophicated ways and perhaps a way to interact/accept terms on the landing page from python, however I chose a different approach that needed less cross-platform expertise. 

If we download this page local and then scrape this text file for the redirection link we will be able to access the proper pdf. If time permits in the future I will update this method to not have to download this txt file locally before accessing the correct webpage.



### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/jordanmuskitta/ASX_Scraper_/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

If you're interested in more of my projects, check out my gitHub for more documentation and code. https://github.com/jordanmuskitta
