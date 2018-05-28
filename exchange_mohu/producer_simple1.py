#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',type='topic')

channel.basic_publish(exchange='topic_logs',
                      routing_key='old.info',
                      body='topic_logs')


connection.close()
