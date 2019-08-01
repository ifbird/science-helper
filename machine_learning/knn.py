import sys

import numpy as np
from sklearn import datasets
from collections import Counter

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#==============================================================================#
# Helper functions
#==============================================================================#
def distance(instance1, instance2):
  # just in case, if the instances are lists or tuples:
  instance1 = np.array(instance1) 
  instance2 = np.array(instance2)
  
  return np.linalg.norm(instance1 - instance2)


def get_neighbors(training_set, 
                  labels, 
                  test_instance, 
                  k, 
                  distance=distance):
  """
  get_neighors calculates a list of the k nearest neighbors
  of an instance 'test_instance'.
  The list neighbors contains 3-tuples with  
  (index, dist, label)
  where 
  index    is the index from the training_set, 
  dist     is the distance between the test_instance and the 
           instance training_set[index]
  distance is a reference to a function used to calculate the 
           distances
  """

  # Init the distances list
  distances = []

  # Calculate the dist between test_instance and all training set
  for index in range(len(training_set)):
    dist = distance(test_instance, training_set[index])
    distances.append((training_set[index], dist, labels[index]))

  # Sort the distances list, starting from the smallest dist
  distances.sort(key=lambda x: x[1])

  # Select the smallest k elements as the neighbors
  neighbors = distances[:k]

  return neighbors


def vote(neighbors):
  class_counter = Counter()
  for neighbor in neighbors:
    class_counter[neighbor[2]] += 1

  print(class_counter)
  return class_counter.most_common(1)[0][0]


def vote_prob(neighbors):
  class_counter = Counter()
  for neighbor in neighbors:
    class_counter[neighbor[2]] += 1

  labels, votes = zip(*class_counter.most_common())
  winner = class_counter.most_common(1)[0][0]
  votes4winner = class_counter.most_common(1)[0][1]

  return winner, votes4winner/sum(votes)


#==============================================================================#
# Get the data from sklearn sample datasets
#==============================================================================#
iris = datasets.load_iris()
iris_data = iris.data
iris_labels = iris.target
ndata = len(iris_data)

print('Type of iris:', type(iris))
print('Type of iris_data:', type(iris_data))
print('Type of iris_labels:', type(iris_labels))
# print(iris_data[0], iris_data[79], iris_data[100])
# print(iris_labels[0], iris_labels[79], iris_labels[100])

# print(iris_data.shape)


#==============================================================================#
# Divide the data to learnset and testset
#==============================================================================#

# Set random seed
np.random.seed(42)

# Disorder indices
indices = np.random.permutation(ndata)

# Nubmer of training samples (testset)
n_training_samples = 12
n_learning_samples = ndata - n_training_samples

# Get learnset data and their labels
learnset_data = iris_data[indices[:-n_training_samples]]
learnset_labels = iris_labels[indices[:-n_training_samples]]

# Get testset data and their labels
testset_data = iris_data[indices[-n_training_samples:]]
testset_labels = iris_labels[indices[-n_training_samples:]]

# Print info
print('Type of learnset data:', type(learnset_data))
print('Type of learnset labels:', type(learnset_labels))

print(learnset_data[:4], learnset_labels[:4])
print(testset_data[:4], testset_labels[:4])


#==============================================================================#
# Plot data
#==============================================================================#
"""
colours = ("r", "b")
X = []

for iclass in range(3):
  X.append([[], [], []])
  for i in range(len(learnset_data)):
    if learnset_labels[i] == iclass:
      X[iclass][0].append(learnset_data[i][0])
      X[iclass][1].append(learnset_data[i][1])
      X[iclass][2].append(sum(learnset_data[i][2:]))

colours = ("r", "g", "y")

fg = plt.figure()
ax = fg.add_subplot(111, projection='3d')

for iclass in range(3):
  ax.scatter(X[iclass][0], X[iclass][1], X[iclass][2], c=colours[iclass])
# plt.show()
fg.savefig('learnset.png', dpi=150)
"""


#==============================================================================#
# Test distance function
#==============================================================================#
print(distance([3, 5], [1, 1]))
print(distance(learnset_data[3], learnset_data[44]))


#==============================================================================#
# Test get_neighbors function
#==============================================================================#
for i in range(5):
  neighbors = get_neighbors(learnset_data, learnset_labels, testset_data[i], 3, distance=distance)

  print(i, testset_data[i], testset_labels[i], neighbors)


#==============================================================================#
# Test vote function
#==============================================================================#
for i in range(n_training_samples):
  neighbors = get_neighbors(learnset_data, learnset_labels, testset_data[i], 5, distance=distance)
  print("index: ", i, ", result of vote: ", vote(neighbors), ", label: ", testset_labels[i], ", data: ", testset_data[i])


#==============================================================================#
# Test vote_prob function
#==============================================================================#
for i in range(n_training_samples):
  neighbors = get_neighbors(learnset_data, learnset_labels, testset_data[i], 5, distance=distance)
  print("index: ", i, ", vote_prob: ", vote_prob(neighbors), ", label: ", testset_labels[i], ", data: ", testset_data[i])
