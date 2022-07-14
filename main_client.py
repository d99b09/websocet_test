#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@author: W_H_J
@license: Apache Licence
@contact: 415900617@qq.com
@software: PyCharm
@file: clicentMqttTest.py
@time: 2019/2/22 14:19
 @describe: клиент mqtt
"""
import json
import sys
import os
import paho.mqtt.client as mqtt
import time

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")

TASK_TOPIC = 'test'  # Клиент публикует тему сообщения

client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
"""
 client_id предназначен для подключения к агенту. Если длина client_id равна нулю или нулю, поведение определяется используемой версией протокола. Если вы используете MQTT v3.1.1,
 Затем на прокси будет отправлен идентификатор клиента нулевой длины, и прокси будет отправлен для генерации случайной переменной для клиента. Если вы используете MQTT v3.1, то идентификатор будет
 Сгенерировано случайным образом. В обоих случаях clean_session должно быть True. Если это не вызывает ValueError в этом случае.
 Примечание. Обычно, если клиентский сервер разрешает два мониторинга, client_id не может совпадать с идентификатором сервера. Например, здесь в качестве идентификатора используется время «20190222142358».
 Если он совпадает с идентификатором сервера, сообщение не может быть получено
"""
client = mqtt.Client(client_id, transport='tcp')

client.connect("127.0.0.1", 1883,
               60)  # Порт здесь по умолчанию 1883, а период активности порта связи по умолчанию равен 60
client.loop_start()


def clicent_main(message: str):
    """
         Сообщение публикации клиента
         : param message: тело сообщения
    :return:
    """
    time_now = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
    payload = {"msg": "%s" % message, "data": "%s" % time_now}
    # опубликовать (Тема: Тема; Содержание сообщения)
    client.publish(TASK_TOPIC, json.dumps(payload, ensure_ascii=False))
    print("Successful send message!")
    return True


if __name__ == '__main__':
    msg = "Я кусок тестовых данных!"
    clicent_main(msg)