#!/usr/bin/python
# -*- coding:utf-8 -*-

#我想让远程的机器给我计算一个斐波那契怎么搞?

import pika
import uuid
import time


class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)#(生成一个随机的Queue在客户端着里面:)
        self.callback_queue = result.method.queue  #生成一个随机Queue,并给Queue起名字.

        self.channel.basic_consume(self.on_response,           #回调函数:即只要一收到消息就调用response.
                                   no_ack=True,
                                   queue=self.callback_queue)  #从这个Queue里面收消息,

    def on_response(self, ch, method, props, body): #?
        if self.corr_id == props.correlation_id:
            self.response = body  #此时self.response不等于None,只要收到消息,self.respoonse改成消息的内容.

    def call(self, n): #客户端在给服务器端发送指令的时候,同时带一条消息,告诉服务端将消息返回给哪个Queue.
        self.response = None
        self.corr_id = str(uuid.uuid4())         #3693006d-ea9e-4976-802d-1dfee9faac6e
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',  #发送一个消息到rpc_queue里面
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,  #告诉服务端处理完消息之后将消息返回到这个Queue里面.
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(n))  #发送的消息,必须传递是字符串.
        while self.response is None:    #发送消息之后就应该收结果???但是我没有写start consumer。
            self.connection.process_data_events()  #不阻塞,有消息或者没有都进行返回.（有消息,就收消息,没消息,就继续往下走.）
            print('no msg')
            time.sleep(0.5)  #如果结果是None,那么我就一直收消息,直到不为None为止.
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)    #调用call()方法,传30进去.
print(" [.] Got %r" % response)