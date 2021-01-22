# 搜集圖片會顯示的字
VOCAB = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] + [chr(i) for i in range(65,91)]
print(VOCAB)
CAPTCHA_LENGTH = 5
VOCAB_LENTH = len(VOCAB)
print(VOCAB_LENTH)

# 寫code
from PIL import Image
from captcha.image import ImageCaptcha
import numpy as np
def generateCaptcha(captchaText):
  """
  get captcha text and np array
  """
  # image = ImageCaptcha()
  # capcha = image.generate(captchaText)

  capchaImg = Image.open("./captcha_Images/" + str(captchaText) + ".png")
  capchaArray = np.array(capchaImg)
  return capchaArray

for img in range(16, 25):
  captcha = generateCaptcha(img)
  print(captcha, captcha.shape)

