import sys
import tensorflow as tf
import numpy as np
import pandas as pd
tf.set_random_seed(777)

xy = pd.read_csv('data/Admission_Predict_Ver1.1.csv')
x_data = xy.values[:, 1:-1]
x_data = (x_data-x_data.mean(axis=0))/x_data.std(axis=0)
y_data = xy.values[:, [-1]]
#xy = np.loadtxt('data/Admission_Predict_Ver1.1.csv',
#                delimiter=',',
#                dtype=np.float32,
#                skiprows=1)
#x_data = xy[:, 1:-1]
#y_data = xy[:, [-1]]

X = tf.placeholder(tf.float32, shape=[None, 7])
Y = tf.placeholder(tf.float32, shape=[None, 1])

W = tf.Variable(tf.random_normal([7, 1]), name='weight')
b = tf.Variable(tf.random_normal([1]), name='bias')

hypothesis = tf.matmul(X, W) + b

cost = tf.reduce_mean(tf.square(hypothesis - Y))

optimizer = tf.train.GradientDescentOptimizer(learning_rate=1e-5)
train = optimizer.minimize(cost)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

for step in range(2001):
    cost_val, hy_val, _ = sess.run([cost, hypothesis, train],
                                   feed_dict={X: x_data, Y: y_data})
    if step % 100 == 0:
        print(step, "Cost: ", cost_val, "\nPrediction:\n", hy_val)
