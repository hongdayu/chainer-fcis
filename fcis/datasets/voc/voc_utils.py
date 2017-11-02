import collections
import numpy as np


def prepare_data(seg_img, ins_img):
    labels = []
    bboxes = []
    masks = []
    instances = np.unique(ins_img)
    for inst in instances[instances != -1]:
        mask_inst = ins_img == inst
        count = collections.Counter(seg_img[mask_inst].tolist())
        instance_class = max(count.items(), key=lambda x: x[1])[0]

        assert inst not in [-1]
        assert instance_class not in [-1, 0]

        where = np.argwhere(mask_inst)
        (y1, x1), (y2, x2) = where.min(0), where.max(0) + 1

        labels.append(instance_class)
        bboxes.append((y1, x1, y2, x2))
        masks.append(mask_inst)
    labels = np.array(labels)
    bboxes = np.array(bboxes)
    masks = np.array(masks)
    return bboxes, masks, labels


voc_label_names = [
    '__background__',
    'aeroplane',
    'bicycle',
    'bird',
    'boat',
    'bottle',
    'bus',
    'car',
    'cat',
    'chair',
    'cow',
    'diningtable',
    'dog',
    'horse',
    'motorbike',
    'person',
    'potted plant',
    'sheep',
    'sofa',
    'train',
    'tv/monitor',
]
