#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',type='direct')

# 将这个队列绑定到exchange.#将队列绑定到exchange的关键字
channel.queue_bind(exchange='direct_logs',queue='queue4',routing_key='error')
channel.queue_bind(exchange='direct_logs',queue='queue4',routing_key='info')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,queue='queue4')

channel.start_consuming()