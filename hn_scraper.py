import os
import requests
from bs4 import BeautifulSoup
import oauth2client
from oauth2client import client, tools, file
from apiclient import errors, discovery
import httplib2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = "C:\\Users\\wyatw\\Desktop\\Projects\\pythonAutomation\\HackerNewsScraper\\client_secret.json"
APPLICATION_NAME = 'Gmail API Python Send Email'


def extract_news(url): # function to extract titles
    print('Extracting Hacker News Stories...') # operating message
    cnt = ''
    cnt += ('<strong>HN Top Stories: <\strong>\n' +
            '<br>' +
            '-' * 50 +
            '<br>') # email heading
    response = requests.get(url) # http get using input url
    content = response.content # keeping packet body from server response
    soup = BeautifulSoup(content, 'html.parser') # parsing the packet body with bs4
    for i, tag in enumerate(soup.find_all('a', attrs={'class':'titlelink'})):
        # gets index and tag for all html elements of type td with class = 'title' and y-align = ''
        cnt += ((str(i+1)+' :: ' + tag.text + "\n" + '<br>') if tag.text != 'More' else '')
        # appends to email body the number and text of the headline
    return cnt

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print(credentials)
        print('Storing credentials to ' + credential_path)
    return credentials

def SendMessage(msgHtml):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    result = SendMessageInternal(service, "me", msgHtml)
    return result

def SendMessageInternal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"
    return "OK"

def main():
    now = datetime.datetime.now() # getting the current date

    content = '' # placeholder content
    cnt = extract_news('https://news.ycombinator.com/')
    content += cnt
    content += ('<br>------<br>')
    content += ('<br><br>End of Message')

    to = "wyatwrig@gmail.com"
    sender = "anothera690@gmail.com"
    subject = 'Top News Stories HN [Auto-Generated]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(content, 'html'))

    SendMessage(msg)



if __name__ == "__main__":
    main()