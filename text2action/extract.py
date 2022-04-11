from stanfordcorenlp import StanfordCoreNLP


class WordTag:
    word = ''  # 单词本身
    tag = ''  # 单词标签

    def __init__(self, w, t):
        self.word = w
        self.tag = t


class Noun:
    word = ''
    cnt = 1
    idx = -1  # 在word_tags中的索引值
    length = 1  # 占用多少个单词

    def __init__(self, w):
        self.word = w

    def __str__(self):
        return 'name: %s, count: %s, start: %s' \
               % (self.word, self.cnt, self.idx)


class Prep:
    word = ''
    phrase = False
    idx = -1
    length = 1

    def __init__(self, w, p):
        # w 要么是字符串，要么是字符串数组
        self.phrase = p
        if self.phrase:
            n = len(w)
            for i in range(0, n):
                self.word = self.word + w[i]
                if i != n - 1:
                    self.word = self.word + ' '
            self.length = len(w)
        else:
            self.word = w[0]

    def __str__(self):
        description = 'preposition'
        if self.phrase:
            description = 'prep-phrase'
        return '%s: %s, start: %s' % (description, self.word, self.idx)


# 检查名词是不是合法的：如果一个名词是介词短语的一部分就是不合法的
def check_valid_noun(noun, word_tags, len):
    before = True
    for i in range(noun.idx - 1, -1, -1):
        if word_tags[i].tag == 'IN':
            before = False
            break

    behind = True
    for i in range(noun.idx + noun.length, len):
        if word_tags[i].tag == 'IN':
            behind = False
            break

    return before or behind


def extract_noun(word_tags, len):
    result = []
    for i in range(0, len):
        if word_tags[i].tag == 'NNS' or word_tags[i].tag == 'NN':
            noun = Noun(word_tags[i].word)
            if word_tags[i].tag == 'NNS':
                if i != 0 and (word_tags[i - 1].tag == 'CD' or word_tags[i - 1].tag == 'DT'):
                    noun.cnt = word_tags[i - 1].word  # 可能是数量描述信息
                    noun.idx = i - 1

            else:
                if i == 0 or (word_tags[i - 1].tag != 'DT' and word_tags[i - 1].tag != 'JJ'):
                    continue  # 如果是单数形式而前面还没有冠词限定或形容词就认为不是实体
                if i != 0:
                    noun.cnt = word_tags[i - 1].word
                    noun.idx = i - 1

            if noun.idx == -1:
                noun.idx = i
            noun.length = (i - noun.idx + 1)
            if check_valid_noun(noun, word_tags, len):
                result.append(noun)

    return result


def extract_prep(word_tags, length):
    first_in = -1
    last_in = -1
    for i in range(0, length):
        if word_tags[i].tag == 'IN':
            if first_in != -1:
                last_in = i
            else:
                first_in = i

            if last_in != -1 and first_in != -1:
                break

    if last_in == -1:
        last_in = first_in
    w = []
    for i in range(first_in, last_in + 1):
        w.append(word_tags[i].word)
    p = len(w) > 1

    result = Prep(w, p)
    result.idx = first_in
    result.length = last_in - first_in + 1

    return result


def parse_sent(sentence):

    # nlp = StanfordCoreNLP(r'E:\nju\hci\stanford-corenlp-4.4.0')
    nlp = StanfordCoreNLP('/home/songdj/hci/data/stanford-corenlp-4.4.0')
    # nlp = StanfordCoreNLP('/Users/sdj/Documents/course/S2/人机交互/project/data/stanford-corenlp-4.4.0')
    # 这里改成你stanford-corenlp所在的目录

    # word_tags = nlp.pos_tag(sentence)
    # print('Part of Speech:', word_tags)

    # pos tagging
    word_tags = nlp.pos_tag(sentence)
    print('Part of Speech:', word_tags)

    # 将word_tags处理成 WordTag数组
    arr = []
    for wt in word_tags:
        word_tag = WordTag(wt[0], wt[1])
        arr.append(word_tag)
    length = len(arr)

    # 提取名词
    noun_words = extract_noun(arr, length)
    for i in noun_words:
        print(str(i))

    # 提取介词
    prep_word = extract_prep(arr, length)
    print(str(prep_word))


    nlp.close()  # Do not forget to close! The backend server will consume a lot memery.


if __name__ == '__main__':

    # sentence = 'There is a table on the left of another table.'

    sentences = [
        'There is a bird flying above the sea.',
        'There is a radio on the table.',
        'I see a boat on the river.',
        'There is a big diamond in the sky.',
        'There are two trees in the field.'
    ]

    for sentence in sentences:
        parse_sent(sentence)
