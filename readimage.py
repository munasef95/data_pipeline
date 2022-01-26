from importlib.metadata import files

import cv2
import numpy as np
import pdf2image
import os
from PIL import Image
import subprocess

def convert_pdf_to_image(pdfPath, dpi):
    pages = pdf2image.convert_from_path(pdfPath, dpi)
    i=1
    os.chdir(fpath)
    for page in pages:
        imagename = os.path.splitext(convert_all_pdf_in_folder.filename)[0] + "_" + str(i) + ".jpg"
        page.save(imagename, "JPEG")
        i = i +1

def convert_all_pdf_in_folder (folderpath, dpi):
    for file in os.listdir(folderpath):
        absfilepath = os.path.join(folderpath, file)
        convert_all_pdf_in_folder.filename = file
        if os.path.splitext(absfilepath)[1].lower() == '.pdf' :
            print(absfilepath)
            input("press any key to continue")
            convert_pdf_to_image(absfilepath, dpi)
        else:
            pass

def make_rectangles(image_path):
    im = cv2.imread(image_path)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(9,9),0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)

    #DILATING TO COMBINE ADJ TEXT CONTOURS
    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernal, iterations=4)

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
    cv2.imshow('image_1', cv2.resize(image, (980, 1060)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image, line_items_coordinates


fpath = r"C:\Users\MNSF\Documents\pdftoscan"
imagepath1 = "C:\\Users\\MNSF\\Documents\\pdftoscan\\toll_1.jpg"
imagepath2 = "C:\\Users\\MNSF\\Documents\\pdftoscan\\covidVaccinationCard_1.jpg"
make_rectangles(imagepath2)
#convert_all_pdf_in_folder(fpath, 600)
# convert_pdf_to_image(fpath,600)
