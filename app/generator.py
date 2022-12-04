from faker import Faker
import time
import datetime
import argparse
from kafka import KafkaProducer
from json import dumps

def main():
    '''
    python generator.py localhost:9092 test --num=25

    {
    "basket_price":"",
    "detectedCorruption":false,
    "detectedDuplicate":false,
    "eventType":"itemViewEvent",
    "firstInSession":true,
    "item_id":"bx_xjMvKPct_FPvmYjZWcXzfFVCIYzxrDozDkLTTTkKL",
    "item_price":6409,"item_url":"https:\/\/b24-mu3bxs.bitrix24.shop\/\/katalog\/item\/dress-red-fairy\/",
    "location":"https:\/\/b24-mu3bxs.bitrix24.shop\/",
    "pageViewId":"0:WPdilZdP:LHUvPXkCoPUlndnWVHqQdAFQsPKBODtS",
    "partyId":"0:MLjKrORs:lrWNQWQtpfqMqPLLbcbmYtndLePeunWJ",
    "referer":"https:\/\/b24-mu3bxs.bitrix24.shop\/\/katalog\/clothes\/t-shirts\/",
    "remoteHost":"test0",
    "sessionId":"0:grgeChCV:GYAvhbZSWvDaUPuYOqcerlzKUxIrbiJF",
    "timestamp":1545141604432,
    "userAgentName":"Mozilla\/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/29.0.1547.57 Safari\/537.36"
    }
    :return:
    '''

    # Parse arguments for data generation
    parser = argparse.ArgumentParser(description='Configure data generator')
    parser.add_argument('address', type=str, default='localhost:9092', metavar='a', help='Kafka broker address') # will be accesible under args.addr
    parser.add_argument('topic', type=str, default='test', help='Kafka topic name') # will be accesible under args.topic
    parser.add_argument('--num', type=int, default=5, help='Set number of dicts generated') # will be accesible under args.num
    args = parser.parse_args()

    # Initialize Faker library for data synthesizing
    faker = Faker()


    # Initialize Kafka producer
    producer = KafkaProducer(bootstrap_servers=[args.address], # localhost:9092
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    for i in range(args.num):
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
        time.sleep(0.25)
        producer.send(args.topic, value=gen_dct)
        print(f'Sent message #{i}')




if __name__ == "__main__":
    main()