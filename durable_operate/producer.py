#!/usr/bin/python
# -*- coding:utf-8 -*-

#生产者和消费者如何做到数据的持久化操作呢???====>生产数据的时候应该做到数据的持久化操作.


import pika

conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) #先连接到服务端
channel = conn.channel()  #创建一个频道

channel.queue_declare(queue='queue2',durable=True)   #创建一个队列 (如何后期加上的话,queue不能持久化,因为前面的队列已经创建了)
channel.basic_publish(
    exchange='',
    routing_key='queue2',    #指定向哪个队列里面发送数据
    body='1+1=?',             #发送数据的内容
    properties=pika.BasicProperties(
    delivery_mode=2,   ) #将消息进行持久化.  #效果:发送数据之后,服务器关闭,在重启之后,数据还是在的。
)

#注意:持久化肯定是在生产者一方做的.

conn.close() #关闭连接


