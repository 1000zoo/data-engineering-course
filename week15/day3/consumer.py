from kafka import KafkaConsumer
from json import loads
from time import sleep

consumer = KafkaConsumer(
    'topic_test',   # 소비할 Topic 이름
    bootstrap_servers=['localhost:9092'],   # 연결할 Broker 선택
    auto_offset_reset='earliest',   # earliest vs latest (가장 오래된 offset vs 가장 최근 offset)
    enable_auto_commit=True,    # 사용중인 offset 값을 Kafka 내부에 자동으로 기록, False의 경우, commit 함수로 명시적으로 커밋
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))   # deserialization
)

for event in consumer:
    event_data = event.value
    print(event_data)
    sleep(1)