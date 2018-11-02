import numpy as np
import sys
import random

from collections import defaultdict, Counter
from nltk.tokenize import TweetTokenizer

def make_pairs(corpus):
    for i in range(len(corpus)-1):
        yield (corpus[i], corpus[i+1])
        

def make_dict(pairs):
    word_dict = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]
    return word_dict


def make_stuff(word_dict, corpus, n_words=20):
    first_word = np.random.choice(corpus)
    while first_word.islower():
        first_word = np.random.choice(corpus)

    chain = [first_word]

    for i in range(n_words):
        chain.append(np.random.choice(word_dict[chain[-1]]))

    return ' '.join(chain)

def filter_words(words):
    words2 = [word.lower() for word in words if word.isalpha()]
    return words2

def filter_words2(words):
    stop_words = [u'\"']
    words2 = [word for word in words if (word.lower() not in stop_words)]
    return words2

def tokenize(lines, filterlen=5):
    tokenizer = TweetTokenizer()
    tokenized_lines = []
    for line in lines:
        line = tokenizer.tokenize(line)
        line = filter_words2(line)
        if len(line) > filterlen:
            tokenized_lines.append(line)
    print(len(tokenized_lines))
    return tokenized_lines

def clean_input():
    textfile = open('cleaned.txt','r')
    lines = textfile.read().split('},')
    extracted_lines = []
    for count, line in enumerate(lines):
        split_line = line.split(':')
        if len(split_line)>4:
            split_line = " ".join(split_line[4:])
            if "\"url\"" not in split_line:
                extracted_lines.append(split_line)  
    return extracted_lines

def clean_whatsapp(filename):
    textfile = open(filename,'r')
    lines = textfile.readlines()
    extracted_lines = []
    for count, line in enumerate(lines):
        split_line = line.split('-')
        if len(split_line)>1:
            split_line = " ".join(split_line[1:])
            split_line = split_line.split(':')
            split_line = " ".join(split_line[1:])
            if "omitted>" not in split_line:
                extracted_lines.append(split_line)  
    return extracted_lines

def main():
    if not len(sys.argv)==5:
        print("Incorrect amount of arguments, required: 4")
        sys.exit(-1)
    filename = sys.argv[1]
    n_words = int(sys.argv[2])
    n_lines = int(sys.argv[3])
    filterlen = int(sys.argv[4])

    # lines = clean_input()
    lines = clean_whatsapp(filename)
    tokenized_lines = tokenize(lines, filterlen)
    tokenized_lines = np.asarray(tokenized_lines)
    tokenized_lines = np.concatenate(tokenized_lines)

    # trump = open('speeches.txt', encoding='utf8').read()
    # corpus = trump.split()
    # tokenized_lines = np.concatenate([tokenized_lines,corpus])

    pairs = make_pairs(tokenized_lines)
    word_dict = make_dict(pairs)
    for i in range(0,n_lines):
        print(make_stuff(word_dict, tokenized_lines, n_words))
        print("-----------------")

    # pairs = make_pairs(corpus)
    # word_dict = make_dict(pairs)
    # for i in range(0,n_lines):
    #     print(make_stuff(word_dict, corpus, n_words))

if __name__ == "__main__":
    main()