# Thesis Linguistics
Code used to extract child stress patterns from PhonBank corpora

## How to use
After cloning this repo, you need to download the corpora from the PhonBank website (https://phon.talkbank.org/access/). You can then use the readXMLfile.py script to read in the xml files in the corpus to a .pkl file (pikkle is a python library that allows you to save python objects). The folder downloaded from PhonBank should be one folder level higher than the code. 

You can then use the ProcessData.ipynb notebook to read in the corpus. Note that you will have to add the corpus to the different settings dictionaries with the right settings. This might take some trial and error. If it does not work out, feel free to contact me for help. 
