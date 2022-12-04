from faker import Faker
import time
import datetime
import argparse
from kafka import KafkaProducer
from json import dumps

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

def main():
    '''
    Receives arguments:
        address - Kafka address. Default - 'localhost:9092'
        topic - Kafka topic name. Default - 'test'
        --num - Number of messages to send. Default - 0. 0 means limitless continuous flow of messages
    Sends messages in dictionaries into the
    '''

    # Parse arguments for data generation
    parser = argparse.ArgumentParser(description='Configure data generator')
    parser.add_argument('address', type=str, default='localhost:9092', metavar='a', help='Kafka broker address') # will be accesible under args.addr
    parser.add_argument('topic', type=str, default='test', help='Kafka topic name') # will be accesible under args.topic
    parser.add_argument('--num', type=int, default=0, help='Set number of dicts generated') # will be accesible under args.num
    args = parser.parse_args()

    # Initialize Faker library for data synthesizing
    faker = Faker()

    # Initialize Kafka producer
    producer = KafkaProducer(bootstrap_servers=[args.address], # localhost:9092
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    # Message counter
    msg_num = 0

    if args.num > 0:
        for i in range(args.num):
            gen_dct = generate_message(faker)
            time.sleep(0.25)
            producer.send(args.topic, value=gen_dct)
            print(f'Sent message #{i}')
    elif args.num == 0:
        while True:
            msg_num += 1
            gen_dct = generate_message(faker)
            time.sleep(0.25)
            producer.send(args.topic, value=gen_dct)
            print(f'Sent message #{msg_num}')
    else:
        print(f'Incorrect number of messages - should be >= 0. Received instead: {msg_num}')



if __name__ == "__main__":
    main()