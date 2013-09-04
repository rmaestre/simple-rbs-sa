# coding=utf-8
import pymongo

__author__ = 'epeinado'


class SentiwordnetToTreetagger:
    """
        Sentiment from SentiWordNet to Treetagger POS tagging.
    """

    def __init__(self):
        self.en_mapping = {"adj": "a",
                           "adv": "r",
                           "noun": "n",
                           "verb": "v"}

        config = {}
        config['db'] = {}
        config['db']['host'] = "web40"
        config['db']['port'] = 27017
        config['db']['db'] = "wordnet"

        # Get Mongo collection
        connection = pymongo.Connection(config['db']['host'], config['db']['port'])
        db = connection[config['db']['db']]
        self.sentiment_collection = db["sentiment"]


    def get_sentiment(self, word, pos, languaje):
        # Mapping Tretagger postagging  to MongoDB postagging
        if pos == "None":
            return None
        else:
            postag = self.en_mapping[pos]
            suffix = ''
            # Determinamos si la palabra a recuperar será española o inglesa
            if languaje == 'english':
                suffix = "_en"
            elif languaje == 'spanish':
                suffix = "_es"
            # Realizamos la consulta para obtener todas los synsets con la palabra y el tipo indicados
            document = self.sentiment_collection.find(
                {"$and": [
                    {"$and": [{"word" + suffix: word}, {"type": postag}]},
                    {"$or" : [
                    {"$and" : [{"negative" : "0"}, {"positive" : {"$gt" : "0"}}]},
                    {"$and" : [{"negative" : {"$gt" : "0"}}, {"positive" : "0"}]}
                    ]}
                ]}
            )
            count = document.count()
            result = {}
            if count == 0:
                # La palabra no pertenece a WordNet
                return None
            elif count > 1:
                # Ordenamos la lista por valor ascendente del índice (más prioritario primero)
                docs = []
                for doc in document:
                    docs.append(doc)
                docs.sort(key=lambda x: (x['index']))
                result["positive"] = docs[0]["positive"]
                result["negative"] = docs[0]["negative"]
            else:
                # Cogemos los valores de las polaridades de sentimiento del único resultado
                result["positive"] = document[0]["positive"]
                result["negative"] = document[0]["negative"]
            return result

