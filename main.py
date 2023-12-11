from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageFilter, ImageOps
import textwrap
import numpy as np

ad_template = Image.new('RGB', (1024, 1024), ImageColor.getrgb("#FFFFFF"))
image = Image.open(f"coffee_on_a_desk.png").resize((int(ad_template.size[0]/2), int(ad_template.size[1]/2)))
logo = Image.open(f"Starbucks_Corporation_Logo_2011.svg.png").resize((int(ad_template.size[0]/8), int(ad_template.size[1]/8)))
ad_template.paste(logo, (int(7*(ad_template.size[0]/16)), int(ad_template.size[0]/32)), mask=logo)

# create an image
def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=256)
    alpha = Image.new('L', im.size, 256)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

rounded_image = add_corners(image, 50)
ad_template.paste(rounded_image, (int(ad_template.size[0]/4), int(3*(ad_template.size[0]/16))), rounded_image)

txt = "AI ad banners lead to higher conversion smjkjkjratesxxxxxxx falan filan fesmekan"
button_txt = "call to text here"
print(len(txt))
print(len(button_txt))
# 50 must be maximum
sans16 = ImageFont.truetype("helvetica-rounded-bold-5871d05ead8de.otf", int(3*(min(ad_template.size[0], ad_template.size[1])/64)))
times = ImageFont.truetype("Helvetica-Bold.ttf", int(3*(min(ad_template.size[0], ad_template.size[1])/128)))

# create a punchline
para = textwrap.wrap(txt, width=40)
para_button = button_txt.split()

current_height, current_width, padding = int(3*(ad_template.size[1]/4)), int(3*(ad_template.size[1]/32)), 5
for punchline in para:
    width, height = ImageDraw.Draw(ad_template).textsize(punchline, font=sans16)
    ImageDraw.Draw(ad_template).text((int(ad_template.size[0] - width) / 2, current_height),
                                     punchline, fill=ImageColor.getrgb("#7FA701"), font=sans16)
    current_height += height + padding
    #current_width += width + padding


current_height_button, pad_button = 50, 10
current_height_text, pad_button_text = 32, 10
current_width_button = 100

button = ""
for button_line in para_button:
    w, h = ImageDraw.Draw(ad_template).textsize(button_line, font=times)
    text_size = times.getsize(button_txt)
    line_size = times.getsize(button_line)
    current_width_button += int(line_size[0]) + pad_button
    button_image = Image.new('RGBA', (current_width_button, current_height_button), ImageColor.getrgb("#FFFFFF"))
    ImageDraw.Draw(button_image).rounded_rectangle(((0, 0), (current_width_button, current_height_button)), 15,
                                                   fill=ImageColor.getrgb("#7FA701"))
    button += button_line

    position_x_text_on_button = int((ad_template.size[0]/current_width_button) + int((current_width_button-text_size[0])/2))
    ImageDraw.Draw(button_image).text((position_x_text_on_button, current_height_text/2),
                                      button_txt, fill=ImageColor.getrgb("#FFFFFF"), font=times)

    ad_template.paste(button_image, (int((ad_template.size[0])/2 - int(current_width_button/2)),
                                    int(11*(ad_template.size[1]/12))))


ad_template.show()
