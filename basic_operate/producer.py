#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika

conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) #先连接到服务端
channel = conn.channel()  #创建一个频道

channel.queue_declare(queue='queue1')   #创建一个队列
channel.basic_publish(
    exchange='',             #通过修改exchange可以改变rabbitmq的执行模式（通过修改exchange可以将rabbitmq变成redits同样的功能.）
    routing_key='queue1',    #指定向哪个队列里面发送数据
    body='1+1=?'             #发送数据的内容
)


conn.close() #关闭连接















