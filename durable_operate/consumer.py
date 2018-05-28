#!/usr/bin/python
# -*- coding:utf-8 -*-

#有数据,就直接拿过来,没有数据,就直接夯住.

import pika

conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = conn.channel()

# channel.queue_declare(queue='queue1')  #由于队列已经有了,所以可以不用声明.

def callback(ch,method,properties,body):
    """
    :param ch: 
    :param method: 
    :param properties: 
    :param body: 拿到的数据
    :return: 
    """
    print('[x] Received %r'%body)
    #channel.stop_consuming() 消费者停止消费

channel.basic_qos(prefetch_count=1)    #不在在严格按照顺序进行执行,谁空闲,谁来做.
channel.basic_consume(callback,
                      queue='hello1',  #指定从哪个队列里面消费数据.
                      #no_ack=True
                      )

channel.start_consuming() #开始消费(有数据,直接执行回调函数,没有数据,就阻塞住.)