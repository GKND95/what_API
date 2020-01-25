import falcon
from .sentence import Resource


api = application = falcon.API()

sentence = Resource()
api.add_route('/sentence', sentence)
