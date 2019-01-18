# import os
# file = open('../upload_imgs/explore2.txt', 'w', encoding='utf-8')
# file.write('aaaaaaaaaaaaaaaaaaaa')
# file.close()
from PIL import Image
img = Image.open('../upload_imgs/user-1.jpg')
img.show()