from unsplash.api import Api
from unsplash.auth import Auth
from PIL import Image, ImageFilter

im = Image.open('/home/antek/Pictures/Screenshot from 2022-11-09 14-04-45.png')

print(im.format, im.size, im.mode)
print(im.getextrema())
print(im.getpixel((256, 256)))
new_im = im.convert('L').rotate(90).filter(ImageFilter.GaussianBlur())
new_im.show()
new_im.save('/home/antek/Pictures/Screenshot from 2022-11-09 14-04-45NEW.png', quality=95)

# unsplash = Api(Auth("74i4_wzXS1aC5JPj89c6p7gfVPo1GBlXwVtapdLtvE0"))
# me = unsplash.users.profile()
# print(me.first_name, me.last_name)
