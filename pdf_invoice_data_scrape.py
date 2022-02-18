from ast import Break, keyword
from re import X
import pytesseract as tess
from PIL import Image
import cv2


class ocrByImageRegion:
    key_words_data_lists = []

    def __init__(self, file_path, folder_path = ''):
        self.file_path = file_path
        self.folderpath = folder_path
        ocrByImageRegion.get_getword_coordinates(self)

    #compiles
    def get_getword_coordinates(self):
        img_lines = tess.image_to_data(self.file_path)
        keyWords = ['CUSTOMER', 'INFORMATION:', 'JOB', 'DISCIPLINE:', 'PHONE:', 'EMAIL:']
        ocrByImageRegion.key_words_data_lists.clear()
        for line in img_lines.splitlines():
            line_data = line.split()
            if len(line_data) == 12:
                if line_data[11].upper() in keyWords:
                    del line_data[0:6]
                    ocrByImageRegion.key_words_data_lists.append(line_data)
        return ocrByImageRegion.key_words_data_lists
    
    
    #compiles
    def create_roi(self, keyword, image, index, xoffset, yoffset, xroi, yroi):
        x = int(ocrByImageRegion.key_words_data_lists[index][0]) - xoffset
        y = int(ocrByImageRegion.key_words_data_lists[index][1]) + yoffset
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
        for i, list in enumerate(ocrByImageRegion.key_words_data_lists):
            keyword_from_array = ocrByImageRegion.key_words_data_lists[i][5].upper()
            if keyword_from_array == 'CUSTOMER':
                return ocrByImageRegion.create_roi(self, keyword_from_array, img, i, 10, 15, 200, 20)

    #compiles with create_roi()
    def get_customer_email (self):
        img = cv2.imread(self.file_path, 0)
        for i, list in enumerate(ocrByImageRegion.key_words_data_lists):
            keyword_from_array = ocrByImageRegion.key_words_data_lists[i][5].upper()
            if keyword_from_array == 'EMAIL:' :
                return ocrByImageRegion.create_roi(self, keyword_from_array, img, i, -30, -5, 150, 20)
        

    #compiles with create_roi()        
    def get_customer_address(self):
        img = cv2.imread(self.file_path, 0)
        for i, list in enumerate(ocrByImageRegion.key_words_data_lists):
            keyword_from_array = ocrByImageRegion.key_words_data_lists[i][5].upper()
            if keyword_from_array == 'CUSTOMER' :
                return ocrByImageRegion.create_roi(self, keyword_from_array, img, i, 10, 30, 150, 40)
            

    #compiles with create_roi()        
    def get_job_type(self):
        img = cv2.imread(self.file_path, 0)
        x, y = 0, 0
        for i, list in enumerate(ocrByImageRegion.key_words_data_lists):
            keyword_from_array = ocrByImageRegion.key_words_data_lists[i][5].upper()
            if keyword_from_array == 'DISCIPLINE:':
                return ocrByImageRegion.create_roi(self, keyword_from_array, img, i, -52, -5, 165, 18)
                
    

folder_path = r"/Users/munasef/Documents/python/opencv_project/work orders"
file_path1 = r"/Users/munasef/Documents/python/opencv_project/work orders/58580704  489 JAMESTOWN DR LEHIGHTON  (RMUG)_1.jpg"

ocr1 = ocrByImageRegion(file_path1, folder_path)
#x = ocr1.get_customer_name()
#print (x)
#ocr1.get_customer_address()
#print(x)
#ocr1.get_job_type()
#ocr1.get_invoice_number()
ocr1.get_customer_email()

