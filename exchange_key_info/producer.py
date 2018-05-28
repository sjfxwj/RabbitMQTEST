#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


#生产消息的时候也需要带有关键字:注意body里面不必须带有error关键字.
channel.basic_publish(exchange='direct_logs',routing_key='error',body='abc')


connection.close()



