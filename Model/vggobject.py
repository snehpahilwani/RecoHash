# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 22:16:19 2017

@author: snehc
"""

from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD
import cv2, numpy as np
from keras import backend as K
import bottleneck as bn
from keras.utils import plot_model


K.set_image_dim_ordering('tf')


global model_loaded
model_loaded = False
model_weights_path = 'D:\\RecoHash\\Model\\vgg16_weights_tf_dim_ordering_tf_kernels.h5'

if not model_loaded:
#def VGG_16(weights_path=None):
    model = Sequential()
    model.add(ZeroPadding2D((1,1),input_shape=(224,224,3)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(128, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(128, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(Flatten())
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1000, activation='softmax'))
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='categorical_crossentropy')
    model.load_weights(model_weights_path)
    model_loaded = True

    #return model
print('VGG16 model loaded')

file_name = 'D:\\RecoHash\\Model\\synset_words.txt'

classes = list()
with open(file_name) as class_file:
    for line in class_file:
        #print(line)
        #print(line.split(' ')[1])
        classes.append(line.strip().split(' ')[1:])
classes = tuple(classes)

#To detect faces
def is_face_present(image):
    face_cascade = cv2.CascadeClassifier('D:\\RecoHash\\Model\\haarcascade_frontalface_default.xml')
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    faces_bool = len(faces)
    is_face = 0
    if faces_bool != 0:
        is_face = 1
        
    return is_face


def predict(image):
#if __name__ == "__main__":
    im = cv2.resize(cv2.imread(image), (224, 224)).astype(np.float32)
    im[:,:,0] -= 103.939    
    im[:,:,1] -= 116.779
    im[:,:,2] -= 123.68
    im = im.transpose((1,0,2))
    im = np.expand_dims(im, axis=0)
    out = model.predict(im)
    return classes[np.argmax(out)]

#def top_n_indexes(arr, n):
#    idx = bn.argpartition(arr, arr.size-n, axis=None)[-n:]
#    width = arr.shape[1]
#    return [divmod(i, width) for i in idx]


#def myprint(s):
#    with open('D:\\RecoHash\\Model\\modelsummary.txt','w+') as f:
#        print(s, file=f)

# Test pretrained model
#model = VGG_16('D:\\RecoHash\\Model\\vgg16_weights_tf_dim_ordering_tf_kernels.h5')
#model.summary(print_fn=myprint)

#plot_model(model, to_file='model.png')



#np.random.seed(67)
##arr = np.random.rand(50, 50)
#idx = top_n_indexes(out, 8)
#idx.sort(key = lambda tup: tup[0])
#print(idx)