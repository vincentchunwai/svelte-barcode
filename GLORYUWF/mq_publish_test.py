import socket
import re
import pika
import json
import sys

#HOST = '192.168.3.7' #TCP server (RS232)
#PORT = 8080          #TCP port

MQ_HOST = 'localhost'
MQ_PORT = 5672
MQ_username = 'tssuser'
MQ_password = 'tsstss3801'
MQ_queue_name = 'SCANCOIN'


f = open('test8_withCNY.txt','r')

content = f.read()


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

    

    dict_publish = { 'DENOMS' : resultList }

    print(dict_publish )


    credentials = pika.PlainCredentials(MQ_username, MQ_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost',port=5672,virtual_host='/', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=MQ_queue_name,durable = True)

    publish_str_message = json.dumps(dict_publish)
    str_message = publish_str_message
    channel.basic_publish(exchange='',routing_key=MQ_queue_name, body= str_message)
    print(" [x] Sent 'Message was published'")


connection.close()
