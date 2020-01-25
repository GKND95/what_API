import falcon
import json
from google.cloud import translate_v2 as translate


class Word_Lookup_Resource(object):

    def on_post(self, req, resp):

        # read input json into string
        json_data = json.loads(req.stream.read())
        main_text = json_data["text"]
        lang = json_data["lang"]

        # translate selected sentence, and place in list of word pairs (also list)
        if lang == 'en':
            text = main_text
            target = 'fr'
            model = 'nmt'
            trans_result = translate_client.translate(text, target_language=target, model=model)
            result = trans_result['translatedText']

        if lang == 'fr':
            text = main_text
            target = 'en'
            model = 'nmt'
            trans_result = translate_client.translate(text, target_language=target, model=model)
            result = trans_result['translatedText']

        # send back json object containing resultant list of lists
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

translate_client = translate.Client()
