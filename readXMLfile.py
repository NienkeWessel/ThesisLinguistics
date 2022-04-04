from xml.dom import minidom

import lxml.etree as etree
import os
import pandas as pd
import fnmatch


def readXMLfile(filename, df = pd.DataFrame(columns=['Name','Age','word','model','actual'])):
    """
        Reads Childes XML file and appends to data frame the name age correct word(orthography)
        correct pronounciation and uttered pronounciation per utterance
        
        filename = the name of the file to be read
        df = the current data frame; optional, if not specified, function will make a new data frame
    """
    
    # Counter counts how many items were problematic to parse in some sense, for future reference purposes
    skipcounter = 0


    # parse an xml file by name
    f = minidom.parse(filename)

    #use getElementsByTagName() to get tag
    session = f.getElementsByTagName('session')[0]
    child_name = session.getElementsByTagName('participants')[0].getElementsByTagName('participant')[0].getElementsByTagName('name')[0].firstChild.data
    try: 
        child_age = session.getElementsByTagName('participants')[0].getElementsByTagName('participant')[0].getElementsByTagName('age')[0].firstChild.data
    except:
        child_age = 'N/A'
    
    transcript = session.getElementsByTagName('transcript')[0].getElementsByTagName('u')
    for u in transcript: 
        skip = False # skip boolean keeps track of whether something is wrong in the data
        word = u.getElementsByTagName('orthography')[0].getElementsByTagName('g')[0].getElementsByTagName('w')[0].firstChild.data
        l = u.getElementsByTagName('ipaTier')
        
        col = []
    
        for attr in l:
            ipa = attr.getElementsByTagName('pg')[0].getElementsByTagName('w')[0].firstChild
            if ipa is None:
                # if ipa is None, something is wrong, so we skip; no use to continue in this word, so break
                skip = True
                break
            else: 
                col.append( (attr.attributes['form'].value, ipa.data) )
        
        if not skip:
            # We append name, age, word and the actual and model pronun to the list. We do not know/assume in which order the latter two occur, so we use the dictionary structure to account for that and match the value with dict names
            dic = {'Name': child_name, 'Age': child_age, 'word': word, col[0][0]: col[0][1], col[1][0]: col[1][1]}
            df = df.append(dic, ignore_index = True)
        else:
            # We skipped one, so we increment the counter
            skipcounter += 1


    # OLD STUFF 
    # MIGHT BE USEFUL IN THE FUTURE 
    
    #print(df)
    #pretty_xml = f.toprettyxml()
    # remove the weird newline issue:
    #pretty_xml = os.linesep.join([s for s in pretty_xml.splitlines()
    #                              if s.strip()])
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
    
    
    # Signal ending of file reading and return completed dataframe
    print("done reading {}, skipped {} items".format(filename, skipcounter))
    return df


def find_files(root_folder='../CLPF'):
    """
    Code from stack overflow: https://stackoverflow.com/questions/2186525/how-to-use-glob-to-find-files-recursively
    """
    
    matches = []
    for root, dirnames, filenames in os.walk(root_folder):
        for filename in fnmatch.filter(filenames, '*.xml'):
            if 'project' in filename:
                continue
            matches.append(os.path.join(root, filename))
    return matches


def save_data(filename, df):
    """
    Code from: https://www.kite.com/python/answers/how-to-save-a-pandas-dataframe-in-python
    """
    df.to_pickle(filename)


def read_data(filename):
    """
    Code from: https://www.kite.com/python/answers/how-to-save-a-pandas-dataframe-in-python
    """
    return pd.read_pickle(filename)



# Collect all the file names, you can give it a root folder if you want to
filenames = find_files(root_folder='../Grimm')
#print(filenames)

# To test if it all works (and it does (or did, at least))
#df2 = readXMLfile("011010.xml")
#save_data("test.pkl", df2)

# Make empty data frame for the loop
df = pd.DataFrame(columns=['Name','Age','word','model','actual'])

# Loop through all the files and append to current dataframe
for filename in filenames:
    print('file opened: ' + filename)
    df = readXMLfile(filename, df)

df.rename(columns={'actual': 'realization'}, inplace=True)

print(df)
# Save data frame to pickle file
save_data("Grimm.pkl", df)

