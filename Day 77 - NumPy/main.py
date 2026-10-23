import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

# پروجیکٹ کی فائلوں کا راستہ
BASE = Path(__file__).parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

print("=" * 50)
print("DAY 77 - NUMPY")
print("=" * 50)

# 1. ndarray بنانا
numbers = np.array([10, 20, 30, 40, 50])
print("\n1. NumPy Array:", numbers)
print("Array کی قسم:", type(numbers))
print("Array کی شکل:", numbers.shape)
print("Array میں عناصر:", numbers.size)

# 2. مختلف Arrays بنانا
print("\n2. Arrays بنانا")
print("Zeros:\n", np.zeros((2, 3), dtype=int))
print("Ones:\n", np.ones((2, 3), dtype=int))
print("0 سے 10 تک:", np.arange(0, 11, 2))

grid = np.arange(1, 10).reshape(3, 3)
print("3x3 Array:\n", grid)
print("پہلی قطار:", grid[0])
print("دوسرا کالم:", grid[:, 1])
print("ہر عدد میں 10 جمع:", grid + 10)
print("ہر عدد کو 2 سے ضرب:", grid * 2)
print("صرف 5 سے بڑے اعداد:", grid[grid > 5])

# 3. Broadcasting
print("\n3. Broadcasting")
prices = np.array([100, 200, 300])
print("اصل قیمتیں:", prices)
print("ہر قیمت میں 50 جمع:", prices + 50)
print("ہر قیمت پر 10 فیصد رعایت:", prices * 0.90)

# 4. Matrix multiplication
print("\n4. Matrix Multiplication")
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print("Matrix A:\n", A)
print("Matrix B:\n", B)
print("عام ضرب A * B:\n", A * B)
print("Matrix ضرب A @ B:\n", A @ B)

# 5. تصویر کو NumPy Array میں تبدیل کرنا
print("\n5. Image as an ndarray")
image = Image.new("RGB", (160, 100), "white")
draw = ImageDraw.Draw(image)
draw.rectangle((10, 10, 70, 90), fill=(255, 80, 60))
draw.ellipse((85, 15, 150, 80), fill=(40, 130, 240))
draw.line((0, 99, 159, 0), fill=(20, 180, 90), width=4)

image_path = OUT / "sample_image.png"
image.save(image_path)

pixels = np.array(image)
print("تصویر کے Array کی شکل:", pixels.shape)
print("اوپر بائیں پکسل کا رنگ:", pixels[0, 0])
print("سرخ رنگ کی اوسط:", round(float(pixels[:, :, 0].mean()), 2))

# رنگوں کی اوسط لے کر تصویر کو سیاہ سفید بنانا
gray = pixels.mean(axis=2).astype(np.uint8)
Image.fromarray(gray).save(OUT / "sample_image_grayscale.png")

# سرخ اور نیلے رنگ کے چینل الٹنا
effect = pixels.copy()
effect[:, :, 0] = 255 - effect[:, :, 0]
effect[:, :, 2] = 255 - effect[:, :, 2]
Image.fromarray(effect).save(OUT / "sample_image_colour_effect.png")

print("اصل تصویر:", image_path)
print("سیاہ سفید تصویر:", OUT / "sample_image_grayscale.png")
print("رنگ بدلی ہوئی تصویر:", OUT / "sample_image_colour_effect.png")
print("\nDay 77 مکمل ہوگیا!")
