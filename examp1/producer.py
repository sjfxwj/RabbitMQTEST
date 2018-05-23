#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika


#pika.exceptions.ConnectionClosed: Connection to 127.0.0.1:5672 failed: timeout
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()  #声明一个管道

#声明一个Queue,Queue的名字为'hello'
channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',  #Queue的名字:即将消息发送到这个Queue里面
                      body='Hello World')   #消息的内容

print("[x] Sent 'Hello World!'")
connection.close()  #不是将管道关闭,而是将队列关闭???






