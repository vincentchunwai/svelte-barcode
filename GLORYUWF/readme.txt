#
pm2 start gloryuwf_connect_mq.py --name 01_GLORYUWF_CONNECT --interpreter python3 -o /dev/null -e /dev/null

MQ_HOST = 'localhost'
MQ_PORT = 5672
MQ_username = 'tssuser'
MQ_password = 'tsstss3801'
MQ_queue_name = 'SCANCOIN'



RabbitMQ Management
localhost:15672
username: admin
password: admin
