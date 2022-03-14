import random
import string

from PIL import Image, ImageDraw, ImageFont


def create_image_using_comments(temp_filename, title, comments_text):

    text_to_print = title + "\n--------------------------------------\n[Top Comment #1]\n" + comments_text[0] + "\n--------------------------------------\n[Top Comment #2]\n" + comments_text[1]


    color="#000"
    bgcolor="#F6F6EF"
    leftpadding=15
    rightpadding=15
    width=600

    REPLACEMENT_CHARACTER = u'\uFFFD'
    NEWLINE_REPLACEMENT_STRING = ' ' + REPLACEMENT_CHARACTER + ' '

    font = ImageFont.truetype('verdana.ttf', 14)
    text_to_print = text_to_print.replace('\n', NEWLINE_REPLACEMENT_STRING)

    lines = []
    line = u""

    for word in text_to_print.split():

        if word == REPLACEMENT_CHARACTER: # give a blank line
            lines.append(line[1:]) # slice the white space in the begining of the line
            line = u""
            lines.append(u"") # the blank line

        elif font.getsize(line + ' ' + word)[0] <= (width - rightpadding - leftpadding):
            line += ' ' + word

        else: # start a new line
            lines.append(line[1:]) # slice the white space in the begining of the line
            line = u""

            #TODO: handle too long words at this point
            # list = textwrap.wrap(text_to_print, width=30)
            line += ' ' + word #for now, assume no word alone can exceed the line width

    if len(line) != 0:
        lines.append(line[1:]) # add the last line

    line_height = font.getsize(text_to_print)[1]
    img_height = line_height * (len(lines) + 3)

    img = Image.new("RGBA", (width, img_height), bgcolor)
    draw = ImageDraw.Draw(img)

    y = 10
    for line in lines:
        draw.text((leftpadding, y), line, color, font=font)
        y += line_height

    # add credits at the bottom

    credit_text = "created by 'best-hn' from news.ycombinator.com"
    credit_x_size = font.getsize(credit_text)[0] + 15
    credit_y_height = font.getsize(credit_text)[1] + 5

    draw.text((width - credit_x_size, img_height - credit_y_height), credit_text, color, font=font)

    img.save(temp_filename)

    return True
