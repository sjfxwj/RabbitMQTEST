#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
从windows连接虚拟机的rabbitmq的时候:需要输入用户名和密码,rabbitmq如何配置用户名和密码?
一个生产者如何对应多个消费者?

**默认情况下rabbitMQ采用消息轮询的方式将消息依次分发给消费者**

消费者如何给生产者发送一个消息代表消息确实已经消费完呢?(宕机怎么办呢?)
只有处理完之后,生产者才会将任务从队列当中删除,
只要没有确认,就代表消息没有处理完.
"""

import pika


#pika.exceptions.ConnectionClosed: Connection to 127.0.0.1:5672 failed: timeout
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()  #声明一个管道

#声明一个Queue,Queue的名字为'hello'
channel.queue_declare(queue='hello3',durable=True)
#仅仅是将队列进行了持久化,但是消息并没有进行持久化.


channel.basic_publish(exchange='',
                      routing_key='hello3',  #Queue的名字:即将消息发送到这个Queue里面
                      body='Hello World',
                      properties=pika.BasicProperties(
                          delivery_mode=2,   #make message persistent  #将消息进行持久化.
                      ))   #消息的内容

print("[x] Sent 'Hello World!'")
connection.close()  #不是将管道关闭,而是将队列关闭???


"""
rabbitmq内部是可以存放很多队列的,如何查看rabbitmq内部已经存放多少队里了呢?

 rabbitmqctl（控制器）:
 rabbitmq-plugins
 rabbitmq-server
[root@hadoop11 sbin]# pwd
/sbin

[root@hadoop11 examp2]# rabbitmqctl list_queues
Listing queues ...
hello   1
hello2  2(处理完为什么还要两个啊?)待定.....
...done.
"""

