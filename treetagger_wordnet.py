# -*- coding: utf-8 -*-

class TreetaggerToWordnet():
    """
        Treetagger POS tags to wordnet morphological category mapper.
    """

    def __init__(self):
        self.es_mapping = {"ADJ": "adj",
                           "ADV": "adv",
                           "NC": "noun",
                           "NMEA": "noun",
                           "NP": "noun",
                           "VCLIger": "verb",
                           "VCLIinf": "verb",
                           "VCLIfin": "verb",
                           "VEadj": "verb",
                           "VEfin": "verb",
                           "VEger": "verb",
                           "VEinf": "verb",
                           "VHadj": "verb",
                           "VHfin": "verb",
                           "VHger": "verb",
                           "VHinf": "verb",
                           "VLadj": "verb",
                           "VLfin": "verb",
                           "VLger": "verb",
                           "VLinf": "verb",
                           "VMadj": "verb",
                           "VMfin": "verb",
                           "VMger": "verb",
                           "VMinf": "verb",
                           "VSadj": "verb",
                           "VSfi": "verb",
                           "VSge": "verb",
                           "VSinf": "verb"}
        self.en_mapping = {"JJ": "adj",
                           "JJR": "adj",
                           "JJS": "adj",
                           "RB": "adv",
                           "RBR": "adv",
                           "RBS": "adv",
                           "NN": "noun",
                           "NNS": "noun",
                           "NNP": "noun",
                           "NNPS": "noun",
                           "VB": "verb",
                           "VBD": "verb",
                           "VBG": "verb",
                           "VBN": "verb",
                           "VBP": "verb",
                           "VBZ": "verb"}
        self.pt_mapping = {"ADJ": "adj",
                           "ADV": "adv",
                           "N": "noun",
                           "V": "verb"}
        self.ca_mapping = {}
        self.mapping = {
            "es": self.es_mapping,
            "en": self.en_mapping,
            "pt": self.pt_mapping,
            "ca": self.ca_mapping
        }

    def wordnet_morph_category(self, lang, postag):
        """
            Returns the wordnet morphological category corresponding to the 
            POS tag of the given language.
        """
        return self.mapping[lang].get(postag, None)
