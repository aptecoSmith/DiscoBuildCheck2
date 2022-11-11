import requests
import urllib.request
from bs4 import BeautifulSoup
import third
import re
from datetime import date


class Toolbox():

    def GetHTML(url, username="", password=""):
        """Return the html of this url"""
        print("GetHTML called for URL: ", url)

        r = requests.get(url, auth=(username, password))
        htmlpage = r.content
        return htmlpage

    def ListofLinks(url, username="", password="", linkContainsKeyword=""):
        """Return a deduped list of links found in the html"""

        print("ListofLinks called for URL: ", url)

        r = requests.get(url, auth=(username, password))
        htmlPage = r.content

        soup = BeautifulSoup(htmlPage, "html.parser")

        links = list()
        keywordContainingLinks = list()

        for link in soup.findAll('a'):
            possibleLink = link.get('href', "")
            print("ListofLinks- Div a split: {}".format(possibleLink))
            if "" in possibleLink:
                links.append(possibleLink)
                print("ListofLinks- {}".format(possibleLink))

        print("ListofLinks- number containing http: ", len(links))
        for item in links:
            if linkContainsKeyword in item:
                keywordContainingLinks.append(item)

                print("ListofLinks- Found this link containing {}: ".format(item))

        print("ListofLinks- Deduping this list")
        dedupedList = list(set(keywordContainingLinks))
        print("ListofLinks- num of deduped links = ", len(dedupedList))

        for dedupedLink in dedupedList:
            print(dedupedLink)

        print("**ListofLinks Ends **")

        return dedupedList

    def ListofLinks2(url, username="", password="", linkContainsKeyword=""):
        """Return a deduped list of links found in the html"""

        print("ListofLinks2 called for URL: ", url)

        r = requests.get(url, auth=(username, password))
        htmlPage = r.content

        soup = BeautifulSoup(htmlPage, "html.parser")

        links = list()
        keywordContainingLinks = list()

        for link in soup.findAll('a'):
            possibleLink = link.get('href', "")
            possibletextLink = link.text
           # print("ListofLinks- Div a split: {}".format(possibleLink))
            if linkContainsKeyword in possibleLink:
                links.append(possibleLink)
                # print("ListofLinks- Added this to Possibles {}".format(possibleLink))

        # print("ListofLinks- number containing keyword {}: ".format(linkContainsKeyword), len(links))

        #in each of the found links, see if one contains the word results
        for item in links:
            if "Results" in item:
                #if it does, add it to our further refined list, keywordContainingLinks
                keywordContainingLinks.append(item)

            # print("ListofLinks- Found this link containing {}: ".format(item))

        #three very similar links are found, so we need to dedupe this
        print("ListofLinks- Deduping this list")

        #IIRC, this was a smart way of deduping
        dedupedList = list(set(keywordContainingLinks))
        # print("ListofLinks- num of deduped links = ", len(dedupedList))

        #looks like  we sort the link alphabetically - might be because this would give us the links in,
        # effectively, date (or run) order
        sortedAlpha = sorted(dedupedList, reverse=True)

        # for dedupedLink in sortedAlpha:
        # print(dedupedLink)

        # print("This will be the one: {}".format(sortedAlpha[0]))

        print("**ListofLinks Ends **")

        return sortedAlpha

    def RetrieveLatestFail(url, username="", password=""):
        """Return a deduped list of links found in the html"""

        print("SplitHtmlOnDiv called for URL: ", url)

        r = requests.get(url, auth=(username, password))
        htmlPage = r.content

        # Get all the text on the page, split by pipe
        soup = BeautifulSoup(htmlPage, "html.parser")
        pageText = soup.get_text('|', strip=True)

        # Split the string by the pipe into a list
        textList = pageText.split('|')
        lines = len(textList)
        # print("{} unsorted lines".format(lines))

        upToIgnored = list()
        sortedList = list()

        # we are only interested in text up to 'tests ignored'
        for eachline in textList:
            upToIgnored.append(eachline)
            if "tests ignored" in eachline:
                break

        # find the run numbers
        overviewLines = list()
        for eachline in upToIgnored:
            if "Overview" in eachline:
                overviewLines.append(eachline)
                # print("Overview Line: {}".format(eachline))

        iThinkThisNum = list()

        # get rid of lines that include the word function
        for eachline in overviewLines:
            if "function" in eachline:
                overviewLines.remove(eachline)
                print("Removed a line")

        # in each line, cut out just the bit between the # and ( and add it to a list
        for eachline in overviewLines:
            hashLoc = eachline.find('#')
            opBracLoc = eachline.find('(')
            closeBracLoc = eachline.find(')')
            runNumResult = eachline[hashLoc + 1:opBracLoc - 1]
            runDateResult = eachline[opBracLoc + 1:closeBracLoc]
            iThinkThisNum.append(runNumResult)
            # print(iThinkThisNum)

        # if the lines contain FastStatsServerTest, we want to keep them
        for eachline in upToIgnored:
            if "FastStatsServerTest" in eachline:
                sortedList.append(eachline)
                # print(eachline)

        listOfFails = list()

        for eachline in sortedList:
            if "FastStatsServerTester: : " in eachline:
                new1 = eachline.replace("FastStatsServerTester: : ", "")
            else:
                new1 = eachline

            if " (<default>)" in new1:
                new2 = new1.replace(" (<default>)", "")
            else:
                new2 = new1

            if " (Dates)" in new2:
                new3 = new2.replace(" (Dates)", "")
            else:
                new3 = new2

            if " (FTO)" in new3:
                new4 = new3.replace(" (FTO)", "")
            else:
                new4 = new3

            new = (re.findall(r'\d+', eachline))
            for number in new:
                listOfFails.append(number)

        Singleresult = third.SingleResult(runNumResult, listOfFails, runDateResult)

        return Singleresult

    # print (page)

    def ReverseList(listIn):
        print("ReverseList called")

        reversedList = list()
        lengthOfList = len(listIn)
        for x in range(lengthOfList):
            reversedList.append(listIn[lengthOfList - x - 1])

            print("New length of ReversedList {}".format(len(reversedList)))

        return reversedList

    def ReverseResultsList(listIn):
        print("ReverseList called")

        reversedList = list()
        lengthOfList = len(listIn)
        for x in range(lengthOfList):
            reversedList.append(listIn.ResultsList[lengthOfList - x - 1])

            print("New length of ReversedList {}".format(len(reversedList)))

        return reversedList

    def ListofTCFails(url, username="", password="", linkContainsKeyword=""):
        """Return a deduped list of links found in the html"""

        print("ListofTCFails called for URL: ", url)

        r = requests.get(url, auth=(username, password))
        htmlPage = r.content

        soup = BeautifulSoup(htmlPage, "html.parser")

        buildNumbers = list()
        linkandtext = list()
        changerList = list()
        dateList = list()
        links = list()
        keywordContainingLinks = list()

        #build a list of the numberspans
        numberspans = soup.findAll('span', attrs={'class': 'buildNumberInner'});
        for span in numberspans:
            if '#' in span.text:
                #print('yes')
                spantext = span.text
                noslashes = spantext.replace("\\","")
                justNumber = (noslashes.translate({ord(i): None for i in '#\r\n'}))
                andFinally = justNumber.strip()
                #print(andFinally)
                buildNumbers.append(andFinally)


        #build a list of the links and the text that is used - we add it regardless of result
        linksonPage = soup.findAll('a')
        for link in linksonPage:
            possibleLink = link.get('href', "")
            possibletextLink = link.text
            # print("ListofLinks- Div a split: {}".format(possibleLink))
            if linkContainsKeyword in possibleLink:
                linkWithAddress = 'http://aptdevbuild:8080' + possibleLink
                links.append(linkWithAddress)
                mytuple = (linkWithAddress,possibletextLink)
                if  "Tests" in possibletextLink:
                    linkandtext.append(mytuple)
                if  "error" in possibletextLink:
                    linkandtext.append(mytuple)
                # print("ListofLinks- Added this to Possibles {}".format(possibleLink))

        # build a list of the changers
        changerspans = soup.findAll('td', attrs={'class': 'link changesLink'});
        labelspans = soup.findAll('span', attrs={'class': 'pc__label'});
        for span in labelspans:

            spantext = span.text
            if '(' in spantext:
                #print('yes')

                noslashes = spantext.replace("\\", "")
                justNumber = (noslashes.translate({ord(i): None for i in '#\r\n.'}))
                andFinally = justNumber.strip()
                #print(andFinally)
                changerList.append(andFinally)

            elif 'Changes' in spantext:
                # print('yes')

                noslashes = spantext.replace("\\", "")
                justNumber = (noslashes.translate({ord(i): None for i in '#\r\n.'}))
                andFinally = justNumber.strip()
                # print(andFinally)
                changerList.append(andFinally)
        # print("ListofLinks- number containing keyword {}: ".format(linkContainsKeyword), len(links))

        # build a list of the datespans
        datespans = soup.findAll('span', attrs={'class': 'date'});
        for span in datespans:
            if ':' in span.text:
                #print('yes')
                spantext = span.text
                noslashes = spantext.replace("\\", "")
                justNumber = (noslashes.translate({ord(i): None for i in '#\r\n.'}))
                andFinally = justNumber.strip()
                #print(andFinally)
                dateList.append(andFinally)
                # print("ListofLinks- number containing keyword {}: ".format(linkContainsKeyword), len(links))

        # in each of the found links, see if one contains the word results
        for item in links:
            if "Results" in item:
                # if it does, add it to our further refined list, keywordContainingLinks
                keywordContainingLinks.append(item)

            # print("ListofLinks- Found this link containing {}: ".format(item))

        # three very similar links are found, so we need to dedupe this
        print("ListofLinks- Deduping this list")

        # IIRC, this was a smart way of deduping
        dedupedkeywordContainingLinksList = list(set(keywordContainingLinks))
        # print("ListofLinks- num of deduped links = ", len(dedupedList))

        # looks like  we sort the link alphabetically - might be because this would give us the links in,
        # effectively, date (or run) order
        sorteddedupedList = sorted(dedupedkeywordContainingLinksList, reverse=True)
        sortedBeta = sorted(linkandtext, reverse=True)

        fullCollectionofBuildNumberAndData = list()
        todaysCollectionofBuildNumberAndData = list()
        yesterdaysCollectionofBuildNumberAndData = list()
        
        for index,number in enumerate(buildNumbers):
            changer = changerList[index]
            dateofTest = dateList[index]
            datenumber = dateofTest[:2]
            today = date.today()
            d1 = today.strftime("%d")
            todaysdate = d1

            if  index< len(sortedBeta):#avoids out of range exception

                LinkAndText = sortedBeta[index]
                link = LinkAndText[0]
                text = LinkAndText[1]
                obj = number, link, text, changer, dateofTest
                # print(obj)
                if todaysdate == datenumber:
                    # print('Todays')
                    todaysCollectionofBuildNumberAndData.append(obj)
                yesterdaysdate = int(todaysdate) - 1
                if str(yesterdaysdate) == datenumber:
                    # print('Yesterdays')
                    yesterdaysCollectionofBuildNumberAndData.append(obj)
                fullCollectionofBuildNumberAndData.append(obj)

        # for dedupedLink in sortedAlpha:
        # print(dedupedLink)

        # print("This will be the one: {}".format(sortedAlpha[0]))

        print("**ListofLinks Ends **")

        return fullCollectionofBuildNumberAndData,yesterdaysCollectionofBuildNumberAndData,todaysCollectionofBuildNumberAndData
    
    