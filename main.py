from bs4 import BeautifulSoup
import requests

#get tracking number from user and determine carrier
carrier = None
#tracker = input("enter your tracking code\n")
tracker = "9405 5092 0556 8925 5233 70"

if 20 <= len(tracker) <= 35:
    carrier = "usps"
if len(tracker) == 18:
    carrier = "ups"
if 12 <= len(tracker) <= 14:
    carrier = "fedex"
tracker = list(tracker)
while " " in tracker.copy():
    tracker.remove(" ")
str(tracker)

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
print(f"Your package's current status is {currentStatus.lower()}!\n")

#get tracking history of package by day
findHist = soup.find_all("div", class_="panel-actions-content thPanalAction")
strConv = str(findHist)
strConv = strConv.split("\t")
copied = list()
dateDict = dict()
months = ["Jan", "Feb", "Marc", "Apr", "May", "Jun", "Jul", "Aug" \
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
    for index in range(len(copied)-3):
        if len(copied[index]) >2 and copied[index][:3] in months:
            t = 1
            innerList = []
            while copied[index + t][:3] not in months:
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
for day in dateDict:
    if day[-1] == ",":
        print(day[:-1])
    else:
        print(day)
    for event in dateDict[day]:
        if event != "":
            print(event)
    print("\n")
