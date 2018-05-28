#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',type='fanout')  #如果exchange已经存在,则不用进行声明
channel.queue_bind(exchange='logs',queue='queue2')       #将队列queue2与exchange进行绑定.

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(callback,queue='queue2')
channel.start_consuming()