import falcon
from .sentence import Sentence_Resource
from .word_lookup import Word_Lookup_Resource


api = application = falcon.API()

sentence = Sentence_Resource()
word_lookup = Word_Lookup_Resource()
api.add_route('/sentence', sentence)
api.add_route('/word_lookup', word_lookup)
