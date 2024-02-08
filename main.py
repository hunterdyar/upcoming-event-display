from ics import Calendar
import arrow
import requests
import draw
import sys
import os
import logging
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in5_V2
import time

url = "https://outlook.office365.com/owa/calendar/baa6ac4f51934f25a56ce36bd3542b1a@Chatham.edu/34b677cd9b964159b848d670242b969115323442578641261303/calendar.ics"
def main():
    logging.info("Starting calendar image drawing...")
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    image = render_event()
    epd.display(epd.getbuffer(image))
    epd.sleep()

def is_all_day(event):
    for e in event.extra:
        if e.name == 'X-MICROSOFT-CDO-ALLDAYEVENT' and e.value == "TRUE":
            return True
    return False
def get_current_event(calendar):
    l = list(calendar.timeline.at(arrow.now()))
    if len(l) > 0:
        return l[0]
    else:
        return False

def get_next_event(calendar):
    l = list(calendar.timeline.start_after(arrow.now()))
    if len(l) > 0:
        return l[0]
    else:
        return False

def render_event():
    logging.info("Getting calendar events from url "+url)
    c = Calendar(requests.get(url).text)
    current = get_current_event(c)
    if current:
        if is_all_day(current):
            draw.all_day_today(current)
        else:
            draw.current(current)
        return

    next = get_next_event(c)
    if next:
        draw.next(next,is_all_day(next))
        return

    draw.no_events()
    print("done.")


if __name__ == "__main__":
    main()
