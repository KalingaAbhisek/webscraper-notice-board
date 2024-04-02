import requests
from bs4 import BeautifulSoup
import pymongo
import schedule
import certifi
from flask import Flask, jsonify
import time
ca = certifi.where()

app = Flask(__name__)

def scrape_websites():
    data_dict={}
    url = 'https://www.soa.ac.in/iter'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        div_elements = soup.find_all('div', class_='summary-title')
        for div in div_elements:
            links = div.find_all('a', class_='summary-title-link')
            text = div.get_text()
            for link in links:
                link = link['href']
                data_dict[f"{text}"]=link
        array_of_objects=[]
        for key, value in data_dict.items():
            array_of_objects.append({"notice": key,"link":value})
        print(array_of_objects)
        filter_criteria = {}
        collection.delete_many(filter_criteria)
        collection.insert_many(array_of_objects)
        print(f"Inserted {len(array_of_objects)} documents into MongoDB")
    else:
        print('Failed to fetch the page:', response.status_code)

MONGO_URI = 'mongodb+srv://clistby:clistby@cluster0.zhsxrdu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
DATABASE_NAME = "test"
COLLECTION_NAME = "webscrape"
client = pymongo.MongoClient(MONGO_URI,tlsCAFile=ca)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]
print("Connected to MongoDB Client")

@app.route("/api/data", methods=["GET"])
def get_data():
    data = []
    for doc in collection.find({}, {'_id': False}):
        data.append(doc)
    return jsonify(data)

if __name__ == "__main__":
    scrape_websites()
    # schedule.every().hour.do(scrape_websites)
    schedule.every(2).minutes.do(scrape_websites)
    app.run(debug=True)
    while True:
        scrape_websites()
        schedule.run_pending()
        time.sleep(1)
    # Schedule web scraper function to run every hour

# pip install -r requirements.txt
