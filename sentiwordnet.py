# coding=utf-8
import csv
import time

class SentiWordnet:
    """Sentimentwordnet bindind class

    This class provides a binding to lookup sentiment meassure for
    English and Spanish words
    """

    def insert_swdict(self, word, row, sw_dict):
        """Insert a word like a key into a dict and save data like value
            :param word: insert word param into the sw_dict param like value
            :param pos: part of speech
            :param sw_dict: dictionary
            :param data: insert data param into the sw_dict param like value
        """
        # Insert the new word and pos into the dict+
        pos = row["pos"]
        if word not in sw_dict:
            sw_dict[word] = {}
            sw_dict[word][pos] = row.copy()
        elif pos not in sw_dict[word]:
            sw_dict[word][pos] = row.copy()


    def __init__(self):
        """Initialite datastructures
        """
        # Load a preprocesed file of linked and sorted multilingual words
        f_in = open("data/sentiwordnet.tsv", "r")
        tsv_reader = csv.reader(f_in, delimiter='\t')

        # Read headers
        headers = tsv_reader.next()

        # DS to store each language information
        self.sw_sp = {}
        self.sw_en = {}

        # Iterate for each line
        for csv_row in tsv_reader:

            # Merge headers and row into a dict
            row = dict(zip(headers, csv_row))

            # Insert data to each language
            flat_row = row.copy()
            del flat_row["word_en"]
            del flat_row["word_sp"]

            self.insert_swdict(row["word_en"], flat_row, self.sw_en)
            self.insert_swdict(row["word_sp"], flat_row, self.sw_sp)

        # Save all data
        self.sentiwordnet = {"english": self.sw_en, "spanish": self.sw_sp}


    def get_sentiment(self, word, pos, language):
        """Return the sentiment of a given word, part of speech and language
            :param word: word to analize the sentiment
            :param pos: part of speech (n:Noun, a:Adjetive, v:Verb, r=Adverb)
            :param language: language
        """
        # Assert input params
        assert(language in ["english", "spanish"])
        # Check if word and pos exists into the dict
        if word in self.sentiwordnet[language]:
            if pos in self.sentiwordnet[language][word]:
                return self.sentiwordnet[language][word][pos]
            else:
                return None
        else:
            return None


"""
if __name__ == "__main__":

    # Init class
    time_start = time.time()
    sentiwordnet = SentiWordnet()
    print("Loaded time: %s\n" % (time.time() - time_start))

    # Some lookups
    words = [("unfortunately","r","en"), ("desafortunadamente", "r", "sp"),
                ("exuberant","a","en"), ("stressful","a","en")]
    for word,pos,language in words:
        time_start = time.time()
        a = sentiwordnet.get_sentiment(word, pos, language)
        print("%s %s" % (word, a))
        print("Lookup time: %s \n" % (time.time() - time_start))
"""
