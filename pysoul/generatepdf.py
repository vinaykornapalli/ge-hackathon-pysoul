import os
import fitz
import pandas as pd

def generate_pdf(path, mode):
    if mode == 0:
        
        #access folder
        folder = 'content/'+(path.split('/')[-1]).split('.')[0]
        
        #open actual file                
        doc = fitz.open(path) 
        
        #open phi identified
        phi = pd.read_csv(folder+'/flair.csv')
        phi = phi[phi['type'] != 'CARDINAL']
        img = pd.read_csv(folder+'/image_log.csv')
        img = img.iloc[:,:].values
        
        final = fitz.open()
        for page_no in range(len(doc)):
            page = doc[page_no]
            for x in phi['text']:
                areas = page.searchFor(str(x), hit_max = 16)
                if areas != []:
                    for area in areas:
                        annot = page.addRectAnnot(area)
                        annot.setColors({"stroke":(1, 1, 1), "fill":(1,1,1)})
                        annot.update()
                        
            for i in range(len(img)):
                if str((str(img[i,0]).split('/')[-1]).split('_')[0]) == str(page_no):
                    if img[i,-1] == 'fingerprint' or img[i,-1] == 'person' or img[i,-1] ==  'signature' :
                        rect = fitz.Rect(img[i,1],img[i,2],img[i,3],img[i,4])
                        annot = page.addRectAnnot(rect)
                        annot.setColors({"stroke":(1, 1, 1), "fill":(1,1,1)})
                        annot.update()

            pix = page.getPixmap()
            output = str(folder)+'/outfile.png'
            pix.writePNG(output)
            txt_file= fitz.open(output)
            pdfbytes = txt_file.convertToPDF()
            pdf = fitz.open("pdf", pdfbytes)
            final.insertPDF(pdf)
  
        final.save(folder+'/output.pdf')
                    
    else:
        for file in os.listdir(path):
            if file.endswith('.pdf'):
                
                final = fitz.open()
                #make folder                
                folder = 'content/'+(file.split('/')[-1]).split('.')[0]
                
                #open file
                doc = fitz.open(path+'/'+file) 
                    
                phi = pd.read_csv(folder+'/flair.csv')
                phi = phi[phi['type'] != 'CARDINAL']
                img = pd.read_csv(folder+'/image_log.csv')
                img = img.iloc[:,:].values
                

                for page_no in range(len(doc)):
                    page = doc[page_no]
                    for x in phi['text']:
                        areas = page.searchFor(str(x), hit_max = 16)
                        if areas != []:
                            for area in areas:
                                annot = page.addRectAnnot(area)
                                annot.setColors({"stroke":(1, 1, 1), "fill":(1,1,1)})
                                annot.update()
                                
                        for i in range(len(img)):
                            if str((str(img[i,0]).split('/')[-1]).split('_')[0]) == str(page_no):
                                if img[i,-1] == 'fingerprint' or img[i,-1] == 'person' or img[i,-1] ==  'signature' :
                                    rect = fitz.Rect(img[i,1],img[i,2],img[i,3],img[i,4])
                                    annot = page.addRectAnnot(rect)
                                    annot.setColors({"stroke":(1, 1, 1), "fill":(1,1,1)})
                                    annot.update()
                                    
                    pix = page.getPixmap()
                    output = str(folder)+'/outfile.png'
                    pix.writePNG(output)
                    txt_file= fitz.open(output)
                    pdfbytes = txt_file.convertToPDF()
                    pdf = fitz.open("pdf", pdfbytes)
                    final.insertPDF(pdf)
                        
                final.save(folder+'/output.pdf')