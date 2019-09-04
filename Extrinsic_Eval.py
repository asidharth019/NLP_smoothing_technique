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


def calProb(numerator, denominator, vocab_s, smooth_tech):
    # This function is to implement the smoothing

    if smooth_tech == 1: # Without Smoothing
        prob = numerator/denominator
    elif smooth_tech == 2: # Add1 or Laplace Smoothing
        prob = (numerator + 1)/(denominator + vocab_size)

    return prob


path_name = 'data/'
# corpus_name = 'brown.txt'
corpus_name = 'toy_corpus.txt'
modified_corpus_name = 'modified_corpus.txt'
input_str1 = 'JOHN READ A BOOK'
input_str2= 'JOHN RED A BOOK'
modified_input_str1 = '<S> ' + input_str1 + ' <E>'
modified_input_str2 = '<S> ' + input_str2 + ' <E>'
gram_number = 2
smooth_tech = 2# 1-without smoothing
                # 2-Add1 Smoothing


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

str_to_check1 = modified_input_str1.split(' ')
str_to_check2 = modified_input_str2.split(' ')


prob = 1
for i in range(1, len(str_to_check1)):
    context = str_to_check1[i-1]
    context = context.lower()
    word = str_to_check1[i]
    word = word.lower()
    count_word_context = findcount(context, word, path_name+modified_corpus_name)
    count_context_allword = 0
    for w in vocabulary_set:
        count_context_allword = count_context_allword + findcount(context, w, path_name+modified_corpus_name)
    p = calProb(count_word_context, count_context_allword, vocab_size, smooth_tech)
    prob = prob*p

print('The Prob. of the sentence \"{0}\" is {1} '.format(input_str1,prob))

# Perplexity
perplexity = (1/prob)**(1/len(input_str1))
print('The Perplexity of the sentence  \"{0}\" is {1} '.format(input_str1,perplexity))


prob = 1
for i in range(1, len(str_to_check2)):
    context = str_to_check2[i-1]
    context = context.lower()
    word = str_to_check2[i]
    word = word.lower()
    count_word_context = findcount(context, word, path_name+modified_corpus_name)
    count_context_allword = 0
    for w in vocabulary_set:
        count_context_allword = count_context_allword + findcount(context, w, path_name+modified_corpus_name)
    p = calProb(count_word_context, count_context_allword, vocab_size, smooth_tech)
    prob = prob*p


print('\nThe Prob. of the sentence \"{0}\" is {1} '.format(input_str2,prob))

# Perplexity
perplexity = (1/prob)**(1/len(input_str2))
print('The Perplexity of the sentence  \"{0}\" is {1} '.format(input_str2,perplexity))


