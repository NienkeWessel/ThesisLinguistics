from xml.dom import minidom

import lxml.etree as etree
import os
import pandas as pd


def readXMLfile(filename, df = pd.DataFrame(columns=['Name','Age','word','model','actual'])):
    """
        Reads Childes XML file and appends to data frame the name age correct word(orthography)
        correct pronounciation and uttered pronounciation per utterance
        
        filename = the name of the file to be read
        df = the current data frame; optional, if not specified, function will make a new data frame
    """


    # parse an xml file by name
    f = minidom.parse(filename)

    #use getElementsByTagName() to get tag
    session = f.getElementsByTagName('session')[0]
    child_name = session.getElementsByTagName('participants')[0].getElementsByTagName('participant')[0].getElementsByTagName('name')[0].firstChild.data
    child_age = session.getElementsByTagName('participants')[0].getElementsByTagName('participant')[0].getElementsByTagName('age')[0].firstChild.data
    
    transcript = session.getElementsByTagName('transcript')[0].getElementsByTagName('u')
    for u in transcript: 
        word = u.getElementsByTagName('orthography')[0].getElementsByTagName('g')[0].getElementsByTagName('w')[0].firstChild.data
        l = u.getElementsByTagName('ipaTier')
        
        col = []
    
        for attr in l:
            col.append( (attr.attributes['form'].value, attr.getElementsByTagName('pg')[0].getElementsByTagName('w')[0].firstChild.data) )
        
        dic = {'Name': child_name, 'Age': child_age, 'word': word, col[0][0]: col[0][1], col[1][0]: col[1][1]}

        df = df.append(dic, ignore_index = True)


    print(df)
    pretty_xml = f.toprettyxml()
    # remove the weird newline issue:
    pretty_xml = os.linesep.join([s for s in pretty_xml.splitlines()
                                  if s.strip()])
    #print(pretty_xml)
    #x = etree.parse(filename)
    #print(etree.tostring(x, pretty_print=True))

    # one specific item attribute
    #print('model #2 attribute:')
    #print(models[1].attributes['name'].value)

    # all item attributes
    #print('\nAll attributes:')
    #for elem in models:
    #  print(elem.attributes['name'].value)

    # one specific item's data
    #print('\nmodel #2 data:')
    #print(models[1].firstChild.data)
    #print(models[1].childNodes[0].data)

    # all items data
    #print('\nAll model data:')
    #for elem in models:
    #  print(elem.firstChild.data)
    #https://www.studytonight.com/python-howtos/how-to-read-xml-file-in-python#:~:text=a%20single%20tree.-,Example%20Read%20XML%20File%20in%20Python,XML%20file%20using%20getroot()%20.
    return df

filename = "011010.xml"
readXMLfile(filename)
