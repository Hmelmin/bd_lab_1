import lxml.etree as etree
with open ('template.xsl') as template:
    xslt_context = template.read()
    xslt_root = etree.XML(xslt_context)
    dom = etree.parse('lab2_1_3.xml')
    transform = etree.XSLT(xslt_root)
    result = transform(dom)
    with open("lab2_1_4.html","w") as f:
        f.write(str(result))