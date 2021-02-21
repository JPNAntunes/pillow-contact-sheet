from PIL import Image, ImageDraw, ImageFont

def add_images(original, text_image):
    """This pastes both the original image and the image with the description togeter, putting the latter in the bottom"""
    image_with_text = Image.new(original.mode, (original.width, original.height + text_image.height))
    image_with_text.paste(original)
    image_with_text.paste(text_image, (0, original.height))
    return image_with_text


def image_description(image, color, value):
    """This creates an an image with a description related to the changed value in the RGB value of the original image"""
    new_image = Image.new("RGB", (image.width, 75), color=0)
    draw = ImageDraw.Draw(new_image)
    if color == "red": color = "0"
    if color == "green": color = "1"
    if color == "blue": color = "2"
    font = ImageFont.truetype(font_location, 75) 
    text = 'channel {} intensity {}'.format(color, value)
    draw.text((5, new_image.height - 10), text, font = font, anchor = "ls")
    return new_image

#Insert your image location in the disk here
image_location = r""
#Insert the font you want to use here, indicating the location in the disk
font_location = r""
# read image and convert to RGB
image=Image.open(image_location)
image=image.convert('RGB')
#Initializes the images list to be appended with all the edited images
images = []
#The color for-cycle represents which part of the RGB value is going to be changed. 
#The change for-cycle represents which value is going to affect the RGB value, either multiplying it by 0.1, 0.5 or 0.9
#The last cycle goes through each pixel in an image and changes its RGB value
for color in ("red", "green", "blue"):
    for change in (0.1, 0.5, 0.9):
        used_image = image.copy()
        used_image = add_images(used_image, image_description(used_image, color, change))
        data = used_image.load()
        draw = ImageDraw.Draw(used_image)
        for x in range(image.width):
            for y in range(image.height):
                r, g, b = data[x, y]
                if color == "red": r = int(r * change)
                if color == "green": g = int(g * change)
                if color == "blue": b = int(b *change)
                draw.point((x, y), (r, g, b))
        images.append(used_image)

first_image = images[0]
contact_sheet = Image.new(first_image.mode, (first_image.width*3,first_image.height*3))
x=0
y=0

for img in images:
    # Lets paste the current image into the contact sheet
    contact_sheet.paste(img, (x, y) )
    
    # Now we update our X position. If it is going to be the width of the image, then we set it to 0
    # and update Y as well to point to the next "line" of the contact sheet.
    if x+first_image.width == contact_sheet.width:
        x=0
        y=y+first_image.height
    else:
        x=x+first_image.width

#Put the folder where you want to save the contact sheet to, here
contact_sheet_location = r""
#Resize, display and save the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
contact_sheet.show()
contact_sheet.save(r"{}\contact_sheet.png".format(contact_sheet_location))