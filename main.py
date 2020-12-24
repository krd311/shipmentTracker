from usps import uspsTracking

def main(tr):
    #get tracking number from user and determine carrier
    tracker = tr #"9405 5282 0633 4175 3733 06"

    if 20 <= len(tracker) <= 35:
        return uspsTracking(tracker)
    elif len(tracker) == 18:
        pass
    elif 12 <= len(tracker) <= 14:
        pass
    else:
        return "error 1"

    #remove spaces from tracking code if any are present
    tracker = list(tracker)
    while " " in tracker.copy():
        tracker.remove(" ")
    str(tracker)

