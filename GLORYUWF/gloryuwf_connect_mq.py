# -*- coding: utf-8 -*-
import socket
import re
import pika
import json

HOST = '192.168.3.7' #TCP server (RS232)
PORT = 8080          #TCP port

MQ_HOST = 'localhost'
MQ_PORT = 5672
MQ_username = 'tssuser'
MQ_password = 'tsstss3801'
MQ_queue_name = 'SCANCOIN'

def publish_to_mq(MQ_HOST,MQ_PORT,MQ_username, MQ_password, MQ_queue_name, str_message):
    
    result = 'Y'
    credentials = pika.PlainCredentials(MQ_username, MQ_password)
    parameters = pika.ConnectionParameters(MQ_HOST,MQ_PORT,'/',credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue=MQ_queue_name,durable = True)
    
    channel.basic_publish(exchange='',routing_key=MQ_queue_name, body= str_message)
    print(" [x] Sent 'Message was published'")
    connection.close()

    return result


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

resultdata = ''
while True:
    #outdata = input('please input message: ')
    #print('send: ' + outdata)
    #s.send(outdata.encode())
    tcpcheck = s.connect_ex((HOST, PORT))
    print('TCP:',tcpcheck)
    if tcpcheck == False:
        s.connect((HOST, PORT))
    
    indata = s.recv(1024)
    print('receving TCP data...')
    if len(indata) == 0: # connection closed
        s.close()
        print('server closed connection.')
        break
    resultdata = resultdata + indata.decode('utf-8')
    #print(resultdata)

    #To identify the result

    content = resultdata

    reg1 = re.compile("[\w|\W]+CUR\. DENOMI\.([\w|\W]+)----------------------------------------[\w|\W]+")
    m = reg1.match(content)

    if m:
        print('MATCH TRANSACTION PATTEN')
        reg2string = "(\w{3}) (\d+)\s+PCS.\s+AMOUNT\s+(\d{1,3}(?:,\d{3})*)|(?:(\w{3}) (\d+)\s+(\d{1,3}(?:,\d{3})*))"
        
        reg2 = re.compile(reg2string)

        m2 = re.findall(reg2string,content)

        
        resultList = []

        #print(m2.groups())
        for i in m2:
            
            if i[0] != '':

                tempdict = {
                'CURRENCY' : i[0],
                'DENOM_FACEVALUE' : i[1],
                'DENOM_QTY' : i[2].replace(',','') 
                }

                resultList.append(tempdict)
            
            else :
                tempdict = {
                'CURRENCY' : i[3],
                'DENOM_FACEVALUE' : i[4],
                'DENOM_QTY' : i[5].replace(',','') 
                }

                resultList.append(tempdict)

        

        dict_publish = { 
            'DENOMS' : resultList,
            'RECEIPT' : resultdata 
        }

        print(dict_publish )
        publish_str_message = json.dumps(dict_publish)
        #publish to rabbitmq
        publish_to_mq(MQ_HOST,MQ_PORT,MQ_username, MQ_password, MQ_queue_name, publish_str_message)

        resultdata = ''
    

    #print('recv: ' + indata.decode())


s.close()       
