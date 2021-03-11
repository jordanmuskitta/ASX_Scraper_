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

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/jordanmuskitta/ASX_Scraper_/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

If you're interested in more of my projects, check out my gitHub for more documentation and code. https://github.com/jordanmuskitta
