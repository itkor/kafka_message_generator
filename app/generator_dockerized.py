from faker import Faker
import time
import datetime
import os
import argparse
from kafka import KafkaProducer
from json import dumps
import signal
import logging, sys


class AppKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_app)
        signal.signal(signal.SIGTERM, self.exit_app)

    def exit_app(self,signum, frame):
        self.kill_now = True

def generate_message(faker=Faker()):
    '''
    Takes faker instance
    Returns dictionary with generated data
    '''
    gen_dct = {
        'basket_price': faker.pricetag(),
        'detectedCorruption': faker.boolean(chance_of_getting_true=5),
        'detectedDuplicate': faker.boolean(chance_of_getting_true=2),
        'eventType': faker.random_choices(elements=('itemViewEvent', 'itemBuyEvent'), length=1),
        'firstInSession': faker.boolean(chance_of_getting_true=4),
        'item_id': faker.pystr(),
        'item_price': faker.pyfloat(left_digits=None, right_digits=2, positive=True, min_value=12.76, max_value=14093.23),
        'item_url': faker.image_url(),
        'location': faker.image_url(),
        'pageViewId': faker.bothify(text='0:????????:???????????????????????'),
        'partyId': faker.bothify(text='0:????????:???????????????????????'),
        'referer': faker.image_url(),
        'remoteHost': faker.bothify(text='test#'),
        'sessionId': faker.bothify(text='0:????????:???????????????????????'),
        'timestamp': time.mktime(datetime.datetime.strptime(faker.date(), "%Y-%m-%d").timetuple()),
        'userAgentName': faker.chrome()
    }
    return gen_dct

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    killer = AppKiller()

    # Parse arguments for data generation
    parser = argparse.ArgumentParser(description='Configure data generator')
    parser.add_argument('address', type=str, default='localhost:9092', metavar='a', help='Kafka broker address') # will be accesible under addr
    parser.add_argument('topic', type=str, default='sessions', help='Kafka topic name') # will be accesible under topic
    parser.add_argument('--num', type=int, default=0, help='Set number of dicts generated') # will be accesible under num

    args = parser.parse_args()
    address = args.address
    topic = args.topic
    num = args.num

    # Initialize Faker library for data synthesizing
    faker = Faker()

    # Initialize Kafka producer
    producer = KafkaProducer(bootstrap_servers=[address],# localhost:9092
                            api_version=(0,11,5),
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    # Message counter
    msg_num = 0

    if num > 0:
        for i in range(num):
            gen_dct = generate_message(faker)
            time.sleep(1)
            producer.send(topic, value=gen_dct)
            logging.info(f'Sent message #{i}')

    elif num == 0:
        while True:
            if killer.kill_now:
                break
            msg_num += 1
            gen_dct = generate_message(faker)
            time.sleep(1)
            producer.send(topic, value=gen_dct)
            logging.info(f'Sent message #{msg_num}')
    else:
        print(f'Incorrect number of messages - should be >= 0. Received instead: {msg_num}')

    logging.info("\n The process is interrupted.")