import numpy as np
import matplotlib.pyplot as plt



def calProb(word, dictionary):
    # This function is to implement the Good Turing smoothing
    # word = word.upper()
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

# dictionary = {}
# # Creating dictionary with key as the word and value as the number of occurrence
# with open(path_name+modified_corpus_name,'r') as corpus:
#     lines = corpus.readlines()
#     for line in lines:
#         line = line.strip()
#         l = line.split(' ')
#         for i in l:
#             if i in dictionary:
#                 dictionary[i] = dictionary[i] + 1
#             else:
#                 dictionary[i] = 1

dictionary = {'carp':3,'perch':3,'whitefish':2,'trout':2,'salmon':2,'eel':1,'catfish':1,'bass':0}

total_words_count = 0
for w in dictionary:
    if w not in ['<S>','<E>']:
        total_words_count += dictionary[w]

probdictionaryunsmo = {}
# Creating dictionary with key as the word and value as the number of occurrence
for w in dictionary:
    if dictionary[w] != 3:
        probdictionaryunsmo[w] = dictionary[w]/total_words_count

probdictionarysmo = {}
for w in dictionary:
    if dictionary[w] != 3:
        probdictionarysmo[w] = calProb(w, dictionary)


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
ax.barh(x+width, probsm,width, color='g' ,align='center',label='Good Turing')
ax.set_yticks(range(len(probdictionaryunsmo)))
ax.set_yticklabels(probdictionaryunsmo)
# ax.invert_yaxis()
ax.set_xlabel('Probabilites')
# ax.set_title('Bar Graph for Unsmoothed Unigram')
ax.set_title('Bar Graph for Unsmoothed and Good Turing Unigram')


print((len(probdictionaryunsmo)))

ax.legend()

plt.show()

# print('Prob of the word {0} is {1}'.format(input_word,prob))

# Perplexity
# perplexity = (1/prob)**(1/len(input_str))
# print('The Perplexity of the sentence  \"{0}\" is {1} '.format(input_str,perplexity))
