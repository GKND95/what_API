import falcon
import json
import nltk
from google.cloud import translate_v2 as translate


class Resource(object):

    def on_post(self, req, resp):

        json_data = json.loads(req.stream.read())
        main_text = json_data["text"]
        print(main_text)

        sent_tokenized = nltk.sent_tokenize(main_text)
        print(sent_tokenized)

        text = "Successful Test!"
        target = 'fr'
        model = 'nmt'

        #result = translate_client.translate(text, target_language=target, model=model)

        #resp.body = result['translatedText']
        resp.status = falcon.HTTP_200

translate_client = translate.Client()
