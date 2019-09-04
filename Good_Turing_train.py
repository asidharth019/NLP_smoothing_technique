import numpy as np


def calProb(word, dictionary):
    # This function is to implement the Good Turing smoothing
    word = word.upper()
    if word in dictionary:
        c = dictionary[word]

        total_word_count = 0
        word_with_c = 0
        word_with_c1 = 0
        for w in dictionary:
            total_word_count = total_word_count + dictionary[w]
            if dictionary[w] == c:
                word_with_c = word_with_c + 1
            if dictionary[w] == (c+1):
                word_with_c1 = word_with_c1 + 1

        c_star = ((c+1)*word_with_c1)/word_with_c

        prob = c_star/total_word_count

    else:
        word_with_count1 = 0
        total_word_count = 0
        for w in dictionary:
            total_word_count = total_word_count + dictionary[w]
            if dictionary[w] == 1:
                word_with_count1 = word_with_count1 + 1

        prob = word_with_count1/total_word_count

    return prob


path_name = 'data/'
# corpus_name = 'brown.txt'
corpus_name = 'toy_corpus.txt'
modified_corpus_name = 'modified_corpus.txt'
input_word = 'from'
input_word = input_word.upper()



# Making the corpus into upper case
file = open(path_name+modified_corpus_name,'w')
with open(path_name+corpus_name,'r') as corpus:
    lines = corpus.readlines()
    for line in lines:
        line = line.strip()
        file.write(line.upper()+'\n')

file.close()

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


prob = calProb(input_word, dictionary)

print('Prob of the word {0} is {1}'.format(input_word,prob))

# Perplexity
# perplexity = (1/prob)**(1/len(input_str))
# print('The Perplexity of the sentence  \"{0}\" is {1} '.format(input_str,perplexity))
