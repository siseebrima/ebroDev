from PIL import Image, ImageDraw
import qrcode

data = 'Boy, there is 5 million dollars in the bank. Withdraw it and move to Vegas'
img = qrcode.make(data)
img.save('devLop1.jpg')