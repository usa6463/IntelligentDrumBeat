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

batch_size = 100  # 한번에 뽑아올 파일 개수

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

# train Parameters
seq_length = 2584 # (None, seq_length, data_dim)
data_dim = 40
hidden_dim = 80 # cell에서 몇개의 값이 나올지 정하는 변수. 
output_dim = 8 # fully connected 거치고 나오는 변수의 개수. 
learning_rate = 0.01 
iterations = 500    
genNum = 8  # 장르 개수

X = tf.placeholder(tf.float32, shape=[None, 103360])
#normalize 과정
X_min = tf.reduce_min(X)
X_max = tf.reduce_max(X)
norm_X = (X - X_min) / (X_max - X_min)
X_img = tf.reshape(norm_X, [-1, seq_length, data_dim]) # none, seq_length, data_dim
Y = tf.placeholder(tf.float32, shape=[None, output_dim])

cell = tf.contrib.rnn.BasicLSTMCell(
    num_units=hidden_dim, state_is_tuple=True, activation=tf.tanh)
outputs, _states = tf.nn.dynamic_rnn(cell, X_img, dtype=tf.float32) # 1 100 2584 hidden_dim
# Y_pred = tf.contrib.layers.fully_connected( # 1, 100, 8
#     outputs[:, -1], output_dim, activation_fn=None)  # We use the last cell's output

outputs = tf.slice(outputs, [0,2583,0], [100,1,hidden_dim])
outputs = tf.reshape(outputs, [-1, hidden_dim])
W = tf.get_variable("W", shape=[hidden_dim, genNum], initializer=tf.contrib.layers.xavier_initializer())
b = tf.Variable(tf.random_normal([genNum]))
H = tf.nn.softmax(tf.matmul(outputs, W) + b)

# cost/loss
loss = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(H), axis=1))
# optimizer
optimizer = tf.train.AdamOptimizer(learning_rate)
train = optimizer.minimize(loss)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    # queue runner 사용할 때 준비해야 하는 것들
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord, sess=sess)
    
    totalTestFileNum = test_files_num
    totalTrainingFileNum = train_files_num
    training_epochs = 5  # 에폭 횟수

    batch_xs, batch_ys = sess.run([train_x_batch, train_y_batch])
    batch_xs = np.array(batch_xs).reshape(-1, 40, 2584)
    print(batch_xs.shape)
    batch_xs = np.swapaxes(batch_xs, 1, 2)
    print(batch_xs.shape)
    batch_xs = batch_xs.reshape(-1, 103360)

    print('훈련 시작, 총 에폭 수 : {}, 배치 크기 : {}'.format(training_epochs, batch_size))
    avg_cost = 0
    for epoch in range(training_epochs):
        total_batch = int(totalTrainingFileNum / batch_size)

        for i in tqdm(range(total_batch)):
            batch_xs, batch_ys = sess.run([train_x_batch, train_y_batch])
            _, c = sess.run([train, loss], feed_dict= {X:batch_xs, Y:batch_ys})
            avg_cost += c / total_batch

        print('epoch : %04d'%(epoch+1), 'cost : %09f'%avg_cost)

    # for quere runner
    coord.request_stop()
    coord.join(threads)
