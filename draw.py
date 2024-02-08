import arrow
from PIL import Image,ImageDraw, ImageFont
import logging

#todo: change 800x480 to epd.width, epd.height (passing in values i guess)
def get_image():
    return Image.new('1', (800, 480), 255)


def get_font(size):
    return ImageFont.truetype("FreeMono.ttf", size)


def pretty_start_time_string(time, all_day):
    begin = arrow.get(time)
    begin.to('US/Eastern')
    if all_day:
        return begin.format('MM/DD')
    else:
        return begin.humanize() + " - " + begin.format('dddd MM/DD hh:mm')

def next(event,all_day=False):
    logging.info("Drawing Next event.")
    # New BW (only) image that is 800x400: the size of the 7.5e-ink display we are using.
    out = get_image()
    header_fnt = get_font(64)
    desc_fnt = get_font(24)
    d = ImageDraw.Draw(out)
    d.multiline_text((10, 10), event.name, font=header_fnt)
    time = pretty_start_time_string(event.begin,all_day)
    d.text((10, 80), time, font=desc_fnt, font_size=24)

    # our microsoft calendars don't like publishing descriptions?
    if(event.description):
        d.text((10, 140), event.description, font=desc_fnt)

    return out
def current(event):
    logging.info("Drawing Current event.")
    out = get_image()
    header_fnt = get_font(64)
    desc_fnt = get_font(24)
    d = ImageDraw.Draw(out)
    d.multiline_text((10, 10), "Happening Now:", font=header_fnt)
    d.multiline_text((10, 60), event.name, font=header_fnt)
    begin = arrow.get(event.begin)
    #end = arrow.get(event.end)

    begin.to('US/Eastern')
    time = begin.format('dddd MM/DD hh:mm')
    d.text((10, 140), time, font=desc_fnt)

    # our microsoft calendars don't like publishing descriptions?
    if (event.description):
        d.text((10, 170), event.description, font=desc_fnt)

    return out
def all_day_today(event):
    out = get_image()
    header_fnt = get_font(64)
    d = ImageDraw.Draw(out)
    d.multiline_text((10, 10), "Today: \n"+event.name, font=header_fnt)
    return out

def no_events():
    out = get_image()
    header_fnt = get_font(64)
    d = ImageDraw.Draw(out)
    d.multiline_text((10, 10), "no upcoming events", font=header_fnt)
    return out

def error_code(code):
    out = get_image()
    header_fnt = get_font(80)
    d = ImageDraw.Draw(out)
    d.multiline_text((10, 10), f"Request Error: {code}", font=header_fnt)
    return out


