import pandas as pd
import numpy as np

ipa_vowels = ['a', 'ɑ', 'œ', 'y', 'o', 'ɑ̈', 'i', 'u', 'ɪ', 'ə', 'ɛ', 'e', 'ɔ', 'ʌ', 'ø̈', 'ɛ̝','ʉ', 'œ̞', 'œ']

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


def build_syllable_representation_old(word):
    """
    """
    currently_reading_cons = True
    representation = []
    
    #Edge case where the word starts with a vowel, but no stress
    if word[0] in ipa_vowels:
        representation.append(False)
    
    for cha in word:
        if cha == "ˈ" and not currently_reading_cons:
            representation.append(True)
            currently_reading_cons = True
        elif cha == "ˈ" and currently_reading_cons: #when we just read a cons, we appended a false, which needs to be switched to a True
            if len(representation) > 0:
                representation[-1] = True
            else:
                representation.append(True)
        elif cha in ipa_vowels:
            currently_reading_cons = False
        elif cha not in ipa_vowels and not currently_reading_cons:
            representation.append(False)
            currently_reading_cons = True
    if word[-1] not in ipa_vowels and len(representation) >0: #In this case, it counts the coda of the final syllable as a new syllable, which it should not
        representation.pop()
    #print(word, representation)
    return representation
    
    
def build_syllable_representation(word):
    """
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



df = read_data("data.pkl")
print(df)

for word in df.model.head():
    build_syllable_representation(word)
    #print("".join(c for c in word if c.lower() not in ipa_vowels))

build_syllable_representation("anˈkledən")
build_syllable_representation("ankleˈdən")
print(list(map(build_syllable_representation,df.actual)))
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
for w,v in collect_nonmatches(df, comparison):
    print(w, v, build_syllable_representation(w), build_syllable_representation(v))
