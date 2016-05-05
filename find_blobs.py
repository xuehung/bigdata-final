import os
import sys
from skimage import color, io
from skimage import util
from skimage import img_as_ubyte
from skimage.transform import resize
from skimage.morphology import disk
from skimage import exposure
from skimage.feature import blob_dog, blob_log, blob_doh
import numpy
from skimage.filters.rank import mean_bilateral
from skimage.color import rgb2gray, gray2rgb


TRAINING_DIR = sys.argv[1]
LABEL_FILE = sys.argv[2]
N = int(sys.argv[3])


roi_radius = 340
distance = roi_radius ** 2

def find_blobs(filename):
    feature = ""
    raw_image = io.imread(filename)
    for channel in range(0, 4):
        if channel < 3:
            image = raw_image[:,:,channel]
        image_gray = rgb2gray(image)

        # Smoothing
        image_gray = img_as_ubyte(image_gray)
        image_gray = mean_bilateral(image_gray.astype(numpy.uint16), disk(20), s0=10, s1=10)

        # Increase contrast
        image_gray = exposure.equalize_adapthist(image_gray, clip_limit=0.03)

        # Find blobs
        blobs_doh = blob_doh(image_gray, min_sigma=1, max_sigma=20, threshold=.005)
        count = 0
        for blob in blobs_doh:
            y, x, r = blob
            if (x-400)**2 + (y-400)**2 > distance:
                continue
            count = count + 1
        feature = feature + " " + str(channel + 1) + ":" + str(count)
    return feature

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
        label = labels[filename.split(".")[0]]
        filename = os.path.join(TRAINING_DIR, filename)
        sys.stderr.write("%d/%d\t%s\n" % (n, N, filename))

        feature = find_blobs(filename)
        
        print label + feature

        idx = int(label)
        statistics[idx] = statistics[idx] + 1



        # Condition checking.
        if n >= N:
            break
    print statistics

# img = color.rgb2grey(img)
# io.imsave("/Users/xuehung/Downloads/img.jpeg", img)
