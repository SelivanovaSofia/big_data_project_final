from confluent_kafka import Consumer
import sys
import json
from pymongo import MongoClient
from confluent_kafka.cimpl import KafkaException, KafkaError


class CianConsumer:
    def __init__(self):
        self.conf = {
            'bootstrap.servers': 'localhost:9093',
            'enable.auto.commit': False,
            'group.id': 'test_total',
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(self.conf)
        self.running = True

    def set_data(self, data, topic):
        self.id = int(data['id'])
        self.creation_date = data['creationDate']
        self.city = topic
        self.added_timestamp = data['addedTimestamp']

        if ('totalArea' in data) and (data['totalArea'] != None):
            self.total_area = float(data['totalArea'])
        else:
            self.total_area = 0.0

        if ('livingArea' in data) and (data['livingArea'] != None):
            self.living_area = float(data['livingArea'])
        else:
            self.living_area = 0.0

        if ('kitchenArea' in data) and (data['kitchenArea'] != None):
            self.kitchen_area = float(data['kitchenArea'])
        else:
            self.kitchen_area = 0.0

        if ('floorNumber' in data) and (data['floorNumber'] != None):
            self.floor_number = int(data['floorNumber'])
        else:
            self.floor_number = 0

        if ('building' in data) and (data['building'] != None):
            if ('floorsCount' in data['building']) and (data['building']['floorsCount'] != None):
                self.floors_count = data['building']['floorsCount']
            else:
                self.floors_count = 0

            if ('passengerLiftsCount' in data['building']) and (data['building']['passengerLiftsCount'] != None):
                self.passenger_elevators = data['building']['passengerLiftsCount']
            else:
                self.passenger_elevators = 0

            if ('cargoLiftsCount' in data['building']) and (data['building']['cargoLiftsCount'] != None):
                self.cargo_elevators = data['building']['cargoLiftsCount']
            else:
                self.cargo_elevators = 0

            if ('materialType' in data['building']) and (data['building']['materialType'] != None):
                self.material_of_building = data['building']['materialType']
            else:
                self.material_of_building = 'Not specified'

        else:
            self.floors_count = 0
            self.passenger_elevators = 0
            self.cargo_elevators = 0
            self.material_of_building = 'Not specified'

        if ('bargainTerms' in data) and (data['bargainTerms'] != None):
            if ('clientFee' in data['bargainTerms']) and (data['bargainTerms']['clientFee'] != None):
                self.client_fee = data['bargainTerms']['clientFee']
            else:
                self.client_fee = 0

            if ('priceType' in data['bargainTerms']) and (data['bargainTerms']['priceType'] != None):
                self.price_type = data['bargainTerms']['priceType']
            else:
                self.price_type = 'Not specified'

            if ('paymentPeriod' in data['bargainTerms']) and (data['bargainTerms']['paymentPeriod'] != None):
                self.payment_period = data['bargainTerms']['paymentPeriod']
            else:
                self.payment_period = 'Not specified'

            if ('deposit' in data['bargainTerms']) and (data['bargainTerms']['deposit'] != None):
                self.deposit = data['bargainTerms']['deposit']
            else:
                self.deposit = 0

            if ('agentFee' in data['bargainTerms']) and (data['bargainTerms']['agentFee'] != None):
                self.agent_fee = data['bargainTerms']['agentFee']
            else:
                self.agent_fee = 0

            if ('priceRur' in data['bargainTerms']) and (data['bargainTerms']['priceRur'] != None):
                self.price = data['bargainTerms']['priceRur']
            else:
                self.price = 0

        else:
            self.client_fee = 0
            self.price_type = 'Not specified'
            self.payment_period = 'Not specified'
            self.deposit = 0
            self.agent_fee = 0
            self.price = 0

        if ('bedroomsCount' in data) and (data['bedroomsCount'] != None):
            self.bed_rooms_count = data['bedroomsCount']
        else:
            self.bed_rooms_count = 0

        if ('dealType' in data) and (data['dealType'] != None):
            self.deal_type = data['dealType']
        else:
            self.deal_type = 'Not specified'

        if ('flatType' in data) and (data['flatType'] != None):
            self.flat_type = data['flatType']
        else:
            self.flat_type = 'Not specified'

        if ('category' in data) and (data['category'] != None):
            self.category = data['category']
        else:
            self.category = 'Not specified'

        if ('hasFairPrice' in data) and (data['hasFairPrice'] != None):
            self.has_fair_price = data['hasFairPrice']
        else:
            self.has_fair_price = True

        if ('user' in data) and (data['user'] != None):
            if ('isAgent' in data['user']) and (data['user']['isAgent'] != None):
                self.is_agent = data['user']['isAgent']
            else:
                self.is_agent = False

            if ('agencyName' in data['user']) and (data['user']['agencyName'] != None):
                self.agency_name = data['user']['agencyName']
            else:
                self.agency_name = 'Not specified'

            if ('companyName' in data['user']) and (data['user']['companyName'] != None):
                self.company_name = data['user']['companyName']
            else:
                self.company_name = 'Not specified'

            if ('isSelfEmployed' in data['user']) and (data['user']['isSelfEmployed'] != None):
                self.is_self_employed = data['user']['isSelfEmployed']
            else:
                self.is_self_employed = False
        else:
            self.is_agent = False
            self.agency_name = 'Not specified'
            self.company_name = 'Not specified'
            self.is_self_employed = False

    def filterjson(self, key, topic, data):
        self.set_data(data, topic)
        cluster = MongoClient(
            'mongodb://user:password@localhost:27017/?authMechanism=DEFAULT&readPreference=primary&directConnection=true')
        db = cluster.test
        collection = db['my_collection_test']
        collection.insert_one({
            'id': self.id,
            'creation_date': self.creation_date,
            'city': self.city,
            'total_area': self.total_area,
            'living_area': self.living_area,
            'kitchen_area': self.kitchen_area,
            'floor_number': self.floor_number,
            'floors_count': self.floors_count,
            'passenger_elevators': self.passenger_elevators,
            'cargo_elevators': self.cargo_elevators,
            'material_of_building': self.material_of_building,
            'location': {'type': 'Point', 'coordinates': [data['geo']['coordinates']['lng'], data['geo']['coordinates']['lat']]},
            'addedTimestamp': self.added_timestamp,
            'client_fee': self.client_fee,
            'price_type': self.price_type,
            'payment_period': self.payment_period,
            'deposit': self.deposit,
            'agent_fee': self.agent_fee,
            'price': self.price,
            'bed_rooms_count': self.bed_rooms_count,
            'deal_type': self.deal_type,
            'flat_type': self.flat_type,
            'category': self.category,
            'has_fair_price': self.has_fair_price,
            'published_by_agent': self.is_agent,
            'agency_name': self.agency_name,
            'companyName': self.company_name,
            'is_self_employed': self.is_self_employed
        })

    def basic_consume_loop(self, consumer, topics):
        try:
            consumer.subscribe(topics)
            print('subscribe to topic: ' + topics[0])
            count = 0
            while self.running:
                print('polling...')
                count += 1
                msg = consumer.poll(timeout=15.0)
                if msg is None:
                    print('No More Messages')
                    consumer.close()
                    break

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    data = json.loads(msg.value())
                    key = msg.key()
                    self.filterjson(key, topics[0], data)
                    print('message', count, 'sended to mongoDB')
        finally:
            # Close down consumer to commit final offsets.
            consumer.close()

    def shutdown(self):
        running = False


topics = ['SAINT_PETERSBURG']


def main():
    cian_consumer = CianConsumer()
    cian_consumer.basic_consume_loop(cian_consumer.consumer, topics)


if __name__ == "__main__":
    main()
