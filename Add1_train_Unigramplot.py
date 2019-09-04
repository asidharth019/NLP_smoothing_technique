import numpy as np
import matplotlib.pyplot as plt

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
        prob = (numerator + 1)/(denominator + vocab_s)

    return prob


path_name = 'data/'
# corpus_name = 'brown.txt'
corpus_name = 'toy_corpus.txt'
modified_corpus_name = 'modified_corpus.txt'
input_str = 'JOHN READ A BOOK'
# input_str = 'CHER READ A BOOK'
# input_str = 'i saw a man'
modified_input_str = '<S> ' + input_str + ' <E>'
gram_number = 2
smooth_tech = 1# 1-without smoothing
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


original_input_str = input_str.split(' ')
str_to_check = modified_input_str.split(' ')


#
# prob = 1
# for i in range(1, len(str_to_check)):
#     context = str_to_check[i-1]
#     context = context.lower()
#     word = str_to_check[i]
#     word = word.lower()
#     count_word_context = findcount(context, word, path_name+modified_corpus_name)
#     count_context_allword = 0
#     co= 0
#     for w in vocabulary_set:
#         count_context_allword = count_context_allword + findcount(context, w, path_name+modified_corpus_name)
#         # co +=1
#         # if co > 5:
#         #     break
#     p = calProb(count_word_context, count_context_allword, vocab_size, smooth_tech)
#     prob = prob*p
#
# print('The Prob. of the sentence \"{0}\" is {1} '.format(input_str,prob))
#
# # Perplexity
# perplexity = (1/prob)**(1/len(input_str))
# print('The Perplexity of the sentence  \"{0}\" is {1} '.format(input_str,perplexity))
#
#


# Unigram count of the words


# dictionary = plt.figure()
#
# plt.barh(range(len(probdictionary)), probdictionary.values(), align='center')
# plt.yticks(range(len(probdictionary)), probdictionary)
#
# plt.show()


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

probdictionaryunsmo = {}
# Creating dictionary with key as the word and value as the number of occurrence
for w in dictionary:
    if w not in ['<S>', '<E>']:
        probdictionaryunsmo[w] = calProb(dictionary[w],total_words_count,vocab_size,1)

probdictionarysmo = {}
# Creating dictionary with key as the word and value as the number of occurrence
for w in dictionary:
    if w not in ['<S>', '<E>']:
        probdictionarysmo[w] = calProb(dictionary[w],total_words_count,vocab_size,2)

plt.rcdefaults()
fig, ax = plt.subplots()

probsm = []
# Creating dictionary with key as the word and value as the number of occurrence
for w in probdictionaryunsmo:
    probsm.append(probdictionarysmo[w])

probusm = []
# Creating dictionary with key as the word and value as the number of occurrence
for w in probdictionaryunsmo:
    probusm.append(probdictionaryunsmo[w])

width = 0.5
x = np.arange(len(probdictionaryunsmo))

ax.barh(x, probusm, width, color='b', align='center',label='Unsmoothed')
ax.barh(x+width, probsm,width, color='g' ,align='center',label='Add-1')
ax.set_yticks(range(len(probdictionaryunsmo)))
ax.set_yticklabels(probdictionaryunsmo)
# ax.invert_yaxis()
ax.set_xlabel('Probabilites')
# ax.set_title('Bar Graph for Unsmoothed Unigram')
ax.set_title('Bar Graph for Unsmoothed and Add-1 Unigram')


print((len(probdictionaryunsmo)))

ax.legend()

plt.show()
