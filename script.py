from pdf_invoice_data_scrape import ocrByImageRegion
from xml_dump import xml1
import os


if __name__ == "__main__":
    folder_path = r"/Users/munasef/Documents/python/opencv_project/work orders"
    invoice_jpg = []
    
    for file in os.listdir(folder_path):
        if os.path.splitext(file)[1].lower() == '.jpg':
            invoice_jpg.append(os.path.join(folder_path,file))

    for invoice_file in invoice_jpg:
        print(invoice_file)
        ocr1 = ocrByImageRegion(invoice_file)
        ocr1.get_getword_coordinates()
        invoice = ocr1.get_invoice_number()
        job_type = ocr1.get_job_type()
        cName = ocr1.get_customer_name()
        cEmail = ocr1.get_customer_email()
        cAddress = ocr1.get_customer_address()
        xml1.test_xml_dump ('invoice_data.xml', invoice, job_type, cName, cEmail, cAddress)