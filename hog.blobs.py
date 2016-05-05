import os
import sys
from skimage import color, io
from skimage import util
from skimage import img_as_ubyte
from skimage.transform import resize
from skimage.morphology import disk
from skimage import exposure
from skimage.feature import blob_dog, blob_log, blob_doh, canny, hog
import numpy
from skimage.filters.rank import mean_bilateral
from skimage.color import rgb2gray, gray2rgb
from skimage.filters import threshold_otsu


TRAINING_DIR = sys.argv[1]
LABEL_FILE = sys.argv[2]
START = int(sys.argv[3])
END = int(sys.argv[4])


roi_radius = 210
distance = roi_radius ** 2

def hog_1(img):
    fd, hog_image = hog(img, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualise=True)
    return fd, hog_image


def resize_1(img):
    shape = img.shape
    diameter = min(shape[0], shape[1])
    if shape[0] > diameter:
        # height
        offset = (shape[0] - diameter) / 2
        img = img[offset:offset+diameter]
    elif shape[1] > diameter:
        # width
        offset = (shape[1] - diameter) / 2
        img = img[0:shape[0], offset:offset+diameter]

    img = resize(img, (256, 256))
    return img


def get_channel(img, channel):
    if channel >= 3:
        return img
    else:
        return img[:,:,channel]

def smooth(img):
    image= img_as_ubyte(img)
    image = mean_bilateral(image.astype(numpy.uint16), disk(20), s0=10, s1=10)
    return image

def increase_contrast(img):
    return exposure.equalize_adapthist(img, clip_limit=0.03)

def otsu(img):
    thresh = threshold_otsu(img)
    binary = img > thresh
    return binary

def get_num_blobs(image):
    blobs_doh = blob_doh(image, min_sigma=.1, max_sigma=30, threshold=.05)
    count = 0
    for blob in blobs_doh:
        y, x, r = blob
        count = count + 1
    return count

def get_num_edges(image, sigma):
    edges = canny(image,sigma=sigma)
    return numpy.count_nonzero(edges)


def get_features(filename):
    feature = []
    out = ""
    raw_image = io.imread(filename)
    raw_image = resize_1(raw_image)
    image_gray = rgb2gray(raw_image)
    fd, hog_image = hog_1(image_gray)
    num_blobs = get_num_blobs(hog_image)
    print num_blobs

    return ""

    for i in range(0, len(fd)):
        s = "%.5f" % fd[i]
        if s != "0.00000":
            out = out + " " + str(i + 1) + ":" + s
    return out

def load_label(filename):
    labels = {}
    for line in open(filename):
        name, label = line.split(",")
        labels[name] = label.strip()
    return labels
        


if __name__ == '__main__':
    labels = load_label(LABEL_FILE)
    statistics = [0, 0, 0, 0, 0]
    n = 0
    for filename in os.listdir(TRAINING_DIR):
        n = n + 1
        if n < START:
            continue
        elif n > END:
            break
        label = labels[filename.split(".")[0]]
        filename = os.path.join(TRAINING_DIR, filename)
        sys.stderr.write("%d/%d\t%s\n" % (n - START + 1, END - START + 1, filename))

        feature = get_features(filename)
        
        print label + feature

        idx = int(label)
        statistics[idx] = statistics[idx] + 1

    #print statistics

# img = color.rgb2grey(img)
# io.imsave("/Users/xuehung/Downloads/img.jpeg", img)
