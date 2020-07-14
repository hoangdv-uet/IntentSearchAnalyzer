from collections import defaultdict
import re

from flair.models import SequenceTagger
from flair.data import Sentence

def load_model(modelpath):
    return SequenceTagger.load(modelpath)

def get_tag_dic(sentence):
    res = defaultdict(list)
    for entity in sentence.get_spans('ner'):
        en_dict = entity.to_dict()
        res[en_dict['type']].append(en_dict['text'])
    return res 

def get_tag_sentence(model,query):
    sentence = Sentence(query)
    model.predict(sentence)
    return sentence

def get_entity_by_tag(query, models, tag='TARGET'):
    # tag_display = [['iphone 6 16gb', '<target>'], ['gold', '<color>'], ['xách', ''], ['tay', ''], ['singapore', '<origin>'], ['mới', '<status>'], ['100', ''], ['giá rẻ nhất', '<price>'], ['tp hồ chí minh', '<loc>'], ['giá bán 3 triệu 3', '<price>']]
    # non_tag_display = [['iphone', ''], ['6', ''], ['16gb', ''], ['gold', '<color>'], ['xách', ''], ['tay', ''], ['singapore', '<origin>'], ['mới', '<status>'], ['100', ''], ['giá rẻ nhất', '<price>'], ['tp hồ chí minh', '<loc>'], ['giá bán 3 triệu 3', '<price>']]

    
    # tag_dic = {}
    # tag_dic['target'] = ''
    tag_sentence = get_tag_sentence(models["target_model"], query)
    non_tag_sentence = get_tag_sentence(models["non_target_model"], query)
    
    tag_display = to_display(tag_sentence)
    non_tag_display = to_display(non_tag_sentence)

    tag_display, non_tag_display = combine(tag_display, non_tag_display)
    # print(tag_display)
    # print(non_tag_display)

    tag_dic = get_tag_dic(tag_sentence)
    # print(tag_dic)

    return {"tag_display": tag_display, "non_tag_display": non_tag_display}, tag_dic

def to_display(sentence):
    dct = []
    i = 0
    cur_tag = ''
    phrase = []
    tokens = sentence.to_tagged_string().split()
    # tokens = sentence.split()
    while i < len(tokens)-1:
        if '<' in tokens[i+1]:
            label = tokens[i+1][3:-1].lower()
            if cur_tag == '':
                cur_tag = label
                phrase += [tokens[i]]
            elif cur_tag == label:
                phrase += [tokens[i]]
            elif cur_tag != tokens[i+1]:
                dct.append([' '.join(phrase), '<' + cur_tag + '>'])
                cur_tag = label
                phrase = [tokens[i]]
            i += 1
        else:
            if cur_tag != '':
                dct.append([' '.join(phrase), '<' + cur_tag + '>'])
                phrase = []
                cur_tag = ''
            dct.append([tokens[i], ''])
        i += 1

    if cur_tag != '':
        dct.append([' '.join(phrase), '<' + cur_tag + '>'])

    if i == len(tokens)-1 and '<' not in tokens[i]:
        dct.append([tokens[i], ''])

    return dct

def combine(tag, non_tag):
    new_non_tag = [nt for nt in non_tag if nt[1]!='']
    return tag, new_non_tag


if __name__ == '__main__':
    text = 'iphone 6 16gb gold <B-COLOR> xách tay singapore <B-ORIGIN> mới <B-STATUS> 100 giá <B-PRICE> rẻ <I-PRICE> nhất <I-PRICE> tp <B-LOC> hồ <I-LOC> chí <I-LOC> minh <I-LOC> giá <B-PRICE> bán <I-PRICE> 3 <I-PRICE> triệu <I-PRICE> 3 <I-PRICE>'
    print(to_display(text))