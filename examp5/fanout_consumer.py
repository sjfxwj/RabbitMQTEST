#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import time

#消费者进行消息的订阅

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  #建立连接
channel = connection.channel()  #建立管道

channel.exchange_declare(exchange='logs',type='fanout')

result = channel.queue_declare(exclusive=True)   #独有的,拍他的,唯一的.(消费者在这里声明一个Queue,)
queue_name = result.method.queue  #不指定Queue的名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除.
#即随机生成一个带名字的queue,并且后续会自动删除. ==>result是Queue对象,名字:result.method.queue

print('\03342m队列的名字是:%s\033[0m'%queue_name)

channel.queue_bind(exchange='logs',queue=queue_name)   #将队列queue绑定到指定的转发器

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()













