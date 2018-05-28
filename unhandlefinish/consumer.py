#!/usr/bin/python
# -*- coding:utf-8 -*-


#消费者在消费的过程当中报错怎么处理?===>将消息取出来了,但是没有消费成功,这就很尴尬了.
#如果我们的消息没有处理成功,我们应该将消息继续放到队列当中去,如果做完了,就告诉一下.
#**即如果出现异常,没有将消息处理完毕,我们就应该将消息重新放回到队列当中去.

"""
acknowledgment 消息不丢失（sure）
no-ack ＝ False，如果消费者遇到情况(its channel is closed, connection is closed, 
or TCP connection is lost)挂掉了，那么，RabbitMQ会重新将该任务添加到队列中。
发送一个完成的信号:如果没有完成,则消息仍然在队列里面. ===>未处理完成,将消息在重新放回到队列当中.
"""

import pika


conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = conn.channel()


def callback(ch,method,properties,body):
    print('[x] Received %r'%body)
    import time
    time.sleep(10)
    print('OK')
    ch.basic_ack(delivery_tag=method.delivery_tag)  #第二:每一次消费完成将消息信号发送一下:这样消费者消费完消息之后,
    #才会将消息从队列里面干掉。


channel.basic_consume(callback,
                      queue='hello1',  #指定从哪个队列里面消费数据.
                      no_ack=False     #第一:这里设置一下
                      )

channel.start_consuming() #开始消费(有数据,直接执行回调函数,没有数据,就阻塞住.)









