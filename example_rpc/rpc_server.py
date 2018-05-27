#!/usr/bin/python
# -*- coding:utf-8 -*-


import pika
import time

#客户端将消息发送到了rpc,我的服务端要从rpc接受消息.
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')   #声明一个RPC_queue


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body): #回调函数（先受到消息,然后执行命令,最后在返回结果.）
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)   #执行命令.(在这里搞.)

    #服务器端要将结果返回给谁:如果不约定,服务器端永远不知道将消息要发给谁.(将Queue写死也可以,但是不太好.)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,  #拿到客户端随机生成的Queue,将消息返回给了客户端.
                     properties=pika.BasicProperties(correlation_id= props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)  #确保消息完成.


channel.basic_qos(prefetch_count=1)  #公平调度,没什么用.
channel.basic_consume(on_request, queue='rpc_queue')    #从队列里面接受消息,一旦受到消息,调用on_request回调函数.

print(" [x] Awaiting RPC requests")
channel.start_consuming()