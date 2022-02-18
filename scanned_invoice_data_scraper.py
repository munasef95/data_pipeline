import cv2
import numpy as np
 
class ExtractText:
    def __init__(self, folder_path, image_path=" "):
        self.image_path = image_path
        self.folder_path = folder_path

    def make_rectangles(self):
        im = cv2.imread(self.image_path)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        #blur makes thresholding worse
        #blur = cv2.GaussianBlur(gray, (9, 9), 0)
        #---------------------------------------------------------------------------
        #thresholding is a way to separate the foregrand from the background
        #things we are interested in is the foreground
        thresh = cv2.adaptiveThreshold(gray, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 30)
        print(thresh.shape)
        print(thresh)
        # create a
        kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))
        # DILATING TO COMBINE ADJ TEXT CONTOURS
        dilate = cv2.dilate(thresh, kernal, iterations=1)

        cv2.imshow("thresh", cv2.resize(thresh, (980, 1060)))
        cv2.imshow("kernal", cv2.resize(kernal, (980, 1060)))
        cv2.imshow("dilate", cv2.resize(dilate, (980, 1060)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # find contours, highlight text areas, and extract region of interests
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

    #alternative method howevever text boxes are not as accurate as make_rectangles()
    def make_rectangles2 (self):
        large = cv2.imread(self.image_path)
        rgb = cv2.pyrDown(large)
        small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

        _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
        connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
        # using RETR_EXTERNAL instead of RETR_CCOMP
        contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # For opencv 3+ comment the previous line and uncomment the following line
        # _, contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        mask = np.zeros(bw.shape, dtype=np.uint8)

        for idx in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[idx])
            mask[y:y + h, x:x + w] = 0
            cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
            r = float(cv2.countNonZero(mask[y:y + h, x:x + w])) / (w * h)

            if r > 0.45 and w > 8 and h > 8:
                cv2.rectangle(rgb, (x, y), (x + w - 1, y + h - 1), (0, 255, 0), 2)

        cv2.imshow('rects', cv2.resize(rgb, (980, 1080)))
        cv2.waitKey()
        cv2.destroyAllWindows()




