import pandas as pd
import numpy as np
import csv
import unittest






ipa_vowels = ['a', 'ɑ', 'œ', 'y', 'o', 'ɑ̈', 'i', 'u', 'ɪ', 'ə', 'ɛ', 'e', 'ɔ', 'ʌ', 'ø̈', 'ɛ̝','ʉ', 'œ̞', 'œ', 'ɛ̞', 'ʔ', 'ɒ','ø', 'æ̝', 'ə̆', 'o͡', 'o̝', '͡'] 
agnostic_symbols = ['͡']

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

def write_data_to_csv(filename, df, comparison, header = ['Name', 'Age', 'word', 'model','realization','stressmodel','stressrealization'], apply_filter=True):
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
        else:
            vowels = False
    return representation

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
            
            
            self.assertEqual([True, False, False], build_syllable_representation('ˈʔaːˌkleːdə'))
            
            self.assertEqual([True, False, False], build_syllable_representation('ˈpinoːŭ'))
            self.assertEqual([True, False, False], build_syllable_representation('ˈzeˌot͡jɑ̈s'))



    
        

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

def filter_iambic_bisyllabic_words(df):
    filter_bisyl = [True if l==2 else False for l in df.rep_model.apply(len) ]#df.rep_model.apply(len) #and df.rep_model[1]
    #print(filter_iamb)
    filtered = df[filter_bisyl]
    filter_iamb = [r[1] for r in filtered.rep_model]
    return filtered[filter_iamb] #Second thing returns booleans, we are interested when these are True

def get_odd_syllables():
    return

test = MyTest()
test.test_build_syllable_representation()

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
#write_data_to_csv('datacsvnew.csv', df, comparison)


#print(filter_iambic_bisyllabic_words(df))
#print(append_representation_to_dataframe(df))
