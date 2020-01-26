import falcon
import json
import pickle
import nltk
from random import randint
from nltk.tokenize import word_tokenize
from google.cloud import translate_v2 as translate


class Word_Resource(object):

    def on_post(self, req, resp):

        # import pickled word database, format is: [(string, POS, dunno), ...]
        word_db = pickle.load(open("what_API/lemmatized_word_data_pickle.p","rb"))
        
        # split word database into nouns, verbs, adjectives, and adverbs
        word_db_noun = []
        word_db_verb = []
        word_db_adverb = []
        word_db_adjective = []
        for tup in word_db:
            if tup[1][0] == 'N':
                word_db_noun.append(tup)
            if tup[1][0] == 'V':
                word_db_verb.append(tup)
            if tup[1][0] == 'R':
                word_db_adverb.append(tup)
            if tup[1][0] == 'J':
                word_db_adjective.append(tup)

        # read input json for text and user settings
        json_data = json.loads(req.stream.read())
        main_text = json_data["text"]
        u_freq = json_data["freq"]
        u_dif = json_data["dif"]
        u_noun = json_data["noun"]
        u_verb = json_data["verb"]
        u_adverb = json_data["adverb"]
        u_adjective = json_data["adjective"]

        # tokenize by word - outputs list of word strings
        word_tokenized = word_tokenize(main_text)

        # extract words that match user selected POS
        pos_filtered_words = []
        for word in word_tokenized:
            temp_word = [word]
            word_tup = nltk.pos_tag(temp_word)
            if (u_noun == True and word_tup[0][1][0] == 'N'):
                pos_filtered_words.append(word)
            if (u_verb == True and word_tup[0][1][0] == 'V'):
                pos_filtered_words.append(word)
            if (u_adverb == True and word_tup[0][1][0] == 'R'):
                pos_filtered_words.append(word)
            if (u_adjective == True and word_tup[0][1][0] == 'J'):
                pos_filtered_words.append(word)

        # determine number of words to be translated
        num_words = len(pos_filtered_words)
        num_trans_words = int(u_freq*float(num_words))



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
            source = 'en'
            target = 'fr'
            model = 'nmt'
            trans_result = translate_client.translate(text, source_language=source, target_language=target, model=model)
            inner_array = [text, trans_result['translatedText']]
            result.append(inner_array)

        # send back json object containing resultant list of lists
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

translate_client = translate.Client()
