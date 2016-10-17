import lxml.etree as etree
import requests
import StringIO
from pprint import pprint

root_url = 'http://ostriv.in.ua/'
HTMLpage = requests.get(root_url).text
tree = etree.HTML(HTMLpage)
urls = tree.xpath('/html/body//a//@href')
xml_root = etree.Element('data')

count = 0
for url in urls:
    if url.find('ostriv.in.ua') >= 0 and url.find("mailto") ==-1 and count < 20:
        # print(url)
        xml_page = etree.SubElement(xml_root,"page", url=url)
        count = count+1
        page = requests.get(url).text
        tree = etree.HTML(page)
        imgs = tree.xpath('/html/body//img/@src')
        xml_img = etree.SubElement(xml_page,"fragment", type="image")
        xml_img.text = (', ').join(imgs)

        texts = tree.xpath('/html/body//p//text()')
        xml_text = etree.SubElement(xml_page,"fragment", type="text")
        xml_text.text = (' ').join(texts)
        # pprint(img)

# print(etree.tostring(xml_root, pretty_print=True))
with open("lab2_1_1.xml","w") as f:
    f.write(etree.tostring(xml_root, pretty_print=True, encoding='utf-8', xml_declaration= True))






