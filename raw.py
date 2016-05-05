from skimage import io
from skimage.transform import resize


filename = "/home/hcheng3/kaggle/sample/10_left.jpeg"
img = io.imread(filename)
img = resize(img, (250, 250))
print img.shape
