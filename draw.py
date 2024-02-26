import arrow
from PIL import Image, ImageDraw, ImageFont
import logging
import textwrap

# todo: change 800x480 to epd.width, epd.height (passing in values i guess)
leftstart = 50
screen_width = 800
screen_height = 480
character_width_wrap = 18


def get_image():
    return Image.new('1', (screen_width, screen_height), 255)


def get_font(size):
    return ImageFont.truetype("RifficFree-Bold.ttf", size)


def pretty_start_time_string(time, all_day):
    begin = arrow.get(time)
    begin.to('US/Eastern')
    if all_day:
        return begin.format('MM/DD')
    else:
        humanized_time = begin.humanize()
        formatted_time = begin.format('dddd MM/DD hh:mm')
        return f"{humanized_time}\n{formatted_time}"


def next(event, all_day=False):
    logging.info("Drawing Next event.")
    # New BW (only) image that is 800x400: the size of the 7.5e-ink display we are using.
    out = get_image()
    header_fnt = get_font(72)
    desc_fnt = get_font(36)
    d = ImageDraw.Draw(out)
    name = textwrap.fill(event.name, character_width_wrap)
    # 100 is a guessing game for centering the text. Ideally we would be using the font_width, character_width_wrap and screen_width to calculate it.
    x = get_left_pos_for_centered_block(header_fnt)
    x = x
    d.multiline_text((x, 80), name, font=header_fnt, align="center")
    time = pretty_start_time_string(event.begin, all_day)
    d.text((screen_width / 2, screen_height - 40), time, font=desc_fnt, font_size=24, anchor="ms",
           align="center")  # align to bottom middle of coordinates

    # our microsoft calendars don't like publishing descriptions?
    if (event.description):
        d.text((leftstart, 140), event.description, font=desc_fnt)

    return out


def current(event):
    logging.info("Drawing Current event.")
    out = get_image()
    header_fnt = get_font(64)
    desc_fnt = get_font(24)
    d = ImageDraw.Draw(out)
    bar_height = 150
    # Draw now text
    #Black bg top
    d.rectangle([(0,0),(screen_width,bar_height)], 0, 0, 0)
    d.text((screen_width/2, 80), "Now:", font=header_fnt, align="center", anchor="mt",fill=255)

    name = textwrap.fill(event.name, character_width_wrap)
    x = get_left_pos_for_centered_block(header_fnt)
    d.multiline_text((x, 160), name, font=header_fnt)
    begin = arrow.get(event.begin)
    # end = arrow.get(event.end)

    #black bg bottom
    d.rectangle([(0,screen_height-60),(screen_width,screen_height)], 0, 0, 0)
    begin.to('US/Eastern')
    time = begin.format('dddd MM/DD hh:mm')
    d.text((screen_width / 2, screen_height - 40), time, font=desc_fnt, font_size=24, anchor="ms",
           align="center", fill=255)  # align to bottom middle of coordinates
    # our microsoft calendars don't like publishing descriptions?


    #if (event.description):
    #    d.text((leftstart, 170), event.description, font=desc_fnt)

    return out


def all_day_today(event):
    out = get_image()
    header_fnt = get_font(64)
    d = ImageDraw.Draw(out)
    name = textwrap.fill(event.name, character_width_wrap)
    d.multiline_text((leftstart, 10), "Today: \n" + name, font=header_fnt)
    return out


def no_events():
    out = get_image()
    header_fnt = get_font(64)
    d = ImageDraw.Draw(out)
    text = textwrap.fill("no upcoming events", character_width_wrap)
    d.multiline_text((leftstart, 180), text, font=header_fnt)
    return out


def error_code(code):
    out = get_image()
    header_fnt = get_font(80)
    d = ImageDraw.Draw(out)
    d.multiline_text((leftstart, 10), f"Request Error: {code}", font=header_fnt)
    return out


def get_left_pos_for_centered_block(fnt):
    char_width = fnt.size * 1/2
    block_width = character_width_wrap*char_width
    return screen_width/2 - block_width/2
