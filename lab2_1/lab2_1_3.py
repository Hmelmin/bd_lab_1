import requests
import lxml.etree as etree
root_url = "http://fishing-mart.com.ua"
HTMLpage = requests.get(root_url).text
root_tree = etree.HTML(HTMLpage)
categories = root_tree.xpath("//div[@id='categories_block_left']//ul/li/ul/li/a/@href")
xml_root = etree.Element('data')


counter = 0
for category in categories:
    if counter < 20:
        web_page = requests.get(category).text
        category_tree = etree.HTML(web_page)
        goods = category_tree.xpath("//ul[@id='product_list']/li/div[@class='center_block']/h3/a/@href")
        for good in goods:
            if counter < 20:
                counter = counter + 1
                good_page = requests.get(good).text
                good_tree = etree.HTML(good_page)
                name = good_tree.xpath('//*[@id="primary_block"]/h1/text()')
                price = good_tree.xpath("//div[@id='primary_block']//p[@class='price']/span/span/text()")
                description = good_tree.xpath("//div[@id='more_info_sheets']/div[@id='idTab1']//p//text()")
                image = good_tree.xpath("//*[@id='bigpic']/@src")
                # print(name)
                # print (image)
                xml_product = etree.SubElement(xml_root,'product')
                xml_name = etree.SubElement(xml_product,'name')
                xml_name.text = name[0]
                xml_price=etree.SubElement(xml_product,'price')
                xml_price.text = price[0]
                xml_description=etree.SubElement(xml_product,'description')
                xml_description.text = description[0]
                xml_image=etree.SubElement(xml_product,'image')
                xml_image.text = image[0]

with open("lab2_1_3.xml","w") as f:
    f.write(etree.tostring(xml_root, pretty_print=True, encoding='utf-8', xml_declaration= True))






