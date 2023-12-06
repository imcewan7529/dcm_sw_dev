from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=10)  # Adjust size as needed

def display(device):
    content = Image.new("1", device.size, "black")
    draw = ImageDraw.Draw(content)
    draw.text((0,20), "Fuel Level Reset\nAre you sure?", font=font, fill=255)
    draw.text((70,0), "Continue ->", font=font, fill=255)
    draw.text((80,50), "Cancel ->", font=font, fill=255)
    device.display(content)