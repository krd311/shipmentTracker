from bs4 import BeautifulSoup
import requests
from uszipcode import SearchEngine
import mpu

def uspsTracking(tracker):
    #attempt to contact usps
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = f'https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1={tracker}'

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    #remove newlines from children list
    html = list(soup.children)
    for x in html.copy():
        if x == "\n":
            html.remove(x)

    #print current status of package
    findStatus = soup.find_all("div",class_="delivery_status")
    start = str(findStatus).find("<strong>")
    end = str(findStatus).find("</strong>")
    currentStatus = str(findStatus)[start + 8 :end]

    #get tracking history of package by day
    findHist = soup.find_all("div", class_="panel-actions-content thPanalAction")
    strConv = str(findHist)
    strConv = strConv.split("\t")
    copied = list()
    dateDict = dict()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug" \
              "Sep", "Oct", "Nov", "Dec"]

    for item in strConv.copy():
        if item == "":
            strConv.remove(item)
        if "<" in item or ">" in item:
            strConv.remove(item)

    for item in strConv:
        item = item[:-2]
        copied.append(item)

    dayCount = 0
    for item in copied:
        if item[:3] in months:
            dayCount += 1

    if dayCount > 1:
        for index in range(len(copied)-4):
            innerList = []
            if len(copied[index]) > 3 and copied[index][:3] in months:
                t = 1
                while index > 0 and copied[index + t][:3] not in months:
                    innerList.append(copied[index + t])
                    t += 1
                if copied[index] in dateDict:
                    dateDict[copied[index]] += innerList
                else:
                    dateDict[copied[index]] = innerList
    else:
        innerList= copied[1:]
        if copied[0] in dateDict:
            dateDict[copied[0]] += innerList
        else:
            dateDict[copied[0]] = innerList

    #print breakdown
    zipList = []
    print("-" * 10, "RECAP", "-"*10)
    for day in dateDict:
        if day[-1] == ",":
            print(day[:-1])
        else:
            print(day)
        for event in dateDict[day]:
            if event != "":
                print(event)
            try:
                int(event[-6:])
                if event[-6:].split()[0] not in zipList:
                    zipList.append(event[-6:].split()[0])
            except:
                pass
        print("\n")

    #find total travel distance of package
    search = SearchEngine(simple_zipcode=True)
    if len(zipList) > 1:
        startZip = search.by_zipcode(zipList[0])
        startLat = startZip.lat
        startLong = startZip.lng

        currentZip = search.by_zipcode(zipList[-1])
        currentLat = currentZip.lat
        currentLong = currentZip.lng

        try:
            distance = mpu.haversine_distance((startLat,startLong),(currentLat,currentLong))
            print(f'Your package has traveled {distance:.2f} km.')
            print(f'Your package has traveled {distance * 0.621371:.2f} mi.')
        except:
            print(f"Cannot determine distance between {startZip.city} and {currentZip.city} at this time.")

    print(f"Your package's current status is {currentStatus.lower()}!")