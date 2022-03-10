import requests
import json

APP_TOKEN = "jRFBgbNXCPdumKaN1BYKLd0kK"

def pprint(json_item):
    print(json.dumps(json_item, indent=4))


class GetBin():
    def __init__(self, bin_number):
        self.bin_number = bin_number
        bis_jobs = self.bis()
        now_jobs = self.now()
        violations = self.violations()
        ecb = self.ecb()
        
        
        
    
    def ecb(self, ):
        url = "https://data.cityofnewyork.us/resource/6bgk-3dad.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "bin" : "{}".format(self.bin_number),
            "$q" : "active"
            }
        r = requests.get(url, params=payload)
        return r.json()
    
    
    def violations(self, ):
        url = "https://data.cityofnewyork.us/resource/3h2n-5cm9.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "bin" : "{}".format(self.bin_number),
            "$q" : "active"
            }
        r = requests.get(url, params=payload)
        return r.json()
    
    def now(self, ):
        url = "https://data.cityofnewyork.us/resource/w9ak-ipjd.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "bin__" : "{}".format(self.bin_number)
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


if __name__ == "__main__":
    job_data = GetBin("1084455")
    

