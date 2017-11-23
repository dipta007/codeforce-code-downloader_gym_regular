"""
Thanks to manojpandey for his awesome code from that I got the idea
Link: https://github.com/manojpandey/CodeForces-Code-Downloader
""" 

import urllib
import json
import time, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sys import platform as _platform

MAX_SUBS = 10
MAX_CF_CONTEST_ID = 900

SUBMISSION_URL = 'http://codeforces.com/contest/{ContestId}/submission/{SubmissionId}'
SUBMISSION_URL_GYM = 'http://codeforces.com/gym/{ContestId}/submission/{SubmissionId}'
USER_INFO_URL = 'http://codeforces.com/api/user.status?handle={handle}&from=1&count={count}'

EXT = {'C++': 'cpp', 'C': 'c', 'Java': 'java', 'Python': 'py', 'Delphi': 'dpr', 'FPC': 'pas', 'C#': 'cs'}
EXT_keys = EXT.keys()

replacer = {'&quot;': '\"', '&gt;': '>', '&lt;': '<', '&amp;': '&', "&apos;": "'"}
keys = replacer.keys()

waitTime = 4
path = os.getcwd() + "/chromedriver"

if _platform == "linux" or _platform == "linux2":
   # linux
   path += "_linux"
elif _platform == "darwin":
   # MAC OS X
   path += "_mac"
elif _platform == "win32" or _platform == "win64":
   # Windows
   path += "_win"

driver = webdriver.Chrome(path)

def get_ext(comp_lang):
    if 'C++' in comp_lang:
        return 'cpp'
    for key in EXT_keys:
        if key in comp_lang:
            return EXT[key]
    return ""

def parse(source_code):
    for key in keys:
        source_code = source_code.replace(key, replacer[key])
    return source_code

def CFLogIn(user, passwd):
    login_site = "http://codeforces.com/enter"
    driver.get(login_site)
    time.sleep(waitTime)
    username = driver.find_element_by_id("handle")
    password = driver.find_element_by_id("password")
    
    username.send_keys(user)
    password.send_keys(passwd)

    driver.find_element_by_class_name("submit").click()
    time.sleep(waitTime)

handle = ""

def main():
    handle = raw_input("Enter your handle: ")
    print ("Next step is password. ;) ")
    print ( "If you are afraid then check the code, You are smart enough to understand it")
    passwd = raw_input("Enter your password: ")

    CFLogIn(handle, passwd)

    if not os.path.exists(handle):
        os.makedirs(handle)

    user_info = urllib.urlopen(USER_INFO_URL.format(handle=handle, count=MAX_SUBS)).read()
    dic = json.loads(user_info)
    if dic['status'] != u'OK':
        print ('Oops.. Something went wrong...')
        exit(0)

    submissions = dic['result']
    start_time = time.time()

    for submission in submissions:
        if submission['verdict'] == u'OK' and submission['contestId'] < MAX_CF_CONTEST_ID:
            con_id, sub_id = submission['contestId'], submission['id'],
            prob_name, prob_id = submission['problem']['name'], submission['problem']['index']
            comp_lang = submission['programmingLanguage']
            
            driver.get(SUBMISSION_URL.format(ContestId=con_id, SubmissionId=sub_id))
            submission_info = driver.find_element_by_xpath("//*[@id=\"pageContent\"]/div[3]/pre").text
            result = parse(submission_info).replace('\r', '')
            ext = get_ext(comp_lang)
            
            new_directory = handle + '/' + str(con_id)
            if not os.path.exists(new_directory):
                os.makedirs(new_directory)
            file = open(new_directory + '/' + prob_id + '[ ' + prob_name + ' ]' + '.' + ext, 'w')

            file.write(result)
            file.close()
            print("1", prob_name)
            time.sleep(waitTime)

        elif submission['verdict'] == 'OK':
            con_id, sub_id = submission['contestId'], submission['id'],
            prob_name, prob_id = submission['problem']['name'], submission['problem']['index']
            comp_lang = submission['programmingLanguage']

            driver.get(SUBMISSION_URL_GYM.format(ContestId=con_id, SubmissionId=sub_id))
            submission_info = driver.find_element_by_xpath("//*[@id=\"pageContent\"]/div[3]/pre").text
            result = parse(submission_info).replace('\r', '')
            ext = get_ext(comp_lang)

            new_directory = handle + '/' + str(con_id)
            if not os.path.exists(new_directory):
                os.makedirs(new_directory)
            file = open(new_directory + '/' + prob_id + '[ ' + prob_name + ' ]' + '.' + ext, 'w')

            file.write(result)
            file.close()
            print("2", prob_name)
            time.sleep(waitTime)

    end_time = time.time()
    driver.quit()

    print ('Execution time %d seconds' % int(end_time - start_time) )

if __name__ == "__main__":
    main()

