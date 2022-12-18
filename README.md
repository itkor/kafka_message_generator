# Kafka message generator

A simple Kafka message producer. The messages are generated with Faker library and imitate session activities.

The format of the message:  
>{  
        'basket_price': float,  
        'detectedCorruption': boolean,    
        'detectedDuplicate': boolean,  
        'eventType': String,  
        'firstInSession': boolean,  
        'item_id': String,  
        'item_price': float,  
        'item_url': String,  
        'location': String,  
        'pageViewId': String,  
        'partyId': String,  
        'referer': String,  
        'remoteHost': String,  
        'sessionId': String,  
        'timestamp': datetime ("%Y-%m-%d"),  
        'userAgentName': String  
    }
      
Message example:  
>{  
        "basket_price": "$549.95",   
        "detectedCorruption": false,   
        "detectedDuplicate": false,   
        "eventType": ["itemViewEvent"],   
        "firstInSession": false,   
        "item_id": "ZQqKSsbfkOapBGidwYJi",   
        "item_price": 2433.7,   
        "item_url": "https://dummyimage.com/672x983",   
        "location": "https://picsum.photos/137/238",   
        "pageViewId":"0:tATUTakx:BGRPgipcOxWxRkcuOdMgUnY",   
        "partyId": "0:FJnXyLax:QhpGQGiGMTmdGJigHbRGPJA",   
        "referer": "https://placekitten.com/188/915",   
        "remoteHost": "test4",   
        "sessionId": "0:NRwvKgPH:tfKbpfhkkYogejrrSWnvgzx",   
        "timestamp": 1063238400.0,   
        "userAgentName": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.0 (K
        HTML, like Gecko) Chrome/46.0.855.0 Safari/536.0"  
      }  
***
**How to launch:**

1) Run Kafka (Wurstmeister's - https://github.com/wurstmeister/kafka-docker)

> The topic is created automatically - "sessions" (1 partition, 2
> replicas)

    cd *your_path*/kafka_message_generator
    docker-compose up  

2) Build the generator's image

`   docker build -t kafka_msg_gen:0.0.1 ./app`

3) Run container

   Parameters for the generator:
>  - address - Kafka address. Default - 'localhost:9092'
>  - topic - Kafka topic name. Default - 'test'
>  - --num - Number of messages to send. Default - 0 means limitless continuous flow of messages

    docker run -it --init --rm --network host  kafka_msg_gen:0.0.1 generator_dockerized.py 0.0.0.0:9092 sessions --num=0

**Controls:**

Ctrl-C to interrupt message generator
