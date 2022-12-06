import json
import cloudscraper
from colorama import Fore
from kafka import KafkaProducer
import time

from utils.type_of_task import TypeOfTask
from utils.type_real_state import TypeRealState
from utils.region import Region
from utils.type_room import TypeRoom

class Parser:
    def __init__(self):
        pass
    
    def setParser(self, region, type_real_state, type_of_task, room):
        self.type_of_task = type_of_task
        self.url = "https://api.cian.ru/search-offers/v1/search-offers-desktop/"
        self.engine_version = {"type": "term", "value": 2}
        self.type = type_real_state
        self.region = {"type": "terms", "value": [region]}
        self.room = {"type": "terms", "value": [room]}
        self.scraper = cloudscraper.create_scraper(disableCloudflareV1=True, browser={
            'browser': 'firefox',
            'platform': 'darwin',
            'desktop': True,
            
        }, interpreter='nodejs', allow_brotli=False)

    def parse(self, page):
        if (self.type_of_task == TypeOfTask.FROM_BEGINING):
            return self.parse_FROM_BEGINING(page)
        else:
            return self.parse_LAST_DAY(page)

    def parse_FROM_BEGINING(self, page):
        print(Fore.CYAN + "INFO: Parsing from beginning\nCurrent page: " + str(page))
        payload = json.dumps({
            "jsonQuery":
            {
                "_type": self.type,
                "engine_version": self.engine_version,
                "region": self.region,
                "room": self.room,
                "page": {"type": "term", "value": page}
            }
        })
        response = self.scraper.post(
            "https://api.cian.ru/search-offers/v2/search-offers-desktop/", payload)
        if (response.status_code == 200):
            response = json.loads(response.text)
            data = response['data']
            offers = data['offersSerialized']
            ret = json.dumps(offers, ensure_ascii=False)
            print(Fore.GREEN + "SUCCESS: STATUS 200")
            return ret
        else:
            print(Fore.RED + "ERROR: NOT STATUS CODE 200!")
            return -1

    def parse_LAST_DAY(self, page):
        print(Fore.CYAN + "INFO: Update current day\nCurrent page: " + str(page))
        payload = json.dumps({
            "jsonQuery":
            {
                "_type": self.type,
                "engine_version": self.engine_version,
                "region": self.region,
                "publish_period": {"type": "term", "value": -2},
                "room": self.room,
                "page": {"type": "term", "value": page}
            }
        })
        response = self.scraper.post(
            "https://api.cian.ru/search-offers/v2/search-offers-desktop/", payload)
        if (response.status_code == 200):
            response = json.loads(response.text)
            data = response['data']
            offers = data['offersSerialized']
            ret = json.dumps(offers, ensure_ascii=False)
            print(Fore.GREEN + "SUCCESS: STATUS 200")
            return ret
        else:
            print(Fore.RED + "ERROR: NOT STATUS CODE 200!")
            return -1

    def messages(self):
        print(Fore.LIGHTYELLOW_EX + """
       ___ _                 ___                         
      / __(_) __ _ _ __     / _ \__ _ _ __ ___  ___ _ __ 
     / /  | |/ _` | '_ \   / /_)/ _` | '__/ __|/ _ \ '__|
    / /___| | (_| | | | | / ___/ (_| | |  \__ \  __/ |   
    \____/|_|\__,_|_| |_| \/    \__,_|_|  |___/\___|_|   
                                                        
    """)
        print(Fore.LIGHTYELLOW_EX + "Developed by:")
        print(Fore.LIGHTYELLOW_EX + "   - Sofia")
        print(Fore.LIGHTYELLOW_EX + "   - Denis")
        print(Fore.LIGHTYELLOW_EX + "   - Danilo\n")
        print(Fore.WHITE + "Dont forget configure the parser correctly\n")
    
    def start(self, task):
        type_of_task = TypeOfTask.UPDATE
        print(task)
        if(task == 'initial'):
            type_of_task = TypeOfTask.FROM_BEGINING
            
        regions = [Region.MOSCOW, Region.SAINT_PETERSBURG, Region.KRASNODAR, Region.SAMARA, Region.NOVOSIBIRSK, Region.KAZAN, Region.SARATOV, Region.OMSK, Region.TOMSK, Region.SOCHI]
        real_state_types = [TypeRealState.FLAT_RENT, TypeRealState.FLAT_SALE]
        for real_state_type in real_state_types:
            for region in regions:
                tasks = []
                if (real_state_type == TypeRealState.FLAT_RENT):
                    tasks = [TypeRoom.ONE_ROOM, TypeRoom.TWOO_ROOM,
                            TypeRoom.THREE_ROOM, TypeRoom.STUDIO, TypeRoom.ROOM_IN_APARTMENT]
                else:
                    tasks = [TypeRoom.ONE_ROOM, TypeRoom.TWOO_ROOM, TypeRoom.THREE_ROOM,
                            TypeRoom.STUDIO, TypeRoom.ROOM_IN_APARTMENT, TypeRoom.FREE_PLAN]

                self.messages()
                producer = KafkaProducer(bootstrap_servers=['localhost:9093'])
                print(Fore.LIGHTCYAN_EX + "The current configuration is:")
                print(Fore.LIGHTWHITE_EX + "   - Region: " + region.name)
                print(Fore.LIGHTWHITE_EX + "   - Type of real state: " + real_state_type.name)
                print(Fore.LIGHTWHITE_EX + "   - Type of task: " + type_of_task.name)

                print(Fore.LIGHTYELLOW_EX + "\n\nStarting bot ...")
                for task in tasks:
                    print("\n\n")
                    self.setParser(region, real_state_type, type_of_task, task)
                    page = 1
                    while (True):
                        result = json.loads(self.parse(page))

                        if (len(result) > 0):
                            for r in result:
                                msg = json.dumps(r, ensure_ascii=False)
                                key = r['id']
                                producer.send(region.name, key=str.encode(str(key)), value=str.encode(msg))
                            print(Fore.CYAN + "INFO: Starting sending data to kafka from task "+task.name)
                        else:
                            print(Fore.CYAN + "INFO: Task "+task.name + " finished")
                            break
                        time.sleep(2)
                        page += 1