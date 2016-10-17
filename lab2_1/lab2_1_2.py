import lxml.etree as etree

tree = etree.parse("lab2_1_1.xml")
hrefs = tree.xpath("//page/@url")
for href in hrefs:
    print(href)
