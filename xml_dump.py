import xml.etree.cElementTree as xml

class create_xml:
    def __init__(self, rootname):
        self.rootname = rootname
        self.root = xml.Element(self.rootname)
        
    def test_xml_dump(self, filename, sc1text, sc2text, sc3text, sc4text, sc5text):
        child1 = xml.Element("invoice")
        (self.root).append(child1)
 
        subchild1 = xml.SubElement(child1, "invoicenNumber")
        subchild2 = xml.SubElement(child1, "jobtype")
        subchild3 = xml.SubElement(child1, "customerName")
        subchild4 = xml.SubElement(child1, "customerEmail")
        subchild5 = xml.SubElement(child1, "customerAddress")

        subchild1.text = sc1text
        subchild2.text = sc2text
        subchild3.text = sc3text
        subchild4.text = sc4text
        subchild5.text = sc5text

        tree = xml.ElementTree(self.root)
        with open (filename, 'wb') as filenameopen:
            tree.write(filenameopen)
        filenameopen.flush()


xml1 = create_xml("INVOICE")