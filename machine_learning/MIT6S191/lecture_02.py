# Deep Sequence Modelling

# ----- Examples:
# predict ball position next second
# predict the missing words

# variable-length
# long-term
# order
# share parameters

# RNNs: Recurrent Neural Networks
# h(t) = f_w(h(t-1), x(t))

my_rnn = RNN()
hidden_state = [0, 0, 0, 0]

sentence = ['I', 'love', 'recurrent', 'neutral']

for work in sentence:
  prediction, hidden_state = my_rnn(word, hidden_state)

next_word_prediction = prediction
