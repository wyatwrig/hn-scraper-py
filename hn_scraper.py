"""
Written by Wyatt Wright
6/5/2022
v1.0

This script scrapes hacker news for headlines and generates and sends an email.
For details on setup and usage see README.md
"""

import requests
from bs4 import BeautifulSoup
import yagmail
import datetime

SENDFROM = 'anothera690@gmail.com'
SENDTO = 'wyatwrig@gmail.com'



def extract_news(url): # function to extract titles
    print('Extracting Hacker News Stories...') # operating message
    cnt = ''
    cnt += ('HN Top Stories: \n' + ('-' * 50) + '\n') # email heading
    response = requests.get(url) # http get using input url
    content = response.content # keeping packet body from server response
    soup = BeautifulSoup(content, 'html.parser') # parsing the packet body with bs4
    for i, tag in enumerate(soup.find_all('a', attrs={'class':'titlelink'})):
        # gets index and tag for all html elements of type td with class = 'title' and y-align = ''
        cnt += ((str(i+1)+' :: ' + tag.text + " " + tag['href'] + "\n") if tag.text != 'More' else '')
        cnt += '\n'
        # appends to email body the number and text of the headline
    return cnt

def main():
    now = datetime.datetime.now() # getting the current date

    content = '' # placeholder content
    cnt = extract_news('https://news.ycombinator.com/')
    content += cnt
    content += ('-' * 50)
    content += ('\nEnd of Message')

    subject = 'Top News Stories HN [Auto-Generated]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)

    print("Sending Email...")
    yag = yagmail.SMTP(SENDFROM, oauth2_file="./credentials.json") # See README.md for oauth2_file details
    yag.send(SENDTO, subject, content)

    print("Email sent...")


if __name__ == "__main__":
    main()