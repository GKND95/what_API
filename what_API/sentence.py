import falcon
from google.cloud import translate_v2 as translate


class Resource(object):

    def on_post(self, req, resp):

        text = "Successful Test!"
        target = 'fr'
        model = 'nmt'

        result = translate_client.translate(text, target_language=target, model=model)

        resp.body = result['translatedText']
        resp.status = falcon.HTTP_200

translate_client = translate.Client()
