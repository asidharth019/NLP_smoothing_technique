import numpy as np


# Corpus Data

def findcount(context, word, filename):
    # This function finds the total count of the word given the previous context
    count = 0
    with open(filename, 'r') as corpus:
        lines = corpus.readlines()
        for line in lines:
            line = line.strip()
            l = line.split(' ')
            if context.upper() in l:
                ind = l.index(context.upper())
                if word.upper() == l[ind+1].upper():
                    count = count + 1
    return count


def calProb(bigram_prob, unigram_prob, lambda_param):
    # This function is to implement the smoothing

    prob = lambda_param*bigram_prob + (1-lambda_param)*unigram_prob

    return prob


path_name = 'data/'
# corpus_name = 'brown.txt'
corpus_name = 'toy_corpus.txt'
modified_corpus_name = 'modified_corpus.txt'
input_str = 'JOHN READ A BOOK'
modified_input_str = '<S> ' + input_str + ' <E>'


# Appending <s> at the start and <e> at the end of each sentence in the corpus
file = open(path_name+modified_corpus_name,'w')
with open(path_name+corpus_name,'r') as corpus:
    lines = corpus.readlines()
    for line in lines:
        line = line.strip()
        new_line = "<s> " + line + " <e>\n"
        file.write(new_line.upper())

file.close()

vocabulary = []
# Size of Vocabulary
with open(path_name+modified_corpus_name,'r') as corpus:
    lines = corpus.readlines()
    for line in lines:
        line = line.strip()
        l = line.split(' ')
        for i in l:
            vocabulary.append(i)

vocabulary_set = set(vocabulary)

vocab_size = len(vocabulary_set)-2 # -2 for <s> and <e>


original_input_str = input_str.split(' ')
str_to_check = modified_input_str.split(' ')

context = 'read'
context = context.upper()
word = 'cher'
word = word.upper()
lambda_param = 0.6

dictionary = {}
# Creating dictionary with key as the word and value as the number of occurrence
with open(path_name+modified_corpus_name,'r') as corpus:
    lines = corpus.readlines()
    for line in lines:
        line = line.strip()
        l = line.split(' ')
        for i in l:
            if i in dictionary:
                dictionary[i] = dictionary[i] + 1
            else:
                dictionary[i] = 1

total_words_count = 0
for w in dictionary:
    if w not in ['<S>','<E>']:
        total_words_count += dictionary[w]


# bigram_count = findcount(context,word,path_name+modified_corpus_name)
#
# bigram_prob = bigram_count/dictionary[context]
#
# unigram_prob = dictionary[word]/total_words_count
#
# prob = calProb(bigram_prob, unigram_prob, lambda_param)


str_to_check = modified_input_str.split(' ')



prob = 1
for i in range(1, len(str_to_check)):
    context = str_to_check[i-1]
    context = context.lower()
    word = str_to_check[i]
    word = word.lower()
    bigram_count = findcount(context, word, path_name + modified_corpus_name)
    bigram_prob = bigram_count / dictionary[context.upper()]
    if i in range(1,len(str_to_check)-1):
        unigram_prob = dictionary[word.upper()] / total_words_count
    else:
        unigram_prob = 0
    p = calProb(bigram_prob, unigram_prob, lambda_param)
    prob = prob*p

print('The Prob. of the sentence \"{0}\" is {1} '.format(input_str,prob))

# Perplexity
perplexity = (1/prob)**(1/len(input_str))
print('The Perplexity of the sentence  \"{0}\" is {1} '.format(input_str,perplexity))

# print('The Prob. of \"{0}\" given context \"{1}\" is {2}'.format(word,context,prob))

