from bs4 import BeautifulSoup
import requests
from uszipcode import SearchEngine
import mpu
from usps import uspsTracking

#get tracking number from user and determine carrier
carrier = None
#tracker = input("enter your tracking code\n")
tracker = "9405 5282 0633 4175 3733 06"

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

if carrier == "usps":
    uspsTracking(tracker)
