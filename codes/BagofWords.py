#importing necessary modules
import csv
import numpy as np
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline

#creating stemmer for stemming
ps = PorterStemmer()
categories = ["neutral","anger", "disgust", "fear", "Guilt", "Interest", "Joy", "Sad", "shame", "surprise"]
stopwords = stopwords.words("english")

#text will contain the tweets
text = []
#cat will contain the emotion category of tweets
cat =[]

#reading data from csv file
with open("../data/tweets.csv") as tweet:
    reader = csv.reader(tweet)
    for row in reader:
        text.append(row[0])
        cat.append(row[1])

#Preprocessing task
# temp = []
# for i in range(4000):
#     temp=word_tokenize(text[i], language="english")
#     text[i] = ""
#     for j in range(len(temp)):
#         if temp[j] not in stopwords:
#             temp[j] = ps.stem(temp[j])
#             text[i] += temp[j] + " "

#Splitting data into 80% and 20%
trainText = text[:800]
trainCat = cat[:800]
testText = text[800:]
testCat = cat[800:]

#Building the pipeline for sequential tasks
#This pipeline will first vectorize the text as Bag of Words
#  then find the IF_IDF of the terms
text_classifier = Pipeline([('vectorizer', CountVectorizer()),
                            ('tfidfFinder', TfidfTransformer()),
                            ('classifier', MultinomialNB()),])
#creating the classifier
text_clf = text_classifier.fit(trainText, trainCat)

#Evaluation
doc_test = testText
predicted  = text_clf.predict(testText)

#printing classification accuracy
print("\nNaive Bayesian Classifier accuracy: ",np.mean(predicted == testCat)*100,"%")
#printing classification summary
print("Classification summary for NB Classifier:\n")
print(metrics.classification_report(testCat, predicted, target_names=categories))
#printing confusin matrix
print("Confusion Matrix for Classification using NB Classifier:\n")
print(metrics.confusion_matrix(testCat, predicted))

#Neural Neteork Classifier
text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
                     ('clf', MLPClassifier(hidden_layer_sizes=(13,13,13),
                                           max_iter=1000)),])
text_clf= text_clf.fit(trainText, trainCat)
predicted = text_clf.predict(testText)
print("\nNN Accuracy: ",np.mean(predicted == testCat)*100,"%")

print("Classification summary for ANN:\n")
print(metrics.classification_report(testCat, predicted, target_names=categories))
print("Confusion Matrix for Classification using ANN:\n")
print(metrics.confusion_matrix(testCat, predicted))

#using Support vector machine
text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2',
                        alpha=1e-3, n_iter=5, random_state=42)),])
text_clf= text_clf.fit(trainText, trainCat)
predicted = text_clf.predict(testText)
print("\nSVM Accuracy: ",np.mean(predicted == testCat)*100,"%")

print("Classification summary for SVM:\n")
print(metrics.classification_report(testCat, predicted, target_names=categories))
print("Confusion Matrix for Classification using SVM:\n")
print(metrics.confusion_matrix(testCat, predicted))


data = ["I don't love my country"]
clasLabel = text_clf.predict(data)
print("Emotion of data: ", categories[int(clasLabel[0])])
