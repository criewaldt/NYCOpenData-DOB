import requests, json, csv
import os

from config.settings import OPENDATA_APP_TOKEN
APP_TOKEN = os.getenv("OPENDATA_APP_TOKEN") or OPENDATA_APP_TOKEN

def pprint(json_item):
    print(json.dumps(json_item, indent=4))

OPENDATA_URLS = {
    "complaints" : "https://data.cityofnewyork.us/resource/eabe-havv.json",
    "ecb" : "https://data.cityofnewyork.us/resource/6bgk-3dad.json",
    "violations" : "https://data.cityofnewyork.us/resource/3h2n-5cm9.json",
    "now" : "https://data.cityofnewyork.us/resource/w9ak-ipjd.json",
    "bis" : "https://data.cityofnewyork.us/resource/ic3t-wcy2.json",
    "sign": "https://data.cityofnewyork.us/resource/nyis-y4yr.json",
    "cofo": "https://data.cityofnewyork.us/resource/bs8b-p36w.json",
}

class GetBin():
    def __init__(self, bin_number):
        self.bin_number = bin_number

        self.bis_jobs = self.bis()
        self.now_jobs = self.now()
        self.sign_jobs = self.sign()

        self.violations = self.violations()
        self.ecb = self.ecb()
        self.complaints = self.complaints()
        self.info = self.info()

        self.cofo = self.cofo()

    def info(self, ):
        address_list = []
        block_list = []
        lot_list = []

        for a in self.now_jobs:
            address = " ".join([a["house_no"], a["street_name"]])
            block = a["block"].lstrip("0")
            lot = a["lot"].lstrip("0")
            if address not in address_list:
                address_list.append(address)
            if block not in block_list:
                block_list.append(block)
            if lot not in lot_list:
                lot_list.append(lot)

        for a in self.bis_jobs:
            address = " ".join([a["house__"], a["street_name"]])
            block = a["block"].lstrip("0")
            lot = a["lot"].lstrip("0")
            if address not in address_list:
                address_list.append(address)
            if block not in block_list:
                block_list.append(block)
            if lot not in lot_list:
                lot_list.append(lot)
            
        data = {
                "address_list" : set(address_list),
                "block_list" : block_list,
                "lot_list" : lot_list,
            }
        return data
    
    def complaints(self, ):
        url = "https://data.cityofnewyork.us/resource/eabe-havv.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "bin" : "{}".format(self.bin_number),
            }
        r = requests.get(url, params=payload)
        return r.json()
    
    def ecb(self, ):
        url = "https://data.cityofnewyork.us/resource/6bgk-3dad.json"
        payload = {
            "$$app_token" : APP_TOKEN,
            "bin" : "{}".format(self.bin_number),
            #"$q" : "active"
            }
        r = requests.get(url, params=payload)
        return r.json()
    
    
    def violations(self, ):
        url = "https://data.cityofnewyork.us/resource/3h2n-5cm9.json"
        payload = {
            "$$app_token" : APP_TOKEN,
            "bin" : "{}".format(self.bin_number),
            #"$q" : "active"
            }
        r = requests.get(url, params=payload)
        return r.json()
    
    def now(self, ):
        url = "https://data.cityofnewyork.us/resource/w9ak-ipjd.json"
        payload = {
            "$$app_token" : APP_TOKEN,
            "bin" : "{}".format(self.bin_number)
            }
        r = requests.get(url, params=payload)
        return r.json()
    
    def bis(self, ):
    
        url = "https://data.cityofnewyork.us/resource/ic3t-wcy2.json"
        payload = {
            "$$app_token" : APP_TOKEN,
            "bin__" : "{}".format(self.bin_number)
            }
        r = requests.get(url, params=payload)
        return r.json()

    def sign(self):
        url = "https://data.cityofnewyork.us/resource/nyis-y4yr.json"
        payload = {
            "$$app_token" : APP_TOKEN,
            "bin__": "{}".format(self.bin_number)          
            }
        r = requests.get(url, params=payload)
        return r.json()

    def cofo(self, ):
        url = "https://data.cityofnewyork.us/resource/bs8b-p36w.json"
        payload = {
            "$$app_token" : APP_TOKEN,
            "bin" : "{}".format(self.bin_number),
            }
        r = requests.get(url, params=payload)
        return r.json()

if __name__ == "__main__":
    #binData = GetBin("1084455")
    #d = GetBlockLot(520, 56)
    pass