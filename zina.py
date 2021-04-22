import datetime
import wikipedia
import webbrowser
import os
import time
import re
import random
import googleapiclient.discovery as discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests # Import requests
from bs4 import BeautifulSoup # Import BeautifulSoup4
options = Options()
options.headless = True
firefox_path = "/home/oussama/PycharmProjects/rasaa/geckodriver"
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('intl.accept_languages', 'fr')
driver = webdriver.Firefox(executable_path=firefox_path,firefox_profile=firefox_profile)
#driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
translator = Translator(service_urls=['translate.google.com','translate.google.co.ee',])

b="Zina: "
need_list=['what can I do for you?', 'Do you want something else?', 'give me questions or tasks', 'I want to take time with you, do you want to know something else?','what is on your mind?', 'I can not think like you-humans, but can give answer your all questions',"Let's discover this world! What do you want to learn today?" ]
sorry_list=['I am sorry I dont know how can I say answer', 'I dont have an idea about it','Sorry! try again']
bye_list=['Good bye. I will miss you','See you','Bye, dont forget I will always be here']
comic_list=['It is not a comic. I was serious','Do you think that you are comic? SHUT UP!']
greet_list=['Hi', 'Hi my dear']

def calendarr():
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SECRET_FILE = 'credentials.json'
    APPLICATION_NAME = 'Google Calendar - Raw Python'
     
     
    def get_credentials():
        """Gets valid user credentials from storage.
     
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
     
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'credentials.json')
     
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
     
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)   
    
    result= service.calendarList().list().execute()
    calendar_id=result['items'][0]['id']
    start_date = datetime.datetime.today().isoformat() + 'Z'
    end_date = datetime.date.today() + datetime.timedelta(days=1)
    
    result=service.events().list(calendarId=calendar_id,timeZone='Europe/Tallinn').execute()
    
    tomorrow=datetime.date.today() + datetime.timedelta(days=1)
    to=tomorrow.strftime("%Y-%m-%d")
    a=input()
    count=[]
    for i in range(0, len(result['items'])):
        if a=='tomorrow lecture':
            x=to+result['items'][i]['start']['dateTime'][10:]
            if x in result['items'][i]['start']['dateTime']:
                count.append(result['items'][i])
    
    if len(count)>0:
        print('You have '+str(len(count))+' lectures for tomorrow.')
        for i in range(0, len(count)):
            s = translator.translate(count[0]['summary'], dest='en',src='et')
            print(s.text + '  will start at '+count[i]['start']['dateTime'][11:16] +'. Lecture will finish at '+count[i]['end']['dateTime'][11:16]+'. The adress is '+count[i]['location']+ ' and your teacher will be '+count[i]['description'])

def takeCommand(query):
    while True:
        if 'who is' in query.lower():
            try:
                query=query.replace('who is','')
                result=wikipedia.summary(query, sentences=2)
                return result
            except:
                sorry=random.choice(sorry_list)
                return sorry
        elif 'play' in query.lower():
            query=query.replace('play','')
            url='https://www.youtube.com/results?search_query='+query
            webbrowser.open(url)
            time.sleep(2)
            time.sleep(3)
            need=random.choice(need_list)
            return need
        elif 'haha' in query:
            comic=random.choice(comic_list)
            return comic
        elif "weather" in query:
            res=google_weather(query)
            msg='\n'.join(res)
            return msg
        else:
            try:
                
                url='https://www.google.com/search?channel=crow2&client=firefox-b-d&q='
                key=query+str(' yahoo answer')
                url=url+str(key)
                link=get_browser(url)
                a=driver.find_elements_by_xpath("//div[@class='yuRUbf']")
                a=[i.find_element_by_tag_name('a').get_attribute('href') for i in a]
                for href in a:
                    if 'answers.yahoo.com' in href:
                        answers=yahoo_answer(href)
                        answers1=answers.sort(key=lambda item:len(item))
                        answer=answers1[len(answers1)//2]
                        # answer=answers[0]
                        break
                    else:
                        url = 'https://www.google.com/search?channel=crow2&client=firefox-b-d&q='
                        word = query + str(' quora')
                        url = url + str(word)
                        link = get_browser(url)
                        if 'quora.com' in link:
                            answers = quora_answer(link)
                            answer = answers[1]
                return answer
            except Exception as e:
                sorry=random.choice(sorry_list)
                return sorry

def get_browser(url):
    driver.get(url)
    time.sleep(4)
    div=driver.find_elements_by_xpath("//div[@class='yuRUbf']")
    for d in div:
        a=d.find_element_by_tag_name("a")
        link=a.get_attribute('href')
        if 'answers.yahoo' in link:
            #print(link)
            return (link)
        elif 'quora.com' in link:
            #print(link)
            return link

def yahoo_answer(url):
    user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
    'Safari/537.36'
    user_agent_smartphone = 'Mozilla/5.0 (Linux; Android 9; SM-G960F '\
    'Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) '\
    'Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36'
    user_agent_old_phone = 'Nokia5310XpressMusic_CMCC/2.0 (10.10) Profile/MIDP-2.1 '\
    'Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; '\
    'Nokia5310XpressMusic) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile'



    user_agents=[user_agent_desktop,user_agent_smartphone,user_agent_old_phone]
    text=[]  

    for user_agent in user_agents:

        headers = { 'User-Agent': user_agent}


    resp = requests.get(url, headers=headers)  # Send request
    code = resp.status_code  # HTTP response code
    if code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')  # Parsing the HTML
    else:
        print(f'Error to load : {code}')
    div_tags=soup.find('ul',{'class':'AnswersList__answersList___2ikkB'})
    answers=div_tags.find_all('div',{'class':'Answer__answer___FdhNY'})
    text=[]
    for a in answers:
        p_tags=a.find_all('p')
        t=''
        for p in p_tags:
            t+=p.get_text()
        text.append(t)
    return text

def quora_answer(url):
    answers=[]
    p_tags=[]
    driver.get(url)
    scroll_pause_time = 1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
    i = 0
    for j in range(3):
            #scroll one screen height each time
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause_time)
            try:
                button=driver.find_element_by_xpath("//button[@class='q-click-wrapper qu-active--textDecoration--none qu-focus--textDecoration--none base___StyledClickWrapper-lx6eke-1 fDkEAC puppeteer_test_read_more_button  qu-borderRadius--pill qu-alignItems--center qu-justifyContent--center qu-whiteSpace--nowrap qu-userSelect--none qu-display--inline-flex qu-bg--gray_ultralight qu-tapHighlight--white qu-textAlign--center qu-cursor--pointer qu-hover--textDecoration--none']")
                button.click()
                time.sleep(2)
            except:
                pass
            time.sleep(4)
            #update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
             #Break the loop when the height we need to scroll to is larger than the total scroll height
            if screen_height * i > scroll_height:
                break
    butt=driver.find_elements_by_xpath("//div[@class='q-text']")  
    for b in butt:
        answers.append(b.text)
    return answers

def google_weather(query):
    res=[]
    url='https://www.google.com/search?channel=crow2&client=firefox-b-d&q='
    url=url +str(query)
    driver.get(url)
    taks=driver.find_element_by_xpath("//span[@id='wob_dc']").text
    res.append(taks)
    jaw=driver.find_elements_by_xpath("//div[@class='vk_gy vk_sh']")
    for j in jaw:
        div=j.find_elements_by_tag_name("div")
        for d in div[:3]:
            res.append(d.text)
    harr=driver.find_element_by_xpath("//div[@class='vk_bk TylWce']").text
    harr=harr+str('°C')
    res.append(harr)
    return res
