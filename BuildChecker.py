import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import os
from datetime import date,datetime,timedelta
from prettytable import PrettyTable
#import other files
import SomeMethods
import third
import emailMethods


#activate venv
#pip install -r requirements.txt




#pip install pyinstaller
#pip install requests
# pip install beautifulsoup4
#pip install prettytable

# pyinstaller --onefile BuildChecker.py

print("Last update 16062022")

username = 'jsmith'
password = 'jsmith'

latest_release_quarter = 4

URLList = list()
products = list()

products.append('Discoverer')
products.append('CLMClient')
products.append('Client')


def returnCorrectUrlList(latest_release_quarter,products):
    print(' returnCorrectUrlList entered')
    tempReturnList = list()


    product = 'disco'
    release_quarter = latest_release_quarter
    today = date.today()
    day = today.strftime("%d%m%y")
    month =today.strftime("%m")
    year = today.strftime("%Y")
    lastYear = int(year) - 1


    old1 = ''
    old2 = ''
    old3 = ''
    old4 = ''
    old5 = ''
    old6 = ''
    old7 = ''
    old8 = ''


    if latest_release_quarter == 4:
        print(f'last release in {lastYear}')
        old1 = f'{lastYear}q{latest_release_quarter}'
        old2 = f'{lastYear}q{latest_release_quarter-1}'
        old3 = f'{lastYear}q{latest_release_quarter-2}'
        old4 = f'{lastYear}q{latest_release_quarter-3}'
        old5 = f'{int(year)}q{1}'
        old6 = f'{int(year)}q{2}'
        old7 = f'{int(year)}q{3}'
        old8 = f'{int(year)}q{4}'



    for product in products:
        print(f'building for {product}')

        #make the LnG item
        url1a = (f'{product}_LnG', f'http://aptdevbuild:8080/viewType.html?buildTypeId={product}LnG_BuildDebug')
        # make the old ones
        url1b = (f'{product}_{old1}', f'http://aptdevbuild:8080/viewType.html?buildTypeId={product}_{old1}_BuildDebug')
        url1c = (f'{product}_{old2}', f'http://aptdevbuild:8080/viewType.html?buildTypeId={product}_{old2}_BuildDebug')
        url1d = (f'{product}_{old3}', f'http://aptdevbuild:8080/viewType.html?buildTypeId={product}_{old3}_BuildDebug')
        url1e = (f'{product}_{old4}', f'http://aptdevbuild:8080/viewType.html?buildTypeId={product}_{old4}_BuildDebug')

        url1f = (f'{product}_{old5}', f'http://aptdevbuild:8080/viewType.html?buildTypeId={product}_{old5}_BuildDebug')
        url1g = (f'{product}_{old6}', f'http://aptdevbuild:8080/viewType.html?buildTypeId={product}_{old6}_BuildDebug')
        url1h = (f'{product}_{old7}', f'http://aptdevbuild:8080/viewType.html?buildTypeId={product}_{old7}_BuildDebug')
        url1i = (f'{product}_{old8}', f'http://aptdevbuild:8080/viewType.html?buildTypeId={product}_{old8}_BuildDebug')




        tempReturnList.append(url1a)
        tempReturnList.append(url1b)
        tempReturnList.append(url1c)
        tempReturnList.append(url1d)
        tempReturnList.append(url1e)

        tempReturnList.append(url1f)
        tempReturnList.append(url1g)
        tempReturnList.append(url1h)
        tempReturnList.append(url1i)
        print(url1a)
        print(url1b)
        print(url1c)
        print(url1d)
        print(url1e)
        print(url1f)
        print(url1g)
        print(url1h)
        print(url1i)



    print('returnCorrectUrlList ends')

    return tempReturnList





URLs = list()


URLs = returnCorrectUrlList(latest_release_quarter,products)
#r = requests.get(url, auth=(username, password))
#htmlpage = r.content
#print (page)
tools = SomeMethods.Toolbox
fail_threshold = 10
devs =('testing@apteco.com')
#devs =('john.smith@apteco.com')

def Check(product,url_in):
    print('Check')
    # get a list of all the shown tests
    dedupedList1 = tools.ListofTCFails(url_in, username, password, "buildId")
    finalCollectionofBuildNumberLinkAndText = dedupedList1[0]
    yesterdaysCollectionofBuildNumberAndData = dedupedList1[1]
    todaysCollectionofBuildNumberAndData = dedupedList1[2]
    # html_page = urllib.request.urlopen(url)
    print('Latest run:')
    latestRun = dedupedList1[0]
    print(latestRun)



    # we now have a list of all the tests that are on the debug page.
    # which ones do we want to act on?
        # It seems to me we want all of todays and yesterdays....
        # done
        # we should then have the info we need to spam devs.
        # I'm thinking count the pass or fails, then list the data for fails.
    # Poss mark high importance for those we can identify....

    listofYesterdaysFails = list()
    wordIndicatesFails = ["Fail", "fail", "Error", "error"]

    yesterdaysResultsTable = PrettyTable()
    yesterdaysResultsTable.field_names = ["Run", "Link", "Text", "Changes By", "Start Date"]
    failures = False
    for eachFail in yesterdaysCollectionofBuildNumberAndData:
        number = eachFail[0]
        link = eachFail[1]
        text = eachFail[2]
        changer = eachFail[3]
        dateofTest = eachFail[4]
        if any(x in text for x in wordIndicatesFails):
            failures = True
            yesterdaysResultsTable.add_row([number, link, text, changer, dateofTest])
            messagestring = f"""
            Run number {number} has failed
            {link}
            Summary: {text}
            """
    print(yesterdaysResultsTable)
    stringedTable = yesterdaysResultsTable.get_string()
    # html_table = yesterdaysResultsTable.get_html_string()
    print("Email Section")
    today = date.today()
    yesterday = datetime.today() - timedelta(days=1)

    formattedToday = today.strftime("%d%m%y")
    formattedYesterday = yesterday.strftime("%d%m%y")
    if failures:
        try:
            email_recipient = devs
            email_subject = f"{product} Build Failures {formattedYesterday}"
            email_message = f"""***Automated Email***
            On date: {formattedYesterday} there were the following failures:
            {stringedTable}    
            """
            attachment_location = ''
            emailMethods.send_email(email_recipient, email_subject, email_message)
            print("email send passed without exception")
        except Exception as e:
            print("email send hit an exception")
            print(e)
    else:
        print('No Falures')
        # try:
        #     email_recipient = devs
        #     email_subject = f"{product} No Panic Necessary {formattedYesterday}"
        #     email_message = f"""***Automated Email***
        #     On date: {formattedYesterday} there were no failures:
        #     {stringedTable}    
        #     """
        #     attachment_location = ''
        #     emailMethods.send_email(email_recipient, email_subject, email_message)
        #     print("email send passed without exception")
        # except Exception as e:
        #     print("email send hit an exception")
        #     print(e)


    print('***Ends***')




##################

for product,eachURL in URLs:
    print(f'Checking URL {eachURL}')
    time.sleep(60)
    Check(product,eachURL)
    
print('Build Check Complete')
input("Press Enter to continue ...")

