import cv2
import numpy as np
import pdf2image
import os
from PIL import Image
import subprocess

class ExtractText:
    def __init__(self, folder_path, image_path = " "):
        self.image_path = image_path
        self.folder_path = folder_path

    def make_rectangles(self):
        im = cv2.imread(self.image_path)
        print(im)

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(9,9),0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)

        #DILATING TO COMBINE ADJ TEXT CONTOURS
        kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
        dilate = cv2.dilate(thresh, kernal, iterations=2)

        cv2.imshow("dilate", cv2.resize(dilate,  (980, 1060)))
        cv2.waitKey(0)
        

        #find contours, highlight text areas, and extract region of interests
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        line_items_coordinates = []
        for c in cnts:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)

            if y >= 600 and x <= 1000:
                if area > 10000:
                    image = cv2.rectangle(im, (x, y), (2200, y + h), color=(255, 0, 255), thickness=3)
                    line_items_coordinates.append([(x, y), (2200, y + h)])
            if y >= 2400 and x <= 2000:
                image = cv2.rectangle(im, (x, y), (2200, y + h), color=(255, 0, 255), thickness=3)
                line_items_coordinates.append([(x, y), (2200, y + h)])
            else:
                image = cv2.rectangle(im, (x, y), (2200, y + h), color=(255, 0, 255), thickness=3)
                line_items_coordinates.append([(x, y), (2200, y + h)])

        cv2.imshow('image_1', cv2.resize(image, (980, 1060)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return image, line_items_coordinates

class ImagifyPdf:
    def __init__(self, folderpath, filepath = ""):
        self.folderpath = folderpath
        self.filepath = filepath

    def convert_pdf_to_image(self, dpi):
        pages = pdf2image.convert_from_path(self.filepath, dpi)
        i = 1
        os.chdir(self.folderpath)
        for page in pages:
            imagename = os.path.splitext(self.filepath)[0] + "_" + str(i) + ".jpg"
            page.save(imagename, "JPEG")
            i = i +1

    def convert_all_pdf_in_folder (self, dpi):
        for file in os.listdir(self.folderpath):
            self.filepath = os.path.join(self.folderpath, file)
            if os.path.splitext(self.filepath)[1].lower() == '.pdf':
                print(self.filepath)
                input("press any key to continue")
                self.convert_pdf_to_image(dpi)
            else:
                pass


folder_path = r"C:\Users\pdftoscan"
file_path = r"C:\Users\pdftoscan\invoice_1.jpj"

imagify1 = ImagifyPdf(folder_path, file_path)
imagify1.convert_all_pdf_in_folder(100)

# file_path is optional 
extract_text1 = ExtractText(folder_path, file_path)
extract_text1.make_rectangles()

