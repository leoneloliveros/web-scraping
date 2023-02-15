from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
import csv

options = Options()
options.add_argument('--headless')

driver = webdriver.Firefox(options=options)
driver.get("http://100.126.20.133/maximo/ui/?event=loadapp&value=incident&uisessionid=9981&csrftoken=a6qa6acbh2mnvjotdv9rpn9p24")
time.sleep(2)

soup = BeautifulSoup(driver.page_source, 'html.parser')

na = []
addr = []
for name in soup.findAll("a", {'class': 'visaATMPlaceLink'}):
    na.append(name.text)
for add in soup.findAll("p", {'class': 'visaATMAddress'}):
    addr.append(add.get_text(strip=True, separator=" "))

with open('out.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Address'])
    for _na, _addr in zip(na, addr):
        writer.writerow([_na, _addr])

driver.quit()


cookies = driver.get_cookies()
JSESSIONID = [c for c in cookies if c['name'] == 'JSESSIONID'][0]['value']
LtpaToken2 = [c for c in cookies if c['name'] == 'LtpaToken2'][0]['value']
print(JSESSIONID)
print(LtpaToken2)

# send a POST request to the page with a cookie from the session
session = requests.Session()
cookie = {"JSESSIONID": JSESSIONID, "LtpaToken2": LtpaToken2}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {'data': 'your-data-here'}
response = session.post("http://100.126.20.133/maximo/ui/maximo.jsp",
                        cookies=cookie, headers=headers, data=data)

# parse the response as JSON
print(response.text)
data = json.loads(response.text)

print(data)

# initialize the database
Base = declarative_base()


class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    field1 = Column(String)
    field2 = Column(String)
    field3 = Column(String)


engine = create_engine(
    'postgresql://leoneloliveros:LA12OM17mz@localhost/database')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# save the records to the database
for record in data['records']:
    db_record = Record(
        field1=record['field1'], field2=record['field2'], field3=record['field3'])
    session.add(db_record)

session.commit()


# close the browser
driver.quit()
