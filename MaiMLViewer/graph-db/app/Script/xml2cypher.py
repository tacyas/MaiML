#!/usr/bin/env python3

import sys
import re
import xml.etree.ElementTree as ET
#import codecs

#sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

###
##  subtree(e=elem, h="", n=top_node, p=xmail_node, r='XML_Root', file=output)
def subtree(e, h, n, p, r, file=sys.stdout):
  tag2 = re.sub(r'^{.*}', '', e.tag)
  #print '#', h, n, e.tag, e.attrib, '=> "%s"' % tag2
  print('create (%s:XMLtag { __tag: "%s"' % (n, tag2), file=file)
  for name, value in list(e.attrib.items()):
    name2 = re.sub(r'^{.*}', '', name)
    name2 = name2.replace('.', '_')   ### attribute name may contain character '.'
    #print '#  "%s" = "%s"' % (name2, value)
    print('  , %s: "%s"' % (name2, value), file=file)
  print('  })', file=file)
  print('create (%s)-[:%s]->(%s)' % (p, r, n), file=file)

  if (e.text is not None) and (re.match('\S', e.text)):
    #print '#', h, "text: '%s'" % e.text
    #print('create (%s:XMLdata { value: "%s" })' % (n + "d", e.text), file=file)
    print('create (%s:XMLdata { value: "%s" })' % (n + "d", e.text if e.text[-1] != '\\' else e.text+'\\'), file=file)
    print('create (%s)-[:XML_Data]->(%s)' % (n, n + "d"), file=file)
  if (e.tail is not None) and (re.match('\S', e.tail)):
    #print '#', h, "tail: '%s'" % e.tail
    print('create (%s:XMLdata { value: "%s" })' % (n + "d", e.text), file=file)
    print('create (%s)-[:XML_Data]->(%s)' % (n, n + "d"), file=file)
  for i, s in enumerate(e):
    subtree(s, h + "[%d]>>> " % i, n + "_%d" % i, n, 'XML_Child', file=file)

###

def xml2cypher(fname, output=sys.stdout):
  import xml.sax.saxutils as  saxutils
  try:
    xmail_node = "nx"
    top_node = "n"
    #fname = sys.argv[1]
    #filename = os.path.basename(fname)

    ## 20240522 add
    with open(fname, "rt", encoding='utf-8') as f:
      maimlstr = f.read()   ## 改行とスペースが文字コードのリスト
    maimlstr_strip = maimlstr.strip("\t")
    #maimlstr_rstrip = maimlstr_strip.rstrip("\n")
    maimlstr_rstrip = maimlstr_strip.rstrip("\n")
    maimldata = maimlstr_rstrip.replace('&', '&amp;')
    #maimldata = maimlstr_rstrip.replace("¥", '&yen;')
    
    #tree = ET.parse(fname)  ## error -> maimldata.replace('&', '&amp;')
    elem = ET.fromstring(maimldata)
  except Exception as e:
    #sys.stderr.write('XMAIL:ERROR::{0}'.format(e))
    sys.stderr.write('XMAIL: XML file not found\n')
    sys.exit(-1)


  try:
    print('create (%s:XMAIL { file: %s})' % (xmail_node, ascii(str(fname))), file=output)

    #elem = tree.getroot()
    #sys.stderr.write('top level : ' + elem.tag + '\n')
    xmail_version = elem.attrib.get('xmail.version')
    if xmail_version is None:
      #xmail_version = elem.attrib.get('maiml.version')
      xmail_version = elem.attrib.get('version')
    if xmail_version is None:
      sys.stderr.write('XMAIL data not found\n')
      raise Exception
    elif not re.match('[01](\.)?', xmail_version):
      sys.stderr.write('xmail.version is not 0.x nor 1.x\n')
      raise Exception

    subtree(elem, "", top_node, xmail_node, 'XML_Root', file=output)
    print("return id(nx) as xmail_nid", file=output)
    print(";", file=output)

  except:
    sys.stderr.write('XMAIL: parse error\n')
    sys.exit(-2)

  #else:
  #  sys.exit(0)


if __name__ == "__main__":
  xml2cypher(sys.argv[1])


###
### end of script
###
