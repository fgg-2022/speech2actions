import pickle

import hanlp

import requests
import random
import json
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from transformers import BertTokenizer, BertModel

# 视角平移
VIEW_SHIFT = [
    '向左转',
    '转到后面',
    '转向右边',
    '视角转到下面',
    '视角平移到上面',
]


def cos_sim(vector_a, vector_b):
    """
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a
    :param vector_b: 向量 b
    :return: sim
    """
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim


def translate(sent):
    API_KEY = 'HZAnl45C1imoFTwpXLrupO3Z'
    Secret_Key = 'ojsKK6BAp1sIDd1OoeFIBhdWCpYYDFMM'
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type' \
           f'=client_credentials&client_id={API_KEY}&client_secret={Secret_Key}'
    response = requests.get(host)
    if response:
        token = response.json()['access_token']
    else:
        raise AssertionError('no Baidu access token')
    url = 'https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=' + token

    term_ids = ''  # 术语库id，多个逗号隔开

    # Build request
    headers = {'Content-Type': 'application/json'}
    payload = {'q': sent, 'from': 'zh', 'to': 'en', 'termIds': term_ids}

    # Send request
    result = requests.post(url, params=payload, headers=headers).json()
    translation = result['result']['trans_result'][0]['dst']
    return translation


def embed(command, model):
    words_vec = []
    words = command.lower().split()
    for w in words:
        if w not in model.vocab:
            print(f'Cannot find word {w}')
        else:
            words_vec.append(model[w])
    word_vec = np.mean(np.array(words_vec), axis=0)
    return word_vec


def load_w2v(file_name):
    """ load w2v model
        input: model file name
        output: w2v model
    """
    w2v = KeyedVectors.load_word2vec_format(file_name, binary=False)
    return w2v


if __name__ == '__main__':
    # 下载语料库
    # HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)

    zh_sentences = [
        '向左转',    #
        '向左转三十度',    #
        '画一个球',
        '画一个正方体',
        '把球放到正方体上面',
    ]
    en_sentences = [translate(sent) for sent in zh_sentences]

    cls_desc = {
        'View angle shift': 'Moves the position of the camera in the current view',
        'View angle rotation': 'Rotate the camera itself for the current view',
        'Rotate the view around the selected object': 'Rotates the position of the camera with the selected Game '
                                                      'Object as the center and the up vector as the axis to '
                                                      'transform the current view , while keeping the camera view '
                                                      'towards the Game Object',
        'Object Panning': 'Moves the currently selected Game Object',
        'Object rotates around itself': 'Rotates the currently selected Game Object',
        'Object Scaling': 'Scales the currently selected Game Object',
        'Instantiate Object': 'Initialize a Object and places it in the center of the current view'
    }

    # GloVe Model
    print('============== Loading Model ==============')
    word2vec_path = 'embedding/60000_glove.840B.300d.txt'
    w2v = load_w2v(word2vec_path)

    labels = pickle.load(open('embedding/label_embedding.pkl', 'rb'))

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert = BertModel.from_pretrained('bert-base-uncased')



    print('============== Embedding ==============')

    encoder_inputs = tokenizer(en_sentences, padding=True, max_length=128, return_tensors='pt')
    src_ids = encoder_inputs['input_ids']
    embeddings = bert(src_ids).pooler_output.detach().numpy()

    cls_encoder_inputs = tokenizer(list(cls_desc.values()), padding=True, max_length=128, return_tensors='pt')
    cls_src_ids = cls_encoder_inputs['input_ids']
    cls_embeddings = bert(cls_src_ids).pooler_output.detach().numpy()
    np.concatenate
    print('============== Calculating ==============')

    for id, embedding in enumerate(embeddings):
        # HanLP(sentences).pretty_print()
        # HanLP(sentences, tasks='dep').pretty_print()    # 依存句法分析
        # HanLP(sentences, tasks='con').pretty_print()    # 成分句法分析
        # HanLP(sentences, tasks='sdp').pretty_print()    # 语义依存分析
        # doc = HanLP(sentences, tasks='srl')    # 语义角色标注

        # srl = hanlp.load('CPB3_SRL_ELECTRA_SMALL')

        # Zero-shot Spoken language understanding
        # embedding = embed(command, w2v)
        sim_scores = [cos_sim(embedding, v) for v in cls_embeddings]
        print(np.argmax(sim_scores))






