import os
import fitz
import pandas as pd
import shutil

def extract_content(path, mode):
    if os.path.isdir('content'):
        #if already exists remove it
        shutil.rmtree('content')
    
    os.mkdir('content')    
    if mode == 0:
        
        #make folder
        folder = 'content/'+(path.split('/')[-1]).split('.')[0]
        os.mkdir(folder)
        
        #open file                
        doc = fitz.open(path) 
        
        #log files
        image_path = []  
        image_coord = []
        
        #extract content
        for page_no in range(len(doc)):
            
            #extract_text
            page = doc.loadPage(page_no) 
            text = page.getText('text')
            txt_file= open(folder+'/'+ str(page_no)+'.txt','w')
            txt_file.write(text)
            txt_file.close()
        
            #image bounding boxes
            char = page.getText('dict')
            for block in char['blocks']:
                if block['type'] == 1:
                    image_coord.append(block['bbox'])
                        
            #extract_images
            image_no=0
            for image in doc.getPageImageList(page_no):
                image_no+=1
                customxref = image[0]
                pic = fitz.Pixmap(doc, customxref)
                finalpic = fitz.Pixmap(fitz.csRGB, pic)
                finalpic.writePNG(folder+'/'+str(page_no)+ '_'+str(image_no)+'.png')
                image_path.append(folder+'/'+str(page_no)+ '_'+str(image_no)+'.png')
        
        for i in range(len(image_coord)):
            image_coord[i] = list(image_coord[i])
        
        image_log = pd.concat([pd.Series(image_path),pd.DataFrame(image_coord)], axis=1)
        image_log.columns = ['path','x1','y1','x2','y2']
        image_log.to_csv(folder+'/'+'image_log.csv',index=None)
        
    else:
        #traverse files
        for file in os.listdir(path):
            if file.endswith('.pdf'):
                
                #make folder                
                folder = 'content/'+(file.split('/')[-1]).split('.')[0]
                os.mkdir(folder)
                
                #open file
                doc = fitz.open(path+'/'+file) 
                
                #log files
                image_path = []  
                image_coord = []
                    
                #extract content                
                for page_no in range(len(doc)):
                    
                    #extract text 
                    page = doc.loadPage(page_no) 
                    text = page.getText('text')
                    txt_file= open(folder+'/'+ str(page_no)+'.txt','w')
                    txt_file.write(text)
                    txt_file.close()
                    
                    #image bounding boxes
                    char = page.getText('dict')
                    for block in char['blocks']:
                        if block['type'] == 1:
                            image_coord.append(block['bbox'])
                    
                    #extract images
                    image_no=0
                    for image in doc.getPageImageList(page_no):
                        image_no+=1
                        customxref = image[0]
                        pic = fitz.Pixmap(doc, customxref)
                        finalpic = fitz.Pixmap(fitz.csRGB, pic)
                        finalpic.writePNG(folder+'/'+str(page_no)+ '_'+str(image_no)+'.png')
                        image_path.append(folder+'/'+str(page_no)+ '_'+str(image_no)+'.png')
                        
                for i in range(len(image_coord)):
                    image_coord[i] = list(image_coord[i])
        
                        
                image_log = pd.concat([pd.Series(image_path),pd.DataFrame(image_coord)], axis=1)
                image_log.columns = ['path','x1','y1','x2','y2']
                image_log.to_csv(folder+'/'+'image_log.csv',index=None)


