import os
import sys
from skimage import color, io
from skimage import util
from skimage import img_as_ubyte
from skimage.transform import resize
from skimage.morphology import disk
from skimage import exposure
from skimage.feature import blob_dog, blob_log, blob_doh, canny
import numpy
from skimage.filters.rank import mean_bilateral
from skimage.color import rgb2gray, gray2rgb
from skimage.filters import threshold_otsu


TRAINING_DIR = sys.argv[1]
LABEL_FILE = sys.argv[2]
START = int(sys.argv[3])
END = int(sys.argv[4])


roi_radius = 340
distance = roi_radius ** 2


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
    blobs_doh = blob_doh(image, min_sigma=1, max_sigma=20, threshold=.005)
    count = 0
    for blob in blobs_doh:
        y, x, r = blob
        if (x-400)**2 + (y-400)**2 > distance:
            continue
        count = count + 1
    return count

def get_num_edges(image, sigma):
    edges = canny(image,sigma=sigma)
    return numpy.count_nonzero(edges)


def get_features(filename):
    feature = []
    raw_image = io.imread(filename)
    for channel in range(0, 4):
        image = get_channel(raw_image, channel)
        image_gray = rgb2gray(image)
        for is_smoothing in range(0, 2):
            image_gray_1 = smooth(image_gray) if is_smoothing == 1 else image_gray
            for is_incrase_contrast in range(1, 2):
                image_gray_2 = increase_contrast(image_gray_1) if is_incrase_contrast == 1 else image_gray_1

                # Get number of blobs.
                num_blobs = get_num_blobs(image_gray_2)
                feature.append(num_blobs)

                # Get number of edges.
                # for is_otsu in range(0, 2):
                #    image_gray_3 = otsu(image_gray_2) if is_otsu == 1 else image_gray_2

                """
                num_edge = get_num_edges(image_gray_2, 2)
                feature.append(num_edge)
                if num_blobs == 0:
                    feature.append(0)
                else:
                    feature.append(num_edge/num_blobs)
                """

    out = ""
    for i in range(0, len(feature)):
        out = out + " " + str(i + 1) + ":" + str(feature[i])
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

    print statistics

# img = color.rgb2grey(img)
# io.imsave("/Users/xuehung/Downloads/img.jpeg", img)
