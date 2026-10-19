from PIL import Image, ImageDraw
img = Image.new('RGBA', (200, 224), (247, 245, 221, 255))
draw = ImageDraw.Draw(img)
draw.ellipse([20, 50, 180, 210], fill=(231, 48, 91))
img.save("tomato.png")
print("tomato.png ban gayi!")