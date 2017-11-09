# -*- coding:utf-8 -*- 
# Author: Roger
import codecs
from collections import defaultdict
from builtins import range
import numpy as np
import sys
from six import iteritems


def mse(y, predict):
    return np.sqrt(np.sum(np.square(y - predict)))


def pagerank(vertex_weight, edge_matrix, max_iter=1000, stop_threshold=0.0001, factor=0.85):
    print("Vertex Number: %s." % vertex_weight.shape)
    print("Edge Size: %s." % ",".join([str(i) for i in edge_matrix.shape]))
    print("Max Iter: %d, Stop Threshold: %f, Factor: %f." % (max_iter, stop_threshold, factor))
    tp_matrix = edge_matrix / np.sum(edge_matrix, axis=1)[:, None]
    last_vertex_weight = np.copy(vertex_weight)
    for iter_index in range(max_iter):
        vertex_weight = (1 - factor) + factor * np.dot(vertex_weight, tp_matrix)
        loss = mse(last_vertex_weight, vertex_weight)
        if loss < stop_threshold:
            print("Stop at Iter %d loss: %.5f" % (iter_index, loss))
            break
        else:
            print("Iter %d loss: %.5f" % (iter_index, loss))
            last_vertex_weight = np.copy(vertex_weight)
    return vertex_weight


def load_file(filename, stop_word=None, stop_pos=None):
    word2index = dict()
    index2word = dict()
    cooc_count = defaultdict(int)

    def add_word(_w):
        if _w in stop_word:
            return
        if _w not in word2index:
            index = len(word2index)
            word2index[_w] = index
            index2word[index] = _w

    with codecs.open(filename, 'r', 'utf8') as fin:
        for line in fin:
            words = line.strip().split()
            for _w1, _w2 in zip(words[:-1], words[1:]):
                if stop_pos is not None:
                    if '/' not in _w1 or '/' not in _w2:
                        continue
                    w1, pos1 = _w1.split('/')
                    w2, pos2 = _w2.split('/')
                    if pos1 in stop_pos or pos2 in stop_pos:
                        continue
                if w1 in stop_word or w2 in stop_word:
                    continue
                add_word(w1)
                add_word(w2)
                index1, index2 = min(word2index[w1], word2index[w2]), max(word2index[w1], word2index[w2])
                cooc_count[(index1, index2)] += 1

    return index2word, cooc_count


def main():
    index2word, cooc_count = load_file(sys.argv[1], stop_word={u"，", u"。", u"？"},
                                       stop_pos={u"punctuation_mark", u"modal_particle", u"numeral",
                                                 u"pronoun", u"adverb"})
    vertex_weight = np.random.random(size=(len(index2word)))
    edge_weight = np.zeros((len(index2word), len(index2word)))
    for (index1, index2), count in iteritems(cooc_count):
        edge_weight[index1, index2] = count
        edge_weight[index2, index1] = count
    final_weight = pagerank(vertex_weight, edge_weight)
    word_weight = [(final_weight[i], index2word[i]) for i in range(final_weight.shape[0])]
    word_weight.sort(reverse=True)
    with codecs.open("test.out", 'w', 'utf8') as out:
        for weight, word in word_weight:
            out.write("%s\t%s\n" % (word, weight))


if __name__ == "__main__":
    # a = np.random.random(size=(100,))
    # b = np.random.random(size=(100, 100))
    # print(pagerank(a, b))
    main()
