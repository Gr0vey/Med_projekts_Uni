from PIL import Image, ImageFilter, ImageEnhance

# Open the image and resize it
img = Image.open(r'C:\Users\Skolnieks17.5VSK-12380356-K\Documents\GitHub\Med_projekts\images\background.png')
img = img.resize((500, 900))

# Apply a Gaussian blur
img = img.filter(ImageFilter.GaussianBlur(radius=3))

# Darken the image
enhancer = ImageEnhance.Brightness(img)
img = enhancer.enhance(0.4)

# Display the result

img.save(r'C:\Users\Skolnieks17.5VSK-12380356-K\Documents\GitHub\Med_projekts\images\background.png')
