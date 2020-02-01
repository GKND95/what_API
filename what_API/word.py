import falcon
import json
import pickle
import nltk
from random import randint, shuffle
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from google.cloud import translate_v2 as translate


class Word_Resource(object):

    def on_post(self, req, resp):

        # import pickled word databases, format is: [(string, POS, dunno), ...]
        word_db_noun = pickle.load(open('what_API/word_db_noun_pickle.p', 'rb'))
        word_db_verb = pickle.load(open('what_API/word_db_verb_pickle.p', 'rb'))
        word_db_adverb = pickle.load(open('what_API/word_db_adverb_pickle.p', 'rb'))
        word_db_adjective = pickle.load(open('what_API/word_db_adjective_pickle.p', 'rb'))      

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

        # extract any words that match user selected POS
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

        # add ID's to POS filtered words
        i = 0
        pos_filtered_tupl = []
        for entry in pos_filtered_words:
            pos_filtered_tupl.append((entry, i))
            i += 1

        # cut POS specific word databases according to user selected difficulty
        easy = 0.999
        inter_hard = 0.85
        #word_db_noun_cut = []
        word_db_noun_cut_base = []
        #word_db_verb_cut = []
        word_db_verb_cut_base = []
        #word_db_adverb_cut = []
        word_db_adverb_cut_base = []
        #word_db_adjective_cut = []
        word_db_adjective_cut_base = []
        for tupl in word_db_noun:
            if u_dif == 'easy' and tupl[2] > easy:
                #word_db_noun_cut.append(tupl)
                word_db_noun_cut_base.append(tupl[0])
            if u_dif == 'intermediate' and (tupl[2] < easy and tupl[2] > inter_hard):
                #word_db_noun_cut.append(tupl)
                word_db_noun_cut_base.append(tupl[0])
            if u_dif == 'hard' and tupl[2] < inter_hard:
                #word_db_noun_cut.append(tupl)
                word_db_noun_cut_base.append(tupl[0])
        for tupl in word_db_verb:
            if u_dif == 'easy' and tupl[2] > easy:
                #word_db_verb_cut.append(tupl)
                word_db_verb_cut_base.append(tupl[0])
            if u_dif == 'intermediate' and (tupl[2] < easy and tupl[2] > inter_hard):
                #word_db_verb_cut.append(tupl)
                word_db_verb_cut_base.append(tupl[0])
            if u_dif == 'hard' and tupl[2] < inter_hard:
                #word_db_verb_cut.append(tupl)
                word_db_verb_cut_base.append(tupl[0])
        for tupl in word_db_adverb:
            if u_dif == 'easy' and tupl[2] > easy:
                #word_db_adverb_cut.append(tupl)
                word_db_adverb_cut_base.append(tupl[0])
            if u_dif == 'intermediate' and (tupl[2] < easy and tupl[2] > inter_hard):
                #word_db_adverb_cut.append(tupl)
                word_db_adverb_cut_base.append(tupl[0])
            if u_dif == 'hard' and tupl[2] < inter_hard:
                #word_db_adverb_cut.append(tupl)
                word_db_adverb_cut_base.append(tupl[0])
        for tupl in word_db_adjective:
            if u_dif == 'easy' and tupl[2] > easy:
                #word_db_adjective_cut.append(tupl)
                word_db_adjective_cut_base.append(tupl[0])
            if u_dif == 'intermediate' and (tupl[2] < easy and tupl[2] > inter_hard):
                #word_db_adjective_cut.append(tupl)
                word_db_adjective_cut_base.append(tupl[0])
            if u_dif == 'hard' and tupl[2] < inter_hard:
                #word_db_adjective_cut.append(tupl)
                word_db_adjective_cut_base.append(tupl[0])

        # compare POS filtered words to relevant word database. Temporarily lemmatize.
        selected_id = []
        for tupl in pos_filtered_tupl:          
            word_tag = (nltk.pos_tag([tupl[0]]))[0][1][0].lower()
            if word_tag != 'j' and word_tag != 'n' and word_tag != 'v' and word_tag != 'r':
                word_tag = 'n'
            if word_tag != 'j':
                lemmat_word = lemmatizer.lemmatize(tupl[0], word_tag)
            else:
                lemmat_word = tupl[0]            
            lemmat_word = lemmat_word.lower()
            if u_noun == True:
                if lemmat_word.lower() in word_db_noun_cut_base:
                    selected_id.append(tupl[1])
            if u_verb == True:
                if lemmat_word.lower() in word_db_verb_cut_base:
                    selected_id.append(tupl[1])
            if u_adverb == True:
                if lemmat_word.lower() in word_db_adverb_cut_base:
                    selected_id.append(tupl[1])
            if u_adjective == True:
                if lemmat_word.lower() in word_db_adjective_cut_base:
                    selected_id.append(tupl[1])
        
        # turn selected id into list of words to translate (remove after re-pickle)
        pent_output = []        
        for el in selected_id:
            out = pos_filtered_tupl[el][0].lower()
            pent_output.append(out) 

        print(pent_output)

        # remove words without direct to french translation (de-activate with translation removed word database list)
        #en_to_fr_trimmed = []
        #for el in selected_id:
        #    lower = pos_filtered_tupl[el][0].lower()  
        #    source = 'en'
        #    target = 'fr'
        #    model = 'nmt'
        #    translated = translate_client.translate(lower, source_language=source, target_language=target, model=model)  
        #    if lower != translated['translatedText'].lower():
        #        en_to_fr_trimmed.append(lower)       
        
        #print(en_to_fr_trimmed)    
            
        # determine number of words to be translated
        num_words = len(pent_output)
        num_trans_words = int(u_freq*float(num_words))

        # randomly sort list of words to translate, then take first num_trans_words for final translation
        shuffle(pent_output)
        final_output = pent_output[0:num_trans_words]


        # randomly select which sentences to translate, and remove any repeats
        #sent_num = len(reduced_sent_tokenized)
        #trans_num = sent_num//10
        #chosen_sent = []
        #for num in range(trans_num):
        #    chosen_sent.append(reduced_sent_tokenized[randint(0, sent_num-1)])
        #chosen_sent = list(set(chosen_sent))

        # translate selected sentence, and place in list of word pairs (also list)
        result = []       
        for sentence in final_output:
            text = sentence          
            source = 'en'
            target = 'fr'
            model = 'nmt'
            trans_result = translate_client.translate(text, source_language=source, target_language=target, model=model)
            result.append({'originalText': text, 'translatedText': trans_result['translatedText']})

        # send back json object containing resultant list of lists
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

translate_client = translate.Client()
lemmatizer = WordNetLemmatizer()
