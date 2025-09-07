import requests
from bs4 import BeautifulSoup

import pandas as  pd
import numpy as np 
import xlsxwriter
workbook = xlsxwriter.Workbook(r"C:\Users\priya\OneDrive\Desktop\hack\qwerty.xlsx")


worksheet= workbook.add_worksheet("firstsheet")


worksheet.write(0,0,"date")
worksheet.write(0,1,"noticeheadline")
worksheet.write(0,2,"publishedby")

url = "https://imsnsit.org/imsnsit/notifications.php"


session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Referer": url
})


resp_latest = session.get(url, timeout=15)
soup_latest = BeautifulSoup(resp_latest.text, "html.parser")

resp_old = session.post(url, data={"olddata": "Archive"}, timeout=15)
soup_old = BeautifulSoup(resp_old.text, "html.parser")


table_rows = soup_latest.find_all("tr") + soup_old.find_all("tr")

results = []

for row in table_rows[2:]:  
    cells = row.find_all("td")
    if len(cells) > 1:
       
        date = cells[0].get_text(strip=True)
        
        if '2025' in date:            
            title = cells[1].get_text(strip=True).split("Published By:")[0].strip()
            
            pub_last = ""
            if "Published By:" in cells[1].get_text(strip=True):
                pub_text = cells[1].get_text(strip=True).split("Published By:")[-1].strip()
                pub_last = pub_text.split(",")[-1].strip()
            results.append((title, date, pub_last))


for i, (title, date, pub_last) in enumerate(results, 1):  # 1-based count for S.NO.

   
   worksheet.write(i+1,0,date)
   worksheet.write(i+1,1,title)
   worksheet.write(i+1,2,pub_last)
   #print(f"{i}. {title} ({date}) | Published By: {pub_last}")

workbook.close()
print("ho gaya pajji")
   

