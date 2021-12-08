import pandas as pd
import numpy as np
import csv

ipa_vowels = ['a', 'ɑ', 'œ', 'y', 'o', 'ɑ̈', 'i', 'u', 'ɪ', 'ə', 'ɛ', 'e', 'ɔ', 'ʌ', 'ø̈', 'ɛ̝','ʉ', 'œ̞', 'œ', 'ɛ̞', 'ʔ']

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

def write_data_to_csv(filename, df, comparison):
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(['model','actual','stressmodel','stressactual'])

        # write the data
        for w,v in collect_nonmatches(df, comparison):
            writer.writerow([w, v, build_syllable_representation(w), build_syllable_representation(v)])

def write_stats_to_csv(filename, a,b,c,d,e):
    '''
    stats_mod, stats_act, stats_match, stats_nonmatch_mod, stats_nonmatch_act
    '''
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(['number','modellengthall','actuallengthall','lengthmatch', 'modellengthnonmatch', 'actuallengthnonmatch'])

        # write the data
        for i in range(10):
            writer.writerow([i, a[i], b[i], c[i], d[i], e[i]])

    
    
def build_syllable_representation(word):
    """
    word: the word of which you want the syllable representation
    
    Returns the representation of the syllable in the form of a list of booleans, where true represents stressed and false unstressed
    """
    representation = []
    stressed = False
    vowels = False
    for c in word:
        if c == "ˈ":
            stressed = True
        elif c in ipa_vowels:
            if not vowels:
                vowels = True
                representation.append(stressed)
                stressed = False
        else:
            vowels = False
    return representation

def compare_arrays(model, actual):
    assert(len(model) == len(actual))
    
    comparison = []
    
    for i in np.arange(len(model)):
        if len(model[i]) != len(actual[i]):
            print("not equal length", i, model, actual)
            continue
        for j in np.arange(len(model[i])):
            if model[i][j] != actual[i][j]:
                comparison.append(False)
                continue
        comparison.append(True)
    return comparison

def compare_actual_model(model, actual):
    assert(len(model) == len(actual))
    
    comparison = []
    unequal_lengths = []
    for i in np.arange(len(model)):
        mod_word = build_syllable_representation(model[i])
        act_word = build_syllable_representation(actual[i])
        if len(mod_word) != len(act_word):
            print("not equal length", i, mod_word, act_word)
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

def collect_nonmatches(df, comparison):
    cases = []
    for i, boolean in enumerate(comparison):
        if not boolean:
            cases.append((df.model[i], df.actual[i]))
    return cases

def statistics(df, comparison, save=False):
    stats_mod, stats_act, stats_match, stats_nonmatch_mod, stats_nonmatch_act = {}, {}, {}, {}, {}
    for i in np.arange(10):
        stats_mod[i] = 0
        stats_act[i] = 0
        stats_match[i] = 0
        stats_nonmatch_mod[i] = 0
        stats_nonmatch_act[i] = 0
    print(comparison)
    for i, boolean in enumerate(comparison):
        rep_mod = build_syllable_representation(df.model[i])
        rep_act = build_syllable_representation(df.actual[i])
        stats_mod[len(rep_mod)] += 1
        stats_act[len(rep_act)] += 1
        if boolean:
            stats_match[len(rep_mod)] += 1
        else:
            stats_nonmatch_mod[len(rep_mod)] += 1
            stats_nonmatch_act[len(rep_act)] += 1
    print(stats_mod, stats_act, stats_match, stats_nonmatch_mod, stats_nonmatch_act)
    if save:
        write_stats_to_csv('stats.csv', stats_mod, stats_act, stats_match, stats_nonmatch_mod, stats_nonmatch_act)


df = read_data("data.pkl")
#print(df)

#for word in df.model.head():
#    build_syllable_representation(word)
    #print("".join(c for c in word if c.lower() not in ipa_vowels))

#build_syllable_representation("anˈkledən")
#build_syllable_representation("ankleˈdən")
#print(list(map(build_syllable_representation,df.actual)))
#print(np.bitwise_xor(
#    np.asarray(list(map(build_syllable_representation,df.model))),
#    np.asarray(list(map(build_syllable_representation, df.actual)))
#    ))
#print(compare_arrays(list(map(build_syllable_representation,df.model)), list(map(build_syllable_representation,df.actual))))
#print(np.sum( )
comparison, unequal_lengths = compare_actual_model(df.model, df.actual)
print(len(comparison) - np.sum(comparison))
print(len(unequal_lengths))
#print(collect_nonmatches(df, comparison))
#for w,v in collect_nonmatches(df, comparison):
#    print(w, v, build_syllable_representation(w), build_syllable_representation(v))
statistics(df, comparison, save = True)
#write_data_to_csv('datacsv.csv', df, comparison)
