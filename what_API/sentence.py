import falcon
import json
from nltk.tokenize import sent_tokenize
from google.cloud import translate_v2 as translate


class Resource(object):

    def on_post(self, req, resp):

        # read input json to large string
        json_data = json.loads(req.stream.read())
        main_text = json_data["text"]

        # tokenize by sentence - outputs list of sentence strings
        sent_tokenized = sent_tokenize(main_text)

        # remove list elements with fewer than 15 characters
        reduced_sent_tokenized = [i for i in sent_tokenized if len(i) > 15]

        # Google translate stuff
        text = "Successful Test!"
        target = 'fr'
        model = 'nmt'

        #result = translate_client.translate(text, target_language=target, model=model)

        #resp.body = result['translatedText']
        resp.status = falcon.HTTP_200

translate_client = translate.Client()
