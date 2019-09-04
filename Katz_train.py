import numpy as np
import matplotlib.pyplot as plt

def findcount(context, word, filename):
    # This function finds the total count of the word given the previous context
    count = 0
    context = context.upper()
    word = word.upper()
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

def calProb(word, context, discounted_dict, dictionary, bigram_count_dict, alpha_context):
    # This function is to implement the Katz smoothing
    word = word.upper()
    context = context.upper()
    # Total word count of the words whose bigram count is zero
    word_count_zero_bigram_count = 0
    for w in dictionary:
        if bigram_count_dict[w] == 0:
            word_count_zero_bigram_count = word_count_zero_bigram_count + dictionary[w]

    if bigram_count_dict[word] == 0:
        prob = (alpha_context*dictionary[word])/word_count_zero_bigram_count
    else:
        prob = discounted_dict[word]

    return prob

def calDiscountedProb(context, dictionary, discount, filename):
    dis_dict = {}
    context = context.upper()
    bigram_count_dic = {}
    for w in dictionary:
       count_context_word = findcount(context, w, filename)
       bigram_count_dic[w] = count_context_word
       if count_context_word != 0 and dictionary[context] != 0:
           w_dis_word = count_context_word - discount
           dis_dict[w] = w_dis_word / dictionary[context]
       else:
           dis_dict[w] = 0

    return dis_dict, bigram_count_dic

def calAlpha(dis_dict):
    sum = 0
    for w in dis_dict:
        sum = sum + dis_dict[w]

    alpha = 1 - sum

    return alpha

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


# Discount
discount = 0.5
# discount = calDiscount()

# context = 'read'
# word = 'cher'
#
# discounted_dict = {}
# discounted_dict, bigram_count_dict = calDiscountedProb(context, dictionary, discount, path_name+modified_corpus_name)
#
# alpha_context = calAlpha(discounted_dict)
#
# prob = calProb(word, context, discounted_dict, dictionary, bigram_count_dict, alpha_context)

str_to_check = modified_input_str.split(' ')

# prob = 1
# for i in range(1, len(str_to_check)):
#     context = str_to_check[i-1]
#     context = context.lower()
#     word = str_to_check[i]
#     word = word.lower()
#     discounted_dict = {}
#     discounted_dict, bigram_count_dict = calDiscountedProb(context, dictionary, discount,
#                                                            path_name + modified_corpus_name)
#     alpha_context = calAlpha(discounted_dict)
#     p = calProb(word, context, discounted_dict, dictionary, bigram_count_dict, alpha_context)
#     prob = prob*p
#
#
# # print('The Prob. of \"{0}\" given context \"{1}\" is {2}'.format(word,context,prob))
#
# print('The Prob. of the sentence \"{0}\" is {1} '.format(input_str,prob))
#
# # Perplexity
# perplexity = (1/prob)**(1/len(input_str))
# print('The Perplexity of the sentence  \"{0}\" is {1} '.format(input_str,perplexity))


# context = 'A'
context = 'READ'
probdicUnsmo = {}
probus = []
for w in dictionary:
    if w != context and w not in ['<S>','<E>']:
        bigram_count = findcount(context, w, path_name + modified_corpus_name)
        bigram_prob = bigram_count / dictionary[context.upper()]
        probdicUnsmo[w] = bigram_prob

probdicsmo = {}
probs = []
for w in dictionary:
    if w != context and w not in ['<S>','<E>']:
        discounted_dict = {}
        discounted_dict, bigram_count_dict = calDiscountedProb(context, dictionary, discount,
                                                               path_name + modified_corpus_name)
        alpha_context = calAlpha(discounted_dict)
        probdicsmo[w] = calProb(w, context, discounted_dict, dictionary, bigram_count_dict, alpha_context)

# Creating dictionary with key as the word and value as the number of occurrence
for w in probdicsmo:
    probs.append(probdicsmo[w])

# Creating dictionary with key as the word and value as the number of occurrence
for w in probdicUnsmo:
    probus.append(probdicUnsmo[w])

width = 0.5
x = np.arange(len(probdicUnsmo))
plt.rcdefaults()
fig, ax = plt.subplots()
ax.barh(x, probs,width, color='g' ,align='center',label='Interpolation')
ax.barh(x+width, probus, width, color='b', align='center',label='Unsmoothed')
ax.set_yticks(range(len(probdicUnsmo)))
ax.set_yticklabels(probdicUnsmo)
# ax.invert_yaxis()
ax.set_xlabel('Probabilites')
# ax.set_title('Bar Graph for Unsmoothed Unigram')
ax.set_title('Bar Graph for Unsmoothed and Katz on Bigram Context=\'READ\' with discount=0.5')


ax.legend()

plt.show()