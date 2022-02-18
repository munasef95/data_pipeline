from ast import Break, keyword
from re import X
import pytesseract as tess
from PIL import Image
import cv2


class ocrByImageRegion:

    def __init__(self, file_path = ''):
        self.file_path = file_path
        self.key_words_data_lists = []
        self.get_getword_coordinates()
        

    #compiles
    def get_getword_coordinates(self): 
        img_lines = tess.image_to_data(self.file_path)
        keyWords = ['CUSTOMER', 'INFORMATION:', 'JOB', 'DISCIPLINE:', 'PHONE:', 'EMAIL:']
        for line in img_lines.splitlines():
            line_data = line.split()
            if len(line_data) == 12:
                if line_data[11].upper() in keyWords:
                    del line_data[0:6]
                    self.key_words_data_lists.append(line_data)
        return self.key_words_data_lists
    
    
    #compiles
    def create_roi(self, image, index, xoffset, yoffset, xroi, yroi):
        x = int(self.key_words_data_lists[index][0]) - xoffset
        y = int(self.key_words_data_lists[index][1]) + yoffset
        name_roi = image[y: y + yroi, x: x + xroi]
        #cv2.imshow(keyword + ' WINDOW', name_roi)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        extracted_data = tess.image_to_string(name_roi).strip()
        #print (extracted_data)
        return extracted_data

    #compiles. create_roi() not required 
    def get_invoice_number(self):
        img = cv2.imread(self.file_path, 0)
        WO_ROI =  img[0:60, 0:300]
        cv2.imshow('WO ', WO_ROI)
        return (tess.image_to_string(WO_ROI).strip()[-8:])
        

    #compiles with create_roi()
    def get_customer_name (self):
        img = cv2.imread(self.file_path, 0)
        x, y = 0, 0
        for i, list in enumerate(self.key_words_data_lists):
            keyword_from_array = self.key_words_data_lists[i][5].upper()
            if keyword_from_array == 'CUSTOMER':
                return self.create_roi(img, i, 10, 15, 200, 20)

    #compiles with create_roi()
    def get_customer_email (self):
        img = cv2.imread(self.file_path, 0)
        for i, list in enumerate(self.key_words_data_lists):
            keyword_from_array = self.key_words_data_lists[i][5].upper()
            if keyword_from_array == 'EMAIL:' :
                return self.create_roi(img, i, -30, -5, 150, 20)
        

    #compiles with create_roi()        
    def get_customer_address(self):
        img = cv2.imread(self.file_path, 0)
        for i, list in enumerate(self.key_words_data_lists):
            keyword_from_array = self.key_words_data_lists[i][5].upper()
            if keyword_from_array == 'CUSTOMER' :
                return self.create_roi(img, i, 10, 30, 150, 40)
            

    #compiles with create_roi()        
    def get_job_type(self):
        img = cv2.imread(self.file_path, 0)
        x, y = 0, 0
        for i, list in enumerate(self.key_words_data_lists):
            keyword_from_array = self.key_words_data_lists[i][5].upper()
            if keyword_from_array == 'DISCIPLINE:':
                return self.create_roi(img, i, -52, -5, 165, 18)
                
    

#folder_path = r"/Users/munasef/Documents/python/opencv_project/work orders"
file_path1 = r"/Users/munasef/Documents/python/opencv_project/work orders/58583717  381 SNOWDRIFT RD ANDREAS  (RNSU)_1.jpg"
ocr1 = ocrByImageRegion(file_path1)
#print (x)
#print(x)
print ('\n' + ocr1.get_customer_name() + '\n')
print ('\n' + ocr1.get_customer_address() + '\n')
print ('\n' + ocr1.get_job_type() + '\n')
print ('\n' + ocr1.get_invoice_number() + '\n')
print ('\n' + ocr1.get_customer_email() + '\n')

