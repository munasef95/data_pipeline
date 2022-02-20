from pdf_invoice_data_scrape import ocrByImageRegion
from xml_dump import xml1
import os


if __name__ == "__main__":
    folder_path = r"/Users/munasef/Documents/python/opencv_project/work orders"
    # invoice_jpg = [r"/Users/munasef/Documents/python/opencv_project/work orders/58581262  425 VILNO DR LEHIGHTON  (RNSU)_1.jpg", r"/Users/munasef/Documents/python/opencv_project/work orders/58581788  133 CLAREMONT AVE TAMAQUA  (NALE)_1.jpg"]
    invoice_jpg =[]

    for file in os.listdir(folder_path):
        if os.path.splitext(file)[1].lower() == '.jpg':
            invoice_jpg.append(os.path.join(folder_path,file))

    print (folder_path)

    for item in invoice_jpg:
        print(item)
        print('\n') 

    for invoice in invoice_jpg:
        try:
            ocr1 = ocrByImageRegion(invoice)
            ocr1.get_customer_email()
            invoice = ocr1.get_invoice_number()
            job_type = ocr1.get_job_type()
            cName = ocr1.get_customer_name()
            cEmail = ocr1.get_customer_email()
            cAddress = ocr1.get_customer_address()
            xml1.test_xml_dump ('invoice_data.xml', invoice, job_type, cName, cEmail, cAddress)
        except:
            print ('\n' + 'Error reading: ' + invoice)