from PIL import Image, ImageDraw

img = Image.new('RGB', (200, 200), 'white')
draw = ImageDraw.Draw(img)

# kala taala bana
draw.rounded_rectangle([40, 80, 160, 180], radius=20, fill='black')
draw.rectangle([65, 30, 85, 85], fill='black')
draw.rectangle([115, 30, 135, 85], fill='black')

# peela sorakh
draw.ellipse([85, 105, 115, 135], fill='#FFCC00')
draw.rectangle([90, 125, 110, 155], fill='#FFCC00')

img.save('logo.png')
print("logo.png ban gaya!")