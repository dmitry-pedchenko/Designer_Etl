import xml.etree.ElementTree as et

root = et.Element('main')
et.SubElement(root, 'dbtype')
et.SubElement(root, 'dbHost')
et.SubElement(root, 'dbUser')
et.SubElement(root, 'dbPass')
et.SubElement(root, 'dbBase')
et.SubElement(root, 'dbPort')
et.SubElement(root, 'loadMode')
et.SubElement(root, 'dict')
et.SubElement(root, 'checkMode')

import_columns = et.Element('importXml')
export_columns = et.Element('exportTable')

root.append(import_columns)
root.append(export_columns)

import_columns.attrib['mode'] = 'true'
import_columns.text = 'main'




print(et.dump(root))