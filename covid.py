import json
from requests import get
import time
import sys

from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
from unicornhatmini import UnicornHATMini

url = 'https://api.covidactnow.org/v2/states.json?apiKey=c81b4336911848e3a0252cb8db9d5c73'

text= " "
initiated=0
complete=0
g=0
unicornhatmini = UnicornHATMini()

offset_x = 0
rotation = 180
state = 0
covid = get(url).json()
print(len(covid))

if len(sys.argv) > 1:
    try:
        rotation = int(sys.argv[1])
    except ValueError:
        print("Usage: {} <rotation>".format(sys.argv[0]))
        sys.exit(1)
 
unicornhatmini.set_rotation(rotation)
display_width, display_height = unicornhatmini.get_shape()
 
print("{}x{}".format(display_width, display_height))
 
unicornhatmini.set_brightness(0.1)

font = ImageFont.truetype("5x7.ttf", 8)

def percentage_call(initiated,state):
    covid = get(url).json()
    try:
        initiated=round(covid[state]['metrics']['vaccinationsInitiatedRatio']*100)
        print(initiated)
    except:
        initiated=0
    return initiated

def percentage_call_com(complete,state):
    covid = get(url).json()
    try:
        complete=round(covid[state]['metrics']['vaccinationsCompletedRatio']*100)
        print(complete)
    except:
        complete=0
    return complete

def api_call(text,state):  
    print (covid[state]['state'])
    text=covid[state]['state']
    return text
    
while True:
    if (state < 52):
        state+=1
    else:
        state=0
        
    text = api_call(text,state)
    text_width, text_height = font.getsize(text)

    # Create a new PIL image big enough to fit the text
    image = Image.new('P', (text_width + display_width + display_width, display_height), 0)
    draw = ImageDraw.Draw(image)

    # Draw the text into the image
    draw.text((display_width, -1), text, font=font, fill=255)
    
    offset_x = 12
    
    if g < 255:
        g+=10
    else:
        g=0
        
    for y in range(display_height):
        for x in range(display_width):
            if image.getpixel((x + offset_x, y)) == 255:
                unicornhatmini.set_pixel(x, y, 255-g, 255-g, 255)
            else:
                unicornhatmini.set_pixel(x, y, 0, 0, 0)

    unicornhatmini.show()
    time.sleep(2)
    unicornhatmini.clear()
    
    percentage = round(percentage_call(initiated,state)/5.9)
    print(percentage)
    percentage_com = round(percentage_call_com(complete,state)/5.9)
    print(percentage_com)
    
    if percentage > 15:
        percentage = 17
    
    if percentage_com > 15:
        percentage_com = 17
    
    for x in range(percentage):
        for y in range(3):
            unicornhatmini.set_pixel(x, y, 0, 0, 255)
            unicornhatmini.show()
            time.sleep(0.01)
    for x in range(percentage,17):
        for y in range(3):
            unicornhatmini.set_pixel(x, y, 0, 0, 10)
            unicornhatmini.show()
            time.sleep(0.01)
    for x in range(percentage_com):
        for y in range(4,7):
            unicornhatmini.set_pixel(x, y, 0, 255, 255)
            unicornhatmini.show()
            time.sleep(0.01)
    for x in range(percentage_com,17):
        for y in range(4,7):
            unicornhatmini.set_pixel(x, y, 0, 5, 5)
            unicornhatmini.show()
            time.sleep(0.01)
            
    image = Image.new('P', (text_width + display_width + display_width, display_height), 0)
    draw = ImageDraw.Draw(image)
    draw.text((0, 5), text, font=font, fill=255)
    unicornhatmini.show()
    time.sleep(5)
    
    unicornhatmini.clear()
