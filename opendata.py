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

TESTING = False

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


"""

class GetBlockLot():
    def __init__(self, block, lot, borough):

        self.borough = borough
        if self.borough == "MANHATTAN":
            self.borough_number = "1"
        elif self.borough == "BROOKLYN":
            self.borough_number = "3"
        elif self.borough == "QUEENS":
            self.borough_number = "4"
        elif self.borough == "BRONX":
            self.borough_number = "2"
        elif self.borough == "STATEN ISLAND":
            self.borough_number = "5"
        self.block = block
        self.lot = lot

        self.bis_jobs = self.bis()
        self.now_jobs = self.now()
        self.violations = self.violations()
        self.ecb = self.ecb()
        self.info = self.info()

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
    

    
    def ecb(self, ):
        url = "https://data.cityofnewyork.us/resource/6bgk-3dad.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "block" : "{}".format(self.block),
            "lot" : "{}".format(self.lot),
            "boro" : "{}".format(self.borough_number),
            
            #"$q" : "active"
            }
        r = requests.get(url, params=payload)
        return r.json()
    
    
    def violations(self, ):
        url = "https://data.cityofnewyork.us/resource/3h2n-5cm9.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "block" : "{}".format(self.block),
            "lot" : "{}".format(self.lot),
            "boro" : "{}".format(self.borough_number),
            #"$q" : "active"
            }
        r = requests.get(url, params=payload)
        return r.json()
    
    def now(self, ):
        url = "https://data.cityofnewyork.us/resource/w9ak-ipjd.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "block" : "{}".format(self.block),
            "lot" : "{}".format(self.lot),
            "borough" : "{}".format(self.borough.upper()),
            }
        r = requests.get(url, params=payload)
        return r.json()
    
    def bis(self, ):
    
        url = "https://data.cityofnewyork.us/resource/ic3t-wcy2.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "block" : "{}".format(self.block.zfill(5)),
            "lot" : "{}".format(self.lot.zfill(5)),
            "borough" : "{}".format(self.borough.upper()),
            }
        r = requests.get(url, params=payload)
        return r.json()
    def sign(self):
        url = "https://data.cityofnewyork.us/resource/nyis-y4yr.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "$where": "UPPER(street_name) = '{}' AND house__ = '{}' and UPPER(borough) = '{}'".format(self.street_name.upper(), self.house_number, self.borough.upper())          
            }
        r = requests.get(url, params=payload)
        return r.json()



class GetAddress():
    def __init__(self, borough, house_number, street_name):
        self.borough = borough
        if self.borough == "MANHATTAN":
            self.borough_number = "1"
        elif self.borough == "BROOKLYN":
            self.borough_number = "3"
        elif self.borough == "QUEENS":
            self.borough_number = "4"
        elif self.borough == "BRONX":
            self.borough_number = "2"
        elif self.borough == "STATEN ISLAND":
            self.borough_number = "5"

        self.house_number = house_number
        self.street_name = street_name

        house_range = self.house_number.split("-")

        self.bis_jobs = []
        self.now_jobs = []
        self.sign_jobs = []
        self.violations = []
        self.ecb = []
        self.cofo = []
        self.complaints = []


        #if there is a house range
        if len(house_range) > 1:
            for _ in range(int(house_range[0]), (int(house_range[1])+1)):
                #for each house number in range
                self.house_number = _
                for job in self.bis():
                    self.bis_jobs.append(job)
                for job in self.now():
                    self.now_jobs.append(job)
                for job in self.sign():
                    self.sign_jobs.append(job)


        self.info = self.info()
        
        
    
    def sign(self,):
        url = "https://data.cityofnewyork.us/resource/nyis-y4yr.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "$where": "UPPER(street_name) = '{}' AND house__ = '{}' and UPPER(borough) = '{}'".format(self.street_name.upper(), self.house_number, self.borough.upper())          
            }
        r = requests.get(url, params=payload)
        return r.json()
    


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

    def now(self, ):
        url = "https://data.cityofnewyork.us/resource/w9ak-ipjd.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "$where": "UPPER(street_name) = '{}' AND house_no = '{}' and UPPER(borough) = '{}'".format(self.street_name.upper(), self.house_number, self.borough.upper())          
            }
        r = requests.get(url, params=payload)
        return r.json()
    
    def bis(self, ):
    
        url = "https://data.cityofnewyork.us/resource/ic3t-wcy2.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "$where": "UPPER(street_name) = '{}' AND house__ = '{}' and borough = '{}'".format(self.street_name.upper(), self.house_number, self.borough)          
            }
        r = requests.get(url, params=payload)
        return r.json()
"""
    






if __name__ == "__main__":
    #binData = GetBin("1084455")
    #d = GetBlockLot(520, 56)
    pass