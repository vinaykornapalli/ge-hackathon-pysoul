import os
import pandas as pd
import shutil


def filter_content():
    if os.path.isdir('output'):
        #if already exists remove it
        shutil.rmtree('output')
    dirs = [name for name in os.listdir('content') if os.path.isdir(os.path.join('content', name))]

    for directory in dirs:
        path = 'content/'+directory
        img = pd.read_csv(path+'/image_log.csv')
        img = img.iloc[:,:].values
        
        for i in range(len(img)):
            if img[i,-1] == 'fingerprint' or img[i,-1] == 'person' or img[i,-1] ==  'signature':
                print(img[i,0])
                os.remove(img[i,0])
             
        for file in os.listdir(path):            
            if file.endswith('.txt'):
                if file != 'output.txt':
                    print(file)
                    os.remove(path+'/'+file)
                    
            if file.endswith('.csv'):
                print(file)
                os.remove(path+'/'+file)
            
            if file == 'outfile.png':
                print(file)
                os.remove(path+'/'+file)
    
    os.rename('content', 'output')
    
            
            
    