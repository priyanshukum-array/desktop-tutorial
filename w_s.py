import requests
from bs4 import BeautifulSoup

url = "https://imsnsit.org/imsnsit/notifications.php"
resp = requests.get(url, timeout=15)
soup = BeautifulSoup(resp.text, "html.parser")

table_rows = soup.find_all("tr")

published_by_list = []

for row in table_rows[2:]:  # skip header rows
    cells = row.find_all("td")
    if len(cells) > 1:  # Column 1 exists
        col_text = cells[1].get_text(strip=True)
        if "Published By:" in col_text:
            pub_text = col_text.split("Published By:")[-1].strip()
            last_person = pub_text.split(",")[-1].strip()
            published_by_list.append(last_person)

# Print results
for i, person in enumerate(published_by_list, 1):
    print(f"{i}. {person}")
