from PIL import Image, ImageDraw

# images فولڈر بنانا
import os
os.makedirs("images", exist_ok=True)

w, h = 800, 526

# 1. card_front
img = Image.new('RGB', (w, h), '#FFFFFF')
draw = ImageDraw.Draw(img)
draw.rounded_rectangle([0,0,w-1,h-1], radius=40, outline='#E0E0E0', width=2, fill='white')
img.save('images/card_front.png')

# 2. card_back
img2 = Image.new('RGB', (w, h), '#91C2AF')
draw2 = ImageDraw.Draw(img2)
draw2.rounded_rectangle([0,0,w-1,h-1], radius=40, outline='#91C2AF', width=2, fill='#91C2AF')
img2.save('images/card_back.png')

# 3. right button
size = 100
img3 = Image.new('RGBA', (size, size), (0,0,0,0))
d3 = ImageDraw.Draw(img3)
d3.ellipse([0,0,size-1,size-1], fill='#4CAF50')
d3.line([(25,50),(45,70),(75,30)], fill='white', width=6, joint='round')
img3.save('images/right.png')

# 4. wrong button
img4 = Image.new('RGBA', (size, size), (0,0,0,0))
d4 = ImageDraw.Draw(img4)
d4.ellipse([0,0,size-1,size-1], fill='#F44336')
d4.line([(30,30),(70,70)], fill='white', width=6)
d4.line([(70,30),(30,70)], fill='white', width=6)
img4.save('images/wrong.png')

print("4 images ban gaye!")