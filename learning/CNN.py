# -*- coding:utf-8-*-
import tensorflow as tf
import numpy as np
import os
import sys
from tqdm import tqdm

#tfrecord에 몇개의 example이 있는지 반환하는 함수
def get_num_records(tf_record_file):
  return len([x for x in tf.python_io.tf_record_iterator(tf_record_file)])

# 파라미터로 test, train용 데이터를 가진 폴더를 말해줘야한다.
num = len(sys.argv)
if num != 2:
	print('wrong parameters')
	exit()

# train과 test용 파일들의 파일명 불러오기. + tfrecord 에 들어있는 파일 개수 세기
path = sys.argv[1]
if path[-1] != '/':
	path += '/'

print('train 파일 개수 세는중...')
train_files = os.listdir(path + 'train')
train_files_num = 0
for i in tqdm(range(len(train_files))):
	train_files[i] = path + 'train/'+train_files[i]
	train_files_num += get_num_records(train_files[i])
print('train 음악파일 개수 : {}'.format(train_files_num))

print('test 파일 개수 세는중...')
test_files = os.listdir(path + 'test')
test_files_num = 0
for i in tqdm(range(len(test_files))):
	test_files[i] = path + 'test/'+test_files[i]
	test_files_num += get_num_records(test_files[i])
print('test 음악파일 개수 : {}'.format(test_files_num))
print()

batch_size = 100  # 한번에 뽑아올 파일 개수

with tf.device('/cpu:0'):
	# queue runner를 위한 사전 준비
	filename_queue1 = tf.train.string_input_producer(
	    train_files, shuffle=False, name='filename_queue1')
	reader1 = tf.TFRecordReader()
	key1, value1 = reader1.read(filename_queue1)
	xy1 = tf.parse_single_example(value1, features={'label': tf.FixedLenFeature(
	    [8], tf.float32), 'mfcc': tf.FixedLenFeature([103360], tf.float32)})
	train_x_batch, train_y_batch = tf.train.batch(
	    [xy1['mfcc'], xy1['label']], batch_size=batch_size)

	filename_queue2 = tf.train.string_input_producer(
	    test_files, shuffle=False, name='filename_queue2')
	reader2 = tf.TFRecordReader()
	key2, value2 = reader2.read(filename_queue2)
	xy2 = tf.parse_single_example(value2, features={'label': tf.FixedLenFeature(
	    [8], tf.float32), 'mfcc': tf.FixedLenFeature([103360], tf.float32)})
	test_x_batch, test_y_batch = tf.train.batch(
	    [xy2['mfcc'], xy2['label']], batch_size=batch_size)

	genNum = 8  # 장르 개수
	keep_prob = tf.placeholder(tf.float32)  # dropout 세기 조절용

	X = tf.placeholder(tf.float32, shape=[None, 103360])
	#normalize 과정
	X_min = tf.reduce_min(X)
	X_max = tf.reduce_max(X)
	norm_X = (X - X_min) / (X_max - X_min)
	X_img = tf.reshape(norm_X, [-1, 40, 2584, 1])
	Y = tf.placeholder(tf.float32, shape=[None, genNum])

	with tf.name_scope('layer1') as scope:
	    W1 = tf.Variable(tf.random_normal(
	        [3, 3, 1, 32], stddev=0.1))  # filter size
	    layer1 = tf.nn.conv2d(X_img, W1, strides=[1, 1, 1, 1], padding='SAME')  # convolution
	    layer1 = tf.nn.relu(layer1)  # relu
	    layer1 = tf.nn.max_pool(layer1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')  # max pooling

	    w1_histo = tf.summary.histogram('weights1', W1)
	    layer1_histo = tf.summary.histogram('layer1', layer1)

	with tf.name_scope('layer2') as scope:
	    W2 = tf.Variable(tf.random_normal([3, 3, 32, 32], stddev=0.1))  # filter size
	    layer2 = tf.nn.conv2d(layer1, W2, strides=[1, 1, 1, 1], padding='SAME')  # convolution
	    layer2 = tf.nn.relu(layer2)  # relu
	    layer2 = tf.nn.max_pool(layer2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')  # max pooling

	    w2_histo = tf.summary.histogram('weights2', W2)
	    layer2_histo = tf.summary.histogram('layer2', layer2)

	with tf.name_scope('FullyConnected') as scope:
	    layer2 = tf.reshape(layer2, [-1, 10 * 646 * 32])
	    W = tf.get_variable("W", shape=[10 * 646 * 32, genNum], initializer=tf.contrib.layers.xavier_initializer())
	    b = tf.Variable(tf.random_normal([genNum]))
	    H = tf.nn.softmax(tf.matmul(layer2, W) + b)

	    w_histo = tf.summary.histogram('weights', W)
	    b_histo = tf.summary.histogram('biases', b)
	    hypothesis_histo = tf.summary.histogram('hypothesis', H)

	cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(H), axis=1))
	cost_scalar = tf.summary.scalar('cost', cost)

	optimizer = tf.train.AdamOptimizer(learning_rate=1e-5)  # nan 뜨면 러닝레이트 좀 줄여라
	train = optimizer.minimize(cost)

	prediction = tf.argmax(H, 1)
	correct_prediction = tf.equal(prediction, tf.argmax(Y, 1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
	accuracy_scalar = tf.summary.scalar('accuracy', accuracy)

with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())
	# queue runner 사용할 때 준비해야 하는 것들
	coord = tf.train.Coordinator()
	threads = tf.train.start_queue_runners(coord=coord, sess=sess)

	# tensorboard 관련
	summary = tf.summary.merge_all()
	writer = tf.summary.FileWriter('./logs/CNN_0_0001')
	writer.add_graph(sess.graph)

	totalTestFileNum = test_files_num
	totalTrainingFileNum = train_files_num
	training_epochs = 15  # 에폭 횟수

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
