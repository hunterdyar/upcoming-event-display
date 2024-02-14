from ics import Calendar
import arrow
import requests
import draw
import logging
from PIL import Image
flipV = True
flipH = True
incomingHoursShift = 5
has_display = True



logging.basicConfig(level=logging.DEBUG)

url = "https://outlook.office365.com/owa/calendar/95fbbcbe3b3346619f273bbe32109817@Chatham.edu/c31abb24c8a54356bb386bde49cf099215129222627318247751/calendar.ics"
def main():
    logging.info("Starting calendar image drawing...")
    image = render_event()
    if flipV:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    if flipH:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)

    # noinspection PyBroadException
    try:
        from lib.waveshare_epd import epd7in5_V2
        epd = epd7in5_V2.EPD()
        epd.init()
        epd.Clear()
        # Set to true when we have the display

        has_display = True
    except:
        logging.info("can't initiate EPD. Ignoring errors and assuming no display is connected or SPI is not configured")
        has_display = False


    if image is not None:
        if has_display:
            #epd.init_fast() #don't think we need to do this

            epd.display(epd.getbuffer(image))
            epd.sleep()
        else:
            # lol flip it back
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            image.show()
    else:
        logging.error("drawing failed. Image is... "+str(image))

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
    logging.info("Getting calendar events from url")
    cr = requests.get(url)
    if cr.status_code != requests.codes.ok:
        logging.error("Web lookup Error:"+cr.status_code)
        return draw.error_code(cr.status_code)

    c = Calendar(cr.text)
    for e in c.timeline:
        e.end = e.end.shift(hours=incomingHoursShift)
        e.begin = e.begin.shift(hours=incomingHoursShift)
        e.begin = e.begin.to('US/Eastern')
        e.end = e.end.to('US/Eastern')

    for e in c.timeline:
        logging.info(e.begin)
    current = get_current_event(c)
    if current:
        if is_all_day(current):
            logging.info("have an event all day today.")
            return draw.all_day_today(current)
        else:
            logging.info("have an event right now")
            return draw.current(current)

    next = get_next_event(c)
    if next:
        logging.info("have an upcoming events")
        return draw.next(next,is_all_day(next))

    logging.info("No events")
    return draw.no_events()

if __name__ == "__main__":
    main()
