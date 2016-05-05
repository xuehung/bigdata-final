import os
import sys
from skimage import color, io
from skimage import util
from skimage import img_as_ubyte
from skimage.transform import resize


TRAINING_DIR = sys.argv[1]
LABEL_FILE = sys.argv[2]
N = int(sys.argv[3])

def preprocess(filename, output_filename):
    # Resize the image.
    img = io.imread(filename)
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

    img = resize(img, (800, 800))
    io.imsave(output_filename, img)

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
        output_filename = os.path.join("/home/hcheng3/bigdata/resized_800x800_8000pic", filename)
        filename = os.path.join(TRAINING_DIR, filename)
        sys.stderr.write("%d/%d\t%s\n" % (n, N, filename))

        preprocess(filename, output_filename)


        idx = int(label)
        statistics[idx] = statistics[idx] + 1
        



        # Condition checking.
        if n >= N:
            break
    print statistics
