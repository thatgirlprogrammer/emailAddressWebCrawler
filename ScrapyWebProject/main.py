import json
import math
import string
import nltk as nltk
import matplotlib.pyplot as plt  

f = open('tutorial/ksuemail.json')
data = json.load(f)
word_freq = {}
word_freq2 = {}
email_freq = {}
email_page_count = 0
total_words = 0


def update_dict(dict, lst):
    for value in lst:
        if value in dict:
            dict[value] += 1
        else:
            dict.update({value: 1})


stop_words = nltk.corpus.stopwords.words("english")
for i in data:
    if len(i['emails']) > 0:
        email_page_count += 1
        update_dict(email_freq, i['emails'])

    wordLst = i['body'].split(" ")
    total_words += len(wordLst)
    update_dict(word_freq, wordLst)
    wordLst = i['body'].translate(str.maketrans('', '', string.punctuation)).split(" ")

    word_tokens = nltk.word_tokenize(i['body'])
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    update_dict(word_freq2, filtered_sentence)

email_freq = {k: v for k, v in sorted(email_freq.items(), key=lambda item: item[1], reverse=True)}
word_freq = {k: v for k, v in sorted(word_freq.items(), key=lambda item: item[1], reverse=True)}
word_freq2 = {k: v for k, v in sorted(word_freq2.items(), key=lambda item: item[1], reverse=True)}

print("Average page length:", total_words / len(data))
print(email_freq)
print("Percentage of pages with emails:", email_page_count / len(data) * 100)

print("Top word freq before removing punctuation and stopwords")
print("randk\t\tterm\t\t\tfreq")
print("------\t\t--------\t\t-------")
count = 1
values1 = []
for key in word_freq:
    count += 1
    values1.append(word_freq[key])
    if count <= 30:
        print(count, "\t\t", key, "\t\t\t", word_freq[key] / total_words * 100)

total_words = 0
for key in word_freq2:
    total_words += word_freq2[key]

print("Top word freq after removing punctuation and stopwords")
print("randk\t\tterm\t\t\tfreq")
print("------\t\t--------\t\t-------")
count = 1
for key in word_freq2:
    count += 1
    if count <= 30:
        print(count, "\t\t", key, "\t\t\t", word_freq2[key] / total_words * 100)


plt.plot(values1)
plt.ylabel('Word Frequency')
plt.xlabel('Rank')
plt.show()

values2 = [math.log10(value) for value in values1]
plt.plot(values2)
plt.ylabel('Log Word Frequency')
plt.xlabel('Rank')
plt.show()