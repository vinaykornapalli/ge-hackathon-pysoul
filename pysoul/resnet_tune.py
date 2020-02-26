import numpy as np
import pandas as pd
from keras.models import Model
from keras.applications import Xception
import numpy as np
import os
import glob
import time
from keras.applications import ResNet50
from keras.preprocessing import image
from keras.layers import GlobalAveragePooling2D, Dense, Dropout,Activation,Flatten
from keras.applications.imagenet_utils import preprocess_input
from keras.layers import Input
from keras.models import Model
from keras.utils import np_utils
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import tensorflow as tf

# config = tf.ConfigProto(device_count ={'GPU':0})
# sess = tf.Session(config=config)

def resnet_detection(model):
    dirs = [name for name in os.listdir('content') if os.path.isdir(os.path.join('content', name))]
    names = ['fingerprint', 'medical' ,'person', 'signature']
    
    for directory in dirs:
        path = 'content/'+directory
        image_log = pd.read_csv(path+'/image_log.csv')
        image_log['label'] = 'neutral'
        image_log = image_log.iloc[:,:].values
        
        for i in range(len(image_log)):
            total_path = image_log[i,0]
            file = total_path.split('/')[-1]
            img = image.load_img(path+'/'+file, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            output = model.predict(x)
            maximum = max(output[0])
            for p in range(0,4):
                if output[0][p] == maximum:
                    category = p
                    break
            image_log[i,-1] = names[category]
                
    
        (pd.DataFrame(image_log)).to_csv(path+'/image_log.csv',index=None)
                