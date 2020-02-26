import os
import glob
import pandas as pd
import re

def generate_text():
    dirs = [name for name in os.listdir('content') if os.path.isdir(os.path.join('content', name))]
    for directory in dirs:
        output = ''
        path = 'content/'+directory
        phi = pd.read_csv(path+'/flair.csv')
        phi = phi[phi['type'] != 'CARDINAL']
        count = 0
        for infile in sorted(glob.glob(os.path.join(path,'*.txt'))):
            f = open(infile, "r")
            text = f.read()
            for x in phi['text']:
                text = re.sub(re.escape(str(x)),str(' '*len(x)), text)
            output = output+text

        txt_file= open(path+'/output.txt','w')
        txt_file.write(output)
        txt_file.close()
        