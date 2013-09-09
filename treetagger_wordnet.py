# -*- coding: utf-8 -*-

class TreetaggerToWordnet():
    """
        Treetagger POS tags to wordnet morphological category mapper.
    """

    def __init__(self):
        self.es_mapping = {"ADJ": "a",
                           "ADV": "a",
                           "NC": "n",
                           "NMEA": "n",
                           "NP": "n",
                           "VCLIger": "v",
                           "VCLIinf": "v",
                           "VCLIfin": "v",
                           "VEadj": "v",
                           "VEfin": "v",
                           "VEger": "v",
                           "VEinf": "v",
                           "VHadj": "v",
                           "VHfin": "v",
                           "VHger": "v",
                           "VHinf": "v",
                           "VLadj": "v",
                           "VLfin": "v",
                           "VLger": "v",
                           "VLinf": "v",
                           "VMadj": "v",
                           "VMfin": "v",
                           "VMger": "v",
                           "VMinf": "v",
                           "VSadj": "v",
                           "VSfi": "v",
                           "VSge": "v",
                           "VSinf": "v"}
        self.en_mapping = {"JJ": "a",
                           "JJR": "a",
                           "JJS": "a",
                           "RB": "r",
                           "RBR": "r",
                           "RBS": "r",
                           "NN": "n",
                           "NNS": "n",
                           "NNP": "n",
                           "NNPS": "n",
                           "VB": "v",
                           "VBD": "v",
                           "VBG": "v",
                           "VBN": "v",
                           "VBP": "v",
                           "VBZ": "v"}
        self.pt_mapping = {"ADJ": "a",
                           "ADV": "r",
                           "N": "n",
                           "V": "v"}
        self.ca_mapping = {}
        self.mapping = {
            "spanish": self.es_mapping,
            "english": self.en_mapping,
            "pt": self.pt_mapping,
            "ca": self.ca_mapping
        }

    def wordnet_morph_category(self, lang, postag):
        """
            Returns the wordnet morphological category corresponding to the 
            POS tag of the given language.
        """
        return self.mapping[lang].get(postag, None)

