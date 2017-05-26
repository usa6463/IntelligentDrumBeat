# -*- coding:utf-8-*-
import tensorflow as tf
import numpy as np
import os
from tqdm import tqdm

nb_classes = 23
train_feature_num = 42
test_feature_num = 42

test_file = 'C:\\Users\\ISK\\Desktop\\kdd\\test\\test.csv'
train_file = 'C:\\Users\\ISK\\Desktop\\kdd\\train\\train.csv'

batch_size=100

filename_queue1 = tf.train.string_input_producer([train_file], shuffle=False, name = 'filename_queue1')
reader1 = tf.TextLineReader()
key1, value1 = reader1.read(filename_queue1)
record_defaults1=[[0.]]*train_feature_num
xy1 = tf.decode_csv(value1, record_defaults=record_defaults1)
train_x_batch, train_y_batch = tf.train.batch([xy1[:-1], xy1[-1:]], batch_size=batch_size)

filename_queue2 = tf.train.string_input_producer([test_file], shuffle=False, name = 'filename_queue2')
reader2 = tf.TextLineReader()
key2, value2 = reader2.read(filename_queue2)
record_defaults2=[[0.]]*test_feature_num
xy2 = tf.decode_csv(value2, record_defaults=record_defaults2)
test_x_batch, test_y_batch = tf.train.batch([xy2[:-1], xy2[-1:]], batch_size=batch_size)

X = tf.placeholder(tf.float32, shape=[None, 41])
X_min = tf.reduce_min(X)
X_max = tf.reduce_max(X)
norm_X = (X - X_min) / (X_max - X_min)
#X = tf.nn.l2_normalize(X, dim=1, epsilon=1e-1)
Y = tf.placeholder(tf.float32, shape=[None, 1])
Y_one_hot = tf.one_hot(tf.cast(Y, tf.int32), nb_classes)
Y_one_hot = tf.reshape(Y_one_hot, [-1, nb_classes])

W = tf.Variable(tf.random_normal([41,nb_classes]))
b = tf.Variable(tf.random_normal([nb_classes]))

H = tf.nn.softmax(tf.matmul(norm_X,W)+b)
cost = tf.reduce_mean(-tf.reduce_sum(Y_one_hot*tf.log(H), axis=1))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=1e-2)
train = optimizer.minimize(cost)

prediction = tf.argmax(H, 1)
correct_prediction = tf.equal(prediction, tf.argmax(Y_one_hot, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())
	coord = tf.train.Coordinator()
	threads = tf.train.start_queue_runners(coord=coord, sess=sess)
	totalTestFileNum = 494021
	totalTrainingFileNum = 4898431
	training_epochs = 5  # 에폭 횟수

	print('훈련 시작, 총 에폭 수 : {}, 배치 크기 : {}'.format(training_epochs, batch_size))
	avg_cost = 0
	for epoch in range(training_epochs):
		total_batch = int(totalTrainingFileNum / batch_size)

		for i in tqdm(range(total_batch)):
			batch_xs, batch_ys = sess.run([train_x_batch, train_y_batch])
			c, _ = sess.run([cost, train], feed_dict = {X:batch_xs, Y:batch_ys})
			avg_cost += c / total_batch

		print('epoch : %04d'%(epoch+1), 'cost : %09f'%avg_cost)

	print('테스트 시작')
	avg_acc = 0
	total_batch = int(totalTestFileNum / batch_size)
	for i in tqdm(range(total_batch)):
		batch_xs, batch_ys = sess.run([test_x_batch, test_y_batch])
		acc = accuracy.eval(session=sess, feed_dict={X:batch_xs, Y:batch_ys})
		avg_acc += acc / total_batch
	print('accuracy : {}'.format(avg_acc))

	coord.request_stop()
	coord.join(threads)
