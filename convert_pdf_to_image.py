from importlib.metadata import files

import cv2
import numpy as np
import pdf2image
import os
import subprocess
from scanned_invoice_data_scraper import ExtractText


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

# imagify1 = ImagifyPdf(folder_path)
# imagify1.convert_all_pdf_in_folder(100)

extract1 = ExtractText(folder_path, file_path1)
extract1.make_rectangles()

