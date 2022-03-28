# Name: Sai Anish Garapati
# UIN: 650208577

import os
import string
import nltk
import re
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def _remove_stop_words(words_list):
    stop_words = set(stopwords.words('english'))
    return [word for word in words_list if word not in stop_words]


def _apply_stemmer(words_list):
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    return [ps.stem(word) for word in words_list if ps.stem(word) not in stop_words]


def _word_preprocessing(content):
    words_list = word_tokenize(content)
    words_list = [word.translate(str.maketrans('', '', string.punctuation))
                  for word in words_list]
    words_list = [word.lower() for word in words_list if word != '']

    words_list = _remove_stop_words(words_list)
    words_list = _apply_stemmer(words_list)

    # return [word for word in words_list if len(word) > 2]
    return words_list


def _query_preprocessing(query):
    query_dict = {}
    query_list = text_preprocesser().preprocessing(query)
    for word in query_list:
        if word in query_dict:
            query_dict[word] += 1
        else:
            query_dict[word] = 1
    return query_dict


class text_preprocesser:
    def __init__(self):
        pass

    def preprocessing(self, page_content):
        page_content = re.sub(re.compile('<.*>\n'), '', page_content)
        page_content = re.sub(re.compile('[0-9]'), '', page_content)
        # print(page_content)

        words_list = _word_preprocessing(page_content)
        return words_list


class IR_system:
    def __init__(self):
        self.inverted_index = {}
        self.page_lengths = {}

    def build_inverted_index(self, page_index_table):
        for link, page_words_list in page_index_table.items():
            for word in page_words_list:
                if word in self.inverted_index:
                    if link not in self.inverted_index[word]:
                        self.inverted_index[word].update({link: 0})
                else:
                    self.inverted_index[word] = {link: 0}
                self.inverted_index[word][link] += 1

    def compute_webpage_lengths(self, page_index_table):
        self.page_lengths = {page: 0.0 for page in page_index_table.keys()}
        for link, page_words_list in page_index_table.items():
            for word in page_words_list:
                self.page_lengths[link] += (self.inverted_index[word][link] * math.log(
                    float(len(page_index_table)/len(self.inverted_index[word]))))**2
            self.page_lengths[link] = math.sqrt(self.page_lengths[link])

    def compute_ranked_docs(self, query):
        processed_query = _query_preprocessing(query)
        ranked_docs_query = {page: 0.0 for page in self.page_lengths.keys()}
        query_length = 0.0
        for query_term in processed_query:
            if query_term in self.inverted_index:
                for key in self.inverted_index[query_term]:
                    ranked_docs_query[key] += (self.inverted_index[query_term][key] * processed_query[query_term]) * (
                        math.log(float(len(self.page_lengths))/float(len(self.inverted_index[query_term]))))**2
                query_length += (processed_query[query_term] * math.log(
                    float(len(self.page_lengths))/float(len(self.inverted_index[query_term]))))**2

        # Cosine Similarity
        for link in self.page_lengths:
            if self.page_lengths[link] != 0 and query_length != 0:
                ranked_docs_query[link] /= (self.page_lengths[link] * math.sqrt(query_length))

        # Dice Coefficient
        # for link in self.page_lengths:
            # if self.page_lengths[link] != 0 and query_length != 0:
                # ranked_docs_query[link] = 2 * ranked_docs_query[link] / (self.page_lengths[link]**2 + query_length)

        ranked_docs_query = {key: val for key, val in sorted(
            ranked_docs_query.items(), key=lambda x: x[1], reverse=True)}
        return ranked_docs_query
