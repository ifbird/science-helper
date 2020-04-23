import tensorflow as tf


# ----- Define sequential layers, hidden layers, and outputs
# model = tf.keras.Sequential([ \
#   tf.keras.layers.Dense(n1), \
#   tf.keras.layers.Dense(n2), \
#   ...
#   tf.keras.layers.Dense(m), \
#   ])


# ----- Pick your favorite optimizer
optimizer = tf.keras.optimizer.SGD()

while True:
  prediction = model(x)

  with tf.GradientTape() as g:
    loss = compute_loss(weights)
    gradient = g.gradient(loss, model.trainable_variables)

  optimizer.apply_gradients( zip(grads, model.trainable_variables) )

  # weights = weights - lr * gradient


# ----- Dense layer with 2 outputs
# layer = tf.keras.layers.Dense(units=2)




# ----- Loss functions

# binary cross entropy loss:
# J(W) = 1/n * sum_1^n ( yi*log(f(xi, W)) + (1-yi)*log(1-f(xi, W)) )
# loss = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(y, predicted) )

# Mean squared error loss
# loss = tf.reduce_mean( tf.square(tf.subtract(y, predicted)) )
  


class MyDenseLayer(tf.keras.layers.Layer):
  def __init__(self, input_dim, output_dim):
    super(MyDenseLayer, self).__init__()

    # Initialize weights and bias
    self.W = self.add_weight([input_dim, output_dim])
    self.b = self.add_weight([1, output_dim])


  def call(self, inputs):
    # Forward propagate the inputs
    z = tf.matmul(inputs, self.W) + self.b

    # Feed through a non-linear activation
    output = tf.math.sigmoid(z)

    return output


weights = tf.Variable( [tf.random.normal()] )


# ----- Regularization 1: Dropout
# tf.keras.layers.Dropout(p=0.5)

# ----- Regularization 2: Early Stopping
