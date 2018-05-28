#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',type='fanout')  #如果exchange已经存在,则不用进行声明

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue  #随机生成一个队列,并且队列的名字是随机的.

channel.queue_bind(exchange='logs',queue=queue_name)  #将队列与exchange进行绑定.

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()



