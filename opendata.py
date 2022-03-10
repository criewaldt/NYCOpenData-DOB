import requests
import json
import xlwt
import time

APP_TOKEN = "jRFBgbNXCPdumKaN1BYKLd0kK"

def pprint(json_item):
    print(json.dumps(json_item, indent=4))
    

class Spreadsheet():
    def __init__(self, bin_number):
    
        self.timestr = time.strftime("%Y-%m-%d-%H-%M")
    
        self.bin_number = bin_number
        self.book = xlwt.Workbook()
        self.sheet = self.book.add_sheet(str(self.bin_number))
        self.current_row = 0
        
        style = xlwt.XFStyle()

        # font
        font = xlwt.Font()
        font.bold = True
        style.font = font
        self.style = style
        
        
    
    def Seperator(self,):
        pattern = xlwt.Pattern() # Create the Pattern
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        pattern.pattern_fore_colour = 23 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
        style = xlwt.XFStyle() # Create the Pattern
        style.pattern = pattern # Add Pattern to Style
        
        for col in range(4):
            self.sheet.write(self.current_row, col, '', style)
        self.current_row += 1
        
        self.book.save("output/{}_{}.xls".format(str(self.bin_number), self.timestr))
    
    def DOBViolations(self, violation_data):
        self.sheet.write(self.current_row, 0, "Open DOB Violations", self.style)
        self.current_row += 1
        
        self.sheet.write(self.current_row, 0, "Violation Number:", self.style)
        self.sheet.write(self.current_row, 1, "Violation Status:", self.style)
        self.current_row += 1
        
        
        for v in violation_data:
            
            self.sheet.write(self.current_row, 0, v['number'])
            self.sheet.write(self.current_row, 1, v['status'])
            self.current_row += 1
        
        self.current_row += 1
        
        self.Seperator()
        
        self.book.save("output/{}_{}.xls".format(self.bin_number, self.timestr))

    def ECB(self, violation_data):
        
        self.sheet.write(self.current_row, 0, "Open ECB Violations", self.style)
        self.current_row += 1
        
        self.sheet.write(self.current_row, 0, "Violation Number:", self.style)
        self.sheet.write(self.current_row, 1, "Date of Violation:", self.style)
        self.sheet.write(self.current_row, 2, "Violation Status:", self.style)

        self.current_row += 1
        for violation in violation_data:
            self.sheet.write(self.current_row, 0, violation['number'])
            self.sheet.write(self.current_row, 1, violation['date'])
            self.sheet.write(self.current_row, 2, violation['status'])
            self.current_row += 1
            
        self.current_row += 1
        
        self.Seperator()
        
        self.book.save("output/{}_{}.xls".format(self.bin_number, self.timestr))
        
    
    
    def Job(self, job_data):
        
        print("Writing job data for job# {}".format(job_data['job_number']))
        
        self.sheet.write(self.current_row, 0, "Description:", self.style)
        self.sheet.write(self.current_row+1, 0, "Design Team:", self.style)
        self.sheet.write(self.current_row+2, 0, "Filing Representative:", self.style)
        self.sheet.write(self.current_row+3, 0, "Job Number:", self.style)
        
        self.sheet.write(self.current_row, 1, job_data['description'])
        self.sheet.write(self.current_row+1, 1, job_data['design_team'])
        self.sheet.write(self.current_row+2, 1, job_data['filing_rep'])
        self.sheet.write(self.current_row+3, 1, job_data['job_number'])
        
        self.sheet.write(self.current_row, 2, "Status:", self.style)
        self.sheet.write(self.current_row+1, 2, "Job Type:", self.style)
        self.sheet.write(self.current_row+2, 2, "Floors:", self.style)
        self.sheet.write(self.current_row+3, 2, "Date Filed:", self.style)
        
        self.sheet.write(self.current_row, 3, job_data['job_status'])
        self.sheet.write(self.current_row+1, 3, job_data['job_type'])
        self.sheet.write(self.current_row+2, 3, job_data['work_on_floors'])
        self.sheet.write(self.current_row+3, 3, job_data['date_filed'])
        
        self.current_row += 4
        
        self.sheet.write(self.current_row, 0, "Required Items:", self.style)
        self.current_row += 1
        
        #required items
        """
        for item in job_data['required_items']:
            self.sheet.write(self.current_row, 1, item)
            self.current_row += 1
        self.current_row += 1
        """
        
        self.Seperator()
        
        self.book.save("output/{}_{}.xls".format(self.bin_number, self.timestr))

class GetBin():
    def __init__(self, bin_number):
        self.bin_number = bin_number
        self.bis_jobs = self.bis()
        #now_jobs = self.now()
        #violations = self.violations()
        #ecb = self.ecb()
        
    
    def ecb(self, ):
        url = "https://data.cityofnewyork.us/resource/6bgk-3dad.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "bin" : "{}".format(self.bin_number),
            "ecb_violation_status" : "ACTIVE"
            }
            
        #return active ECB violations
        r = requests.get(url, params=payload)
        return r.json()
    
    
    def violations(self, ):
        url = "https://data.cityofnewyork.us/resource/3h2n-5cm9.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "bin" : "{}".format(self.bin_number),
            "$q" : "active"
            }
            
        #return active DOB violations
        r = requests.get(url, params=payload)
        return r.json()
    
    def now(self, ):
        url = "https://data.cityofnewyork.us/resource/w9ak-ipjd.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "bin" : "{}".format(self.bin_number)
            }
        r = requests.get(url, params=payload)
        
        #only return jobs that are not signed off
        
        now_jobs = []
        for job in r.json():
            if job['filing_status'] != "LOC Issued":
                now_jobs.append(job)
        
        return now_jobs
    
    def bis(self, ):
    
        url = "https://data.cityofnewyork.us/resource/ic3t-wcy2.json"
        payload = {
            
            "$$app_token" : APP_TOKEN,
            "bin__" : "{}".format(self.bin_number)
            }
        r = requests.get(url, params=payload)
        
        #only return jobs that are not signed off
        bis_jobs = []
        for job in r.json():
            if job['job_status'] != "X":
                
                j = {
                    "description" : job['job__'],
                    "design_team" : " - ".join([job['applicant_s_last_name'], job['applicant_license__']]),
                    "filing_rep" : "n/a",
                    "job_number" : job['job__'],
                    "job_status" : " - ".join([job['job_status'], job['job_status_descrp']]),
                    "job_type" : job['job_type'],
                    "work_on_floors" : "n/a",
                    "date_filed" : job['pre__filing_date'],
                }
                bis_jobs.append(j)
        
        return bis_jobs


if __name__ == "__main__":
    bin_num = "1084455"

    j = GetBin(bin_num)
    s = Spreadsheet(bin_num)
    
    for job in j.bis_jobs:
        s.Job(job)