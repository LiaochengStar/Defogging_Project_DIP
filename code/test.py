import os.path
import matplotlib.pyplot as plt  # plt 用于显示图片
import matplotlib.image as mpimg  # mpimg 用于读取图片
import numpy as np

img_path = os.path.dirname(os.path.dirname(os.path.abspath('test.py'))) + '\\images\\'
img_city = mpimg.imread(img_path + 'city_fog.png')

plt.imshow(img_city)  # 显示图片
plt.axis('off')  # 不显示坐标轴
plt.show()