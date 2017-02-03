# -*- coding: utf-8 -*-

""" AlexNet.

Applying 'Alexnet' to Oxford's 17 Category Flower Dataset classification task.

References:
    - Alex Krizhevsky, Ilya Sutskever & Geoffrey E. Hinton. ImageNet
    Classification with Deep Convolutional Neural Networks. NIPS, 2012.
    - 17 Category Flower Dataset. Maria-Elena Nilsback and Andrew Zisserman.

Links:
    - [AlexNet Paper](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)
    - [Flower Dataset (17)](http://www.robots.ox.ac.uk/~vgg/data/flowers/17/)

"""

from __future__ import division, print_function, absolute_import

import tflearn
import h5py
import numpy as np
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

f = h5py.File('onehot_dataset.h5','r')
X = f['x_dataset']
Y = f['y_dataset']

# Building 'AlexNet'
network = input_data(shape=[None, 240, 320, 3])
network = conv_2d(network, 96, 11, strides=4, activation='relu')
network = max_pool_2d(network, 3, strides=2)
network = local_response_normalization(network)
network = conv_2d(network, 256, 5, activation='relu')
network = max_pool_2d(network, 3, strides=2)
network = local_response_normalization(network)
network = conv_2d(network, 384, 3, activation='relu')
network = conv_2d(network, 384, 3, activation='relu')
network = conv_2d(network, 256, 3, activation='relu')
network = max_pool_2d(network, 3, strides=2)
network = local_response_normalization(network)
network = fully_connected(network, 96, activation='tanh')
network = dropout(network, 0.5)
network = fully_connected(network, 96, activation='tanh')
network = dropout(network, 0.5)
network = fully_connected(network, 3, activation='softmax')
network = regression(network, optimizer='momentum',
                     loss='categorical_crossentropy',
                     learning_rate=0.001)

# Training
model = tflearn.DNN(network, checkpoint_path='rover_weights_path',
                    max_checkpoints=1, tensorboard_verbose=2)

path = '/home/mpcr/RaceTrackRover/weights/rover_weights2.tf1'

model.load(path)

model.fit(X, Y, n_epoch=40, validation_set=0.1, shuffle=True,
          show_metric=True, batch_size=64, snapshot_step=1000,
          snapshot_epoch=False, run_id='rover_weights_id')

path = '/home/mpcr/RaceTrackRover/weights/rover_weights3.tf1'

model.save(path) #safeguard
print("model saved")


