# -*- coding:utf-8 -*- 
# Author: Roger
import numpy as np

def mse(y, predict):
    return np.sqrt(np.sum(np.square(y - predict)))


def pagerank(vertex_weight, edge_matrix, max_iter=1000, stop_threshold=0.0001, factor=0.85):
    print("Vertex Number: %s." % vertex_weight.shape)
    print("Edge Size: %s." % ",".join([str(i) for i in edge_matrix.shape]))
    print("Max Iter: %d, Stop Threshold: %f, Factor: %f." % (max_iter, stop_threshold, factor))
    tp_matrix = edge_matrix / np.sum(edge_matrix, axis=1)[:, None]
    last_vertex_weight = np.copy(vertex_weight)
    for iter_index in xrange(max_iter):
        vertex_weight = (1 - factor) + factor * np.dot(vertex_weight, tp_matrix)
        loss = mse(last_vertex_weight, vertex_weight)
        if loss < stop_threshold:
            print("Stop at Iter %d loss: %.5f" % (iter_index, loss))
            break
        else:
            print("Iter %d loss: %.5f" % (iter_index, loss))
            last_vertex_weight = np.copy(vertex_weight)
    return vertex_weight


if __name__ == "__main__":
    a = np.random.random(size=(100,))
    b = np.random.random(size=(100, 100))
    print pagerank(a, b)
