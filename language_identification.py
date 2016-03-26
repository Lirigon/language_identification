# coding: utf-8

##############################
#                            #
#  Language Identification   #
#                            #
#                            #
#       Danny Belitz         #
#                            #
##############################

"""This program identifies the language of a given text.
It trains on EuroParl / uses language models for the following languages:

Bulgarian, Czech, Danish, German, Greek, English, Spanish, Finnish, French, Hungarian, Portuguese.

Each training set consists of 10000 sentences.
Initially, unigrams (single characters) were used to train the language models.
In future versions the code will be expanded to also train LMs based on 2-to-5-gram statistics."""

from operator import itemgetter
import os
import sys
import glob
import cPickle as pickle

class LanguageModel(object):
    """A language model for a given language, which is trained on its respective part of EuroParl.

    A language model has the following attributes:

        language: A string representing the language.
        file_path: A string representing the path to the training file.

        model_exists: A boolean value to represent whether a LM model was already trained.
        ranked_unigram_dictionary: A dictionary with ranked unigram counts.

        TODO:
        ranked_bigram_dictionary: A dictionary with ranked bigram counts.
        ranked_trigram_dictionary: A dictionary with ranked trigram counts.
        ranked_4gram_dictionary: A dictionary with ranked 4-gram counts.
        ranked_5gram_dictionary: A dictionary with ranked 5-gram counts.
    """

    def __init__(self, language, file_path):
        """Return a LM object whose language is *language* and which is located at *file_path*."""
        self.language = language
        self.file_path = file_path
        self.ranked_unigram_dictionary = dict()

        self.model_exists = False

        ## call functions to do the work
        # check whether models exist
        self.output_name = self.language + '.pkl'
        if os.path.isfile('models/'+self.output_name) and not self.model_exists:
            self.load_model()
        else:
            processed_text = self.preprocess_text()
            self.unigram_statistics(processed_text)

    def preprocess_text(self):
        """Reads the text file to train the LM and splits it."""
        # print "Training model for "+ self.language +'...'
        # open text file
        with open(self.file_path) as text_file:
            read_file = text_file.read()

        # split text
        read_file = read_file.split()
        return read_file

    def unigram_statistics(self, read_file):
        """Creates a ranked unigram dictionary."""
        char_int_dict = dict() # character -> integer

        # Counts n-grams in the text and puts them into a dictionary
        for word in read_file:
            for character in word:
                if character in char_int_dict:
                    char_int_dict[character] += 1
                else:
                    char_int_dict[character] = 1

        # initialise rank counter with a default value of 1
        rank_counter = 1

        # Sort the dictionary in decreasing order (frequency, high to low)
        for item in sorted(char_int_dict.items(), key=itemgetter(1), reverse=True):
            # Add every item to the ranked dictionary.
            # Highest frequency -> lowest rank.
            char_liste = list(item)
            self.ranked_unigram_dictionary[char_liste[0]] = rank_counter
            rank_counter += 1
        if self.language != "Input": # we don't want to "save" the model for the input file
            # save model to pickle file
            output = open('models/'+self.output_name, 'w')
            pickle.dump(self.ranked_unigram_dictionary, output)
            output.close()
            # set to true, because we built and saved the model
            self.model_exists = True

    def load_model(self):
        """Loads model if it exists."""
        # print "Loading "+ self.output_name
        output_file = open('models/'+self.output_name)
        self.ranked_unigram_dictionary = pickle.load(output_file)

##### TRAINING ######
# corpus files for training
# get paths to all using glob
PATH_LIST = glob.glob("corpus/*.txt")

LANGUAGE_LIST = list()
LM_LIST = list()

# for every file do:
for file_name in PATH_LIST:
    # remove last 4 characters ".txt"
    language_string = file_name[:-4]
    # remove first 7 characters "corpus/"
    language_string = language_string[7:]
    # capitalise first letter
    language_string = language_string.title()
    # save languages names
    LANGUAGE_LIST.append(language_string)

    # create LM
    languageModel = LanguageModel(language_string, file_name)

    # append language models
    LM_LIST.append(languageModel)

# get input text file from command line
# create 'language model' for input document
INPUT_TEXT = LanguageModel('Input', os.path.relpath(sys.argv[1]))

##### COMPARING #####
PROFILE_DICT = dict() # dictionary for all language profiles
PROFILE_LIST = list() # list for every language profile value

# Compares profile of the text with the profile of language
def compare_lms(language_model):
    """Return a LM object whose language is *language* and which is located at *file_path*."""
    summed = 0
    for entry in INPUT_TEXT.ranked_unigram_dictionary:
        if entry in language_model.ranked_unigram_dictionary:
            # we use abs() to not compute with negative values.
            summed += abs(INPUT_TEXT.ranked_unigram_dictionary[entry] - \
            language_model.ranked_unigram_dictionary[entry])
        else: #if not in dict: gets max rank of profile +1
            summed += len(INPUT_TEXT.ranked_unigram_dictionary)+1

    PROFILE_LIST.append(summed)
    PROFILE_DICT[summed] = language_model.language.title()

for lm in LM_LIST:
    compare_lms(lm)

######## Finding and outputting correct language and the ranking ########
# find the correct language: min over all results
MINIMUM = min(PROFILE_LIST)
# print the language of the document on the screen
print "\nThe input document is written in {0}.".format(PROFILE_DICT[MINIMUM])
# print ranking of competing languages
print "\nRanking is as follows:"
for profile_dict_item in sorted(PROFILE_DICT.items(), key=itemgetter(0), reverse=False):
    print profile_dict_item
