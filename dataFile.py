import json


from collections import Counter
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
import string

# variable for ploting
frequency = []
rank=[]

## function for spliting the strings
def split_and_print(line):
    current_line_body = line['body']
    current_line_email = line['emails']
    final_list = []

    k = 0
    while (len(current_line_body) != k):
        x = current_line_body[k]
        split_list = x.split()
        # print(split_list)
        final_list += split_list
        k = k + 1
        # print("Final List : " , final_list , "\n")
        split_list = []
    print("String Found : ", final_list)
    return final_list


# function for printing the table
def print_table(top_20_withoutStopWords, totalNumberOfStrings):
    i = 0
    j = 0

    print("_____________________________________________________________________________")
    print("-----------------------------------------------------------------------------")

    while (i < 15):
        print("{:2}{:2}{:15}{:1}{:5}{:4}{:.4f}{:10}{:2}{:2}{:15}{:1}{:5}{:4}{:.4f}".format(i+1," ",top_20_withoutStopWords[i][0], ":", top_20_withoutStopWords[i][1]," ", top_20_withoutStopWords[i][1]/totalNumberOfStrings,
                                                     " ",i+16,"",  top_20_withoutStopWords[i + 15][0], ":",
                                                     top_20_withoutStopWords[i + 15][1], " ", top_20_withoutStopWords[i + 15][1]/totalNumberOfStrings))
        # print(top_20_withoutStopWords[i][0], "  :",top_20_withoutStopWords[i][1], "             ",top_20_withoutStopWords[i+10][0], "  :",top_20_withoutStopWords[i+10][1] )
        i += 1
    print("\n\n")


num = sum(1 for line in open("abcd.json")) # num of line in the json file
print("num: " , num)
f = open("abcd.json")
dat = json.load(f)
i =0

current_line = dat[i] # taking each line
final_total_list = []
print(current_line)
total_email_extratcted = []


# loop for each line to merge all the emails and words
while(i != num-3):
    string_list = split_and_print(current_line)
    print("Emails Extracted: ", current_line["emails"])
    print("\n\n\n")

    # total list for counting occurances
    final_total_list += string_list
    total_email_extratcted += current_line["emails"]
    i = i + 1
    current_line = dat[i]


# printing email extracted
print("Total Email extracted:   ", total_email_extratcted)
count3 = Counter(total_email_extratcted)
count4 = count3.most_common(10)
print(count3, "\n\n")


# count to count the ocurances
totalNumberOfStrings = len(final_total_list)
count = Counter(final_total_list)
top_30_withoutStopWords =  count.most_common(30)

# printing table without stop words
print("             Most Occurance without StopWords           ")
print_table(top_30_withoutStopWords,totalNumberOfStrings)




## with stop words:
stopword = set.union(set(stopwords.words('english')),set(string.punctuation))
for word in list(final_total_list):  # iterating on a copy since removing will mess things up
    if word in stopword:
        final_total_list.remove(word)



count2 = Counter(final_total_list)
top_30_withStopWords = count2.most_common(30)

j = 0


# frequency for ranking and ploting
while(j < 30):
    frequency.append(top_30_withStopWords[j][1])
    j += 1




totalNumberOfStrings = len(final_total_list)
print("              Most Occurance with StopWords                ")
print_table(top_30_withStopWords,totalNumberOfStrings)


print("most common 10 emails in a list::  ")
print("--------------------------------")
i = 0

while(i < 10):
    print("{:30}{:3}{:3}".format(count4[i][0], " ", count4[i][1]))
    i += 1


# ploting the frequency
plt.plot(frequency)
plt.xlabel("rank")
plt.ylabel("occuarnces")
plt.show()

plt.loglog(frequency)
plt.xlabel("rank")
plt.ylabel("occuarnces")
plt.show()






































