from torchvision.datasets import VisionDataset

from PIL import Image

import os
import os.path
import sys


def pil_loader(path):
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')


class Caltech(VisionDataset):
    def __init__(self, root, split='train', transform=None, target_transform=None):
        super(Caltech, self).__init__(root, transform=transform, target_transform=target_transform)

        self.split = split # This defines the split you are going to use
                           # (split files are called 'train.txt' and 'test.txt')

        '''
        - Here you should implement the logic for reading the splits files and accessing elements
        - If the RAM size allows it, it is faster to store all data in memory
        - PyTorch Dataset classes use indexes to read elements
        - You should provide a way for the __getitem__ method to access the image-label pair
          through the index
        - Labels should start from 0, so for Caltech you will have lables 0...100 (excluding the background class) 
        '''
        DATA_DIR = 'Homework2-Caltech101/101_ObjectCategories'

# Prepare Pytorch train/test Datasets
        #get classes
        classes = [d.name for d in os.scandir(root) if d.is_dir() ]
        classes.sort()
        classes.pop(0)#drops Background Class
        class_to_idx = {classes[i]: i for i in range(len(classes))}
        
        #create dataset
        self.dataset=[]
        with open('Caltech101/'+ split +'.txt') as f:
          for x in f:
            c, imm=x.split('/')
            if (c in class_to_idx):
              self.dataset.append((pil_loader(root + '/'+x.split('\n')[0]), class_to_idx[c]))

    def __getitem__(self, index):
        '''
        __getitem__ should access an element through its index
        Args:
            index (int): Index

        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        '''

        image, label = image, label = self.dataset[index]   # Provide a way to access image and label via index
                                                            # Image should be a PIL Image
                                                            # label can be int

        # Applies preprocessing when accessing the image
        if self.transform is not None:
            image = self.transform(image)

        return image, label

    def __len__(self):
        '''
        The __len__ method returns the length of the dataset
        It is mandatory, as this is used by several other components
        '''
        length = len(self.dataset) # Provide a way to get the length (number of elements) of the dataset
        return length
