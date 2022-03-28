import pandas as pd
import numpy as np
import csv
import unittest


# ----------------------------------------------
class Word:
    def __init__(self, written, model, realization, rep_model, rep_realization):
        self.written = written
        self.model = model
        self.realization = realization
        self.rep_model = rep_model
        self.rep_realization = rep_realization
    
    def __eq__(self, other):
        return self.written == other.written
    


# ----------------------------------------------
class WordList:
    
    def __init__(self, time ):
        '''
        time: the point in time to which this wordlist refers
        '''
        self.time = time
        self.wordlist = set()
        
    def __cmp__(self, other):
        return cmp(self.time, other.time)
    
    def __repr__(self):
        return "%s" % (self.time)
    
    
    def add_word(word):
        self.wordlist.add(word)

    def add_prev_state_wordlist(prev_wordlist):
        for word in prev_wordlist.wordlist:
            self.wordlist.add(word)
            
# ----------------------------------------------
class ChildDevelopment:
    
    def __init__(self, name ):
        '''
        name: child's name (just for bookkeeping purposes)
        '''
        self.name = name
        self.wordlists = []
    
    
    def add_wordlist(self, wordlist):
        self.wordlists.append(wordlist)
    
    def calculate_total_vocab_dev(self):
        for wordlist in wordlists:
            

# ----------------------------------------------


ipa_vowels = ['a', 'ɑ', 'œ', 'y', 'o', 'ɑ̈', 'i', 'u', 'ɪ', 'ə', 'ɛ', 'e', 'ɔ', 'ʌ', 'ø̈', 'ɛ̝','ʉ', 'œ̞', 'œ', 'ɛ̞', 'ʔ', 'ɒ','ø', 'æ̝', 'ə̆', 'o͡', 'o̝']#, '͡'] 
agnostic_symbols = ['͡', 'ː'] # symbols that can either be a vowel or consonant

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

def append_representation_to_dataframe(df):
    '''
    Appends the syllable representations of the model and realization to the dataframe 
    to have all information in one place
    
    df: data set, of which the representations need to be appended
    
    No return, as it mutates the df object
    '''
    df['rep_model'] = df.model.apply(build_syllable_representation)
    df['rep_realization'] = df.realization.apply(build_syllable_representation)
    #print(df)

def write_nonmatches_to_csv(filename, df, comparison, header = ['Name', 'Age', 'word', 'model','realization','stressmodel','stressrealization'], apply_filter=True):
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        for n, a, word, w,v in collect_nonmatches_metadata(df, comparison):
            if not apply_filter:
                writer.writerow([n,a,word,w, v, build_syllable_representation(w), build_syllable_representation(v)])
            else:
                rep_w = build_syllable_representation(w)
                rep_v = build_syllable_representation(v)
                # If at least one of the two representations has 2 or more syllables, then we are interested
                if len(rep_w) >= 2 or len(rep_v) >= 2: 
                    writer.writerow([n,a,word,w, v, rep_w, rep_v])

def write_df_to_csv(filename, df):
    df.to_csv(filename)


def write_stats_to_csv(filename, a,b,c,d,e):
    '''
    stats_mod, stats_act, stats_match, stats_nonmatch_mod, stats_nonmatch_act
    '''
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(['number','modellengthall','realizationlengthall','lengthmatch', 'modellengthnonmatch', 'realizationlengthnonmatch'])

        # write the data
        for i in range(10):
            writer.writerow([i, a[i], b[i], c[i], d[i], e[i]])

    
    
def build_syllable_representation(word, secondary=False):
    """
    word: the word of which you want the syllable representation
    
    Returns the representation of the syllable in the form of a list of booleans, where true represents stressed and false unstressed
    """
    
    representation = []
    stressed = False
    vowels = False
    for c in list(word):
        #print(c)
        if secondary and (c == "ˈ" or c == "ˌ"):
            stressed = True
        elif not secondary and c == "ˈ":
            stressed = True
        elif c in ipa_vowels:
            if not vowels:
                vowels = True
                representation.append(stressed)
                stressed = False
        elif c not in agnostic_symbols: #if we do not know whether something is a vowel or consonant, we leave it be. If it is not a vowel and not agnostic, we have a consonant
            vowels = False
    return representation


def is_final_syllable_heavy(word):
    if word[-1] in ipa_vowels:
        # if the last letter is a vowel, we only have a heavy syllable if it is a diphtong, so if the letter before it is also a vowel
        return word[-2] in ipa_vowels
    else: #so final letter in agnostic_symbols or consonants
        return True


class MyTest(unittest.TestCase):
    def test_build_syllable_representation(self, secondary=False):
        '''
        Tests the build_syllable_representation function with different examples
        Also used to see if something breaks after adjusting
        '''
    
        if not secondary:
            #one syllable word, with bridge
            self.assertEqual([True], build_syllable_representation('ˈbu̠t͡s'))
            
            #simple two syllable words with different stress
            self.assertEqual([False, True], build_syllable_representation('koːˈlɛin'))
            self.assertEqual([True, False], build_syllable_representation('ˈpukə'))
            
            #other
            self.assertEqual([True, False, False], build_syllable_representation('ˈʔaːˌkleːdə'))
            
            self.assertEqual([True, False], build_syllable_representation('ˈpinoːŭ'))
            self.assertEqual([True, False, False], build_syllable_representation('ˈzeˌot͡jɑ̈s'))

    def test_is_final_syllable_heavy(self):
        self.assertEqual(True, is_final_syllable_heavy('ˈzeˌot͡jɑ̈s'))
        self.assertEqual(True, is_final_syllable_heavy('koːˈlɛin'))
        self.assertEqual(True, is_final_syllable_heavy('koˈnɛi'))
        self.assertEqual(False, is_final_syllable_heavy('ˈpukə'))
        self.assertEqual(True, is_final_syllable_heavy('ˈbu̠t͡s'))
        self.assertEqual(True, is_final_syllable_heavy('kˈɑpχː'))
        self.assertEqual(True, is_final_syllable_heavy('neː'))
        self.assertEqual(True, is_final_syllable_heavy('fiˈjoʋ')) 

    
        

def compare_realization_model(model, realization):
    '''
    
    '''
    assert(len(model) == len(realization))
    
    comparison = []
    unequal_lengths = []
    for i in np.arange(len(model)):
        mod_word = build_syllable_representation(model[i])
        act_word = build_syllable_representation(realization[i])
        if len(mod_word) != len(act_word):
            #print("not equal length", i, mod_word, act_word)
            unequal_lengths.append(i)
            comparison.append(False)
            continue
        problem_encountered = False
        for j in np.arange(len(mod_word)):
            if mod_word[j] != act_word[j]:
                problem_encountered = True
                continue
        comparison.append(not problem_encountered)
    return comparison, unequal_lengths

def collect_nonmatches_metadata(df, comparison):
    '''
    Finds the non matches within the data set and puts the model and the realization next to each other
    
    df: data set
    comparison: list of booleans that where true is a match and false is not a match
    
    returns a list of five-tuples of non-matching syllable structures preceded by the meta-data
    '''
    cases = []
    for i, boolean in enumerate(comparison):
        if not boolean:
            cases.append((df.Name[i], df.Age[i], df.word[i], df.model[i], df.realization[i]))
    return cases

def collect_nonmatches(df, comparison):
    '''
    Finds the non matches within the data set and puts the model and the realization next to each other
    
    df: data set
    comparison: list of booleans that where true is a match and false is not a match
    
    returns a list of pairs of non-matching syllable structures
    '''
    cases = []
    for i, boolean in enumerate(comparison):
        if not boolean:
            cases.append((df.model[i], df.realization[i]))
    return cases

def statistics(df, comparison, save=False):
    '''
    Calculates statistics on the syllable structure of the dataset 
    
    df: the data frame on which the statistics need to be calculated
    comparison: the list of booleans where true indicates model and realization match, and false that they do not match
    save: optional argument on whether to save the statistics to a csv file
    
    returns five dictionaries with statistics
    TODO TODO TODO 
    '''
    stats_mod, stats_act, stats_match, stats_nonmatch_mod, stats_nonmatch_act = {}, {}, {}, {}, {}
    for i in np.arange(10):
        stats_mod[i] = 0
        stats_act[i] = 0
        stats_match[i] = 0
        stats_nonmatch_mod[i] = 0
        stats_nonmatch_act[i] = 0
    #print(comparison)
    for i, boolean in enumerate(comparison):
        rep_mod = build_syllable_representation(df.model[i])
        rep_act = build_syllable_representation(df.realization[i])
        stats_mod[len(rep_mod)] += 1
        stats_act[len(rep_act)] += 1
        if boolean:
            stats_match[len(rep_mod)] += 1
        else:
            stats_nonmatch_mod[len(rep_mod)] += 1
            stats_nonmatch_act[len(rep_act)] += 1
    #print(stats_mod, stats_act, stats_match, stats_nonmatch_mod, stats_nonmatch_act)
    if save:
        write_stats_to_csv('stats.csv', stats_mod, stats_act, stats_match, stats_nonmatch_mod, stats_nonmatch_act)
    return stats_mod, stats_act, stats_match, stats_nonmatch_mod, stats_nonmatch_act


def collect_different_words(df):
    '''
    df: complete data set including representations
    '''
    words = set()
    for word in df['model']:
        words.add(word)
    return words

def make_df_words_repr(words):
    df = pd.DataFrame(columns=['word','representation'])
    for word in words:
        df = df.append({'word': word, 'representation': build_syllable_representation(word)}, ignore_index=True)
    return df

def stringify_representation(representation):
    '''
    representation: list of booleans (representing stress pattern
    
    returns: string of the stress pattern
    '''
    string = ""
    for boolean in representation: 
        if boolean:
            string += 'T'
        else:
            string += 'F'
    return string

def calculate_nr_word_types(df):
    strings = df['representation'].apply(stringify_representation)
    print(strings.value_counts())

def filter_iambic_bisyllabic_words(df):
    filter_bisyl = [True if l==2 else False for l in df.rep_model.apply(len) ]#df.rep_model.apply(len) #and df.rep_model[1]
    #print(filter_iamb)
    filtered = df[filter_bisyl]
    filter_iamb = [r[1] for r in filtered.rep_model]
    return filtered[filter_iamb] #Second thing returns booleans, we are interested when these are True
    
def filter_trisyllabic_words(df):
    filter_trisyl = [True if l==3 else False for l in df.rep_model.apply(len) ]#df.rep_model.apply(len) #and df.rep_model[1]
    #print(filter_iamb)
    return df[filter_trisyl]



def add_heavy_fin_syl_column(df):
    df['heavy_final_syl'] = df.model.apply(is_final_syllable_heavy)

test = MyTest()
test.test_build_syllable_representation()
test.test_is_final_syllable_heavy()

df = read_data("data2.pkl")
append_representation_to_dataframe(df)
print(df)



comparison, unequal_lengths = compare_realization_model(df.model, df.realization)
print(len(comparison) - np.sum(comparison))
print(len(unequal_lengths))

#print(collect_nonmatches(df, comparison))
#for w,v in collect_nonmatches(df, comparison):
#    print(w, v, build_syllable_representation(w), build_syllable_representation(v))

#statistics(df, comparison, save = True)
#write_nonmatches_to_csv('datacsvnewnew.csv', df, comparison)

def iambic_bysyl_investigation():
    iamb_bisyl = filter_iambic_bisyllabic_words(df)
    add_heavy_fin_syl_column(iamb_bisyl)
    print(iamb_bisyl)
    print(np.sum(iamb_bisyl.heavy_final_syl))
    print(iamb_bisyl[ [not b for b in iamb_bisyl.heavy_final_syl] ])

#write_df_to_csv('iamb_bisyl.csv', filter_iambic_bisyllabic_words(df))

def word_type_investigation():
    words = collect_different_words(df)
    words_reprs = make_df_words_repr(words)
    calculate_nr_word_types(words_reprs)
    print(words_reprs)

def build_wordlist_for_child(name, df):
    df_child = df[df['Name'] == name]
    print(df_child)
    prev_time = 'P1Y10M28DT0H0M0S'
    child_dev = ChildDevelopment(name)
    wordlist = WordList('P1Y10M28DT0H0M0S')
    for index, data_point in df_child.iterrows(): # Might be slow, see https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
        print(data_point)
        time = data_point['Age']
        if prev_time != time: # klopt geen drol van, off by one error
            child_dev.add_wordlist(wordlist)
            wordlist = WordList(time)
        
        word = Word(data_point['word'], data_point['model'], data_point['realization'], data_point['rep_model'], data_point['rep_realization'])
        
        
        prev_time = time
    return(child_dev)

def trisyl_investigation(df):
    # main function to collect trisyllabic words
    df_trisyl = filter_trisyllabic_words(df)
    write_df_to_csv('trisyl.csv', df_trisyl)
    df_trisyl_unique = df_trisyl.drop_duplicates(subset = ["word"])
    write_df_to_csv('trisyl_unique.csv', df_trisyl_unique)

#word_type_investigation()
leon = build_wordlist_for_child('Leon', df)
print(leon.wordlists[0])

#word_type_investigation()
