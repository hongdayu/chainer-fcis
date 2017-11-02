import chainer
import cv2
from fcis.datasets.voc.voc_utils import prepare_data
from fcis.datasets.voc.voc_utils import voc_label_names
from fcis.utils import visualize_mask
from fcis.utils import whole_mask2mask
import matplotlib.pyplot as plt
import numpy as np
import os.path as osp
import PIL.Image


class VOCInstanceSegmentationDataset(chainer.dataset.DatasetMixin):

    def __init__(self, data_dir=None, split='train'):
        assert split in ['train', 'val']

        if data_dir is None:
            self.data_dir = osp.expanduser(
                '~/data/datasets/VOC/VOCdevkit/VOC2012')

        imgsets_path = osp.join(
            self.data_dir, 'ImageSets/Segmentation/{}.txt'.format(split))
        with open(imgsets_path) as f:
            data = f.read()
        self.ids = data.split('\n')
        if len(self.ids[-1]) == 0:
            self.ids = self.ids[:-1]

    def __len__(self):
        return len(self.ids)

    def get_example(self, i):
        data_id = self.ids[i]
        img, seg_img, ins_img = self._load_data(data_id)
        bboxes, masks, labels = prepare_data(seg_img, ins_img)
        img = img.astype(np.float32)
        bboxes = bboxes.astype(np.float32)
        labels = labels.astype(np.int32)
        return img, bboxes, masks, labels

    def _load_data(self, data_id):
        imgpath = osp.join(
            self.data_dir, 'JPEGImages/{}.jpg'.format(data_id))
        seg_imgpath = osp.join(
            self.data_dir, 'SegmentationClass/{}.png'.format(data_id))
        ins_imgpath = osp.join(
            self.data_dir, 'SegmentationObject/{}.png'.format(data_id))
        img = cv2.imread(imgpath)
        img = img.transpose((2, 0, 1))
        seg_img = PIL.Image.open(seg_imgpath)
        seg_img = np.array(seg_img, dtype=np.int32)
        seg_img[seg_img == 255] = -1
        ins_img = PIL.Image.open(ins_imgpath)
        ins_img = np.array(ins_img, dtype=np.int32)
        ins_img[ins_img == 255] = -1
        ins_img[np.isin(seg_img, [-1, 0])] = -1
        return img, seg_img, ins_img

    def visualize(self, i):
        img, bbox, whole_mask, label = self.get_example(i)
        img = img.transpose(1, 2, 0)
        img = img[:, :, ::-1]
        scores = np.ones(len(label))
        mask = whole_mask2mask(whole_mask, bbox)
        visualize_mask(img, mask, bbox, label, scores, voc_label_names)
        plt.show()
