from time import sleep
from json import dumps
from kafka import KafkaProducer

# 로컬 Kafka 인스턴스를 연결하는 KafkaProducer 객체 생성
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],   # Broker 중 하나 이상을 지정
    value_serializer=lambda x: dumps(x).encode('utf-8') # serialization 방법 정의
)

for j in range(50):
    print("iteration:", j)
    data = {'counter': j}
    producer.send('topic_test', value=data)
    sleep(0.5)