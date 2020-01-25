import falcon
import json
from random import randint
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

        # randomly select which sentences to translate, and remove any repeats
        sent_num = len(reduced_sent_tokenized)
        trans_num = sent_num//10
        chosen_sent = []
        for num in range(trans_num):
            chosen_sent.append(reduced_sent_tokenized[randint(0, sent_num-1)])
        chosen_sent = list(set(chosen_sent))

        # translate selected sentence, and place in list of word pairs (also list)
        result = []
        for sentence in chosen_sent:
            text = sentence
            target = 'fr'
            model = 'nmt'
            trans_result = translate_client.translate(text, target_language=target, model=model)
            inner_array = [text, trans_result['translatedText']]
            result.append(inner_array)

        # send back json object containing resultant list of lists
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

translate_client = translate.Client()
