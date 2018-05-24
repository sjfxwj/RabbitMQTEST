#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  #建立连接
channel = connection.channel()  #建立管道


#You may ask why we declare the queue again ‒ we have already declared it in our previous code.
# We could avoid that if we were sure that the queue already exists. For example if send.py program
#was run before. But we're not yet sure which program to run first. In such cases it's a good
# practice to repeat declaring the queue in both programs.
channel.queue_declare(queue='hello2')  #声明从哪个队列里面收消息(既然队列已经被生产者声明了,为什么我还要声明呢?)

def callback(ch,method,properties,body):  #回调函数(事件一触发,立即调用一个函数)
    print("-->",ch,method,properties)
    time.sleep(3)
    print("[x] Received %r "%body)
    ch.basic_ack(delivery_tag=method.delivery_tag)   #传送标签

#函数执行完了,就代表消息处理完毕了,函数没执行完,就代表消息没有处理完.==>任务没执行完,就丢了??

"""
--> <BlockingChannel impl=<Channel number=1 OPEN conn=<SelectConnection OPEN socket=('127.0.0.1', 38530)->('127.0.0.1', 5672) params=<ConnectionParameters host=localhost port=5672 virtual_host=/ ssl=False>>>> <Basic.Deliver(['consumer_tag=ctag1.e608b73ec97c4504accc7c3295613adb', 'delivery_tag=1', 'exchange=', 'redelivered=False', 'routing_key=hello'])> <BasicProperties>
"""

channel.basic_consume( #消费消息
                      callback,        #如果收到消息,就调用callback回调函数来处理消息.
                      queue='hello2',  #从哪个队列里面收消息
                      #no_ack=True     #先忽略 no acknowledgement(不管消息,消费者处理完了,还是没有处理完毕,都不会和生产者进行确认.),RabbitMq默认消息处理完毕之后,不会进行消息的确认,需要通过ch.basic_ack(delivery_tag=method.delivery_tag)进行确认.
                      )
"""
consumer_callback(channel, method, properties, body)
channel: BlockingChannel
method: spec.Basic.Deliver
properties: spec.BasicProperties
body: str or unicode
只要没有确认,rabbitmq就不会将这条消息删除掉.
消费者突然断了,rabbitmq就自动将这条消息转发给其他的消费者.（socket断了.）
总结:生产者发送一个消息,被消费者接受到了,消费者处理完消息之后,会自动的给生产者发送一个
确认消息,告诉生产者消息处理完毕,随后生产者才会将这条消息从队列里面进行删除，只要没有收到确认,
就不会将这条消息进行删除,一旦消费者在处理消息期间出现故障,rabbitmq会自动将该条消息转发给其他的
消费者.
"""


print('[*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()   #开始收消息,如果没有消息,将一直阻塞住.


