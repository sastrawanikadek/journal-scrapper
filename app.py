from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime
import requests
import re
import os

load_dotenv()

total_requests = os.getenv("TOTAL_REQUESTS", 0)
current_requests = 0
fetched_week = 0
issues_pattern = "^" + re.escape("https://scholarhub.ui.ac.id/jessd/vol") + "\\d+" + re.escape("/iss") + "\\d+$"
issues_regex = re.compile(issues_pattern)
articles_pattern = "^" + re.escape("https://scholarhub.ui.ac.id/cgi/viewcontent.cgi?article=") + "\\d+[&]{1}\\S+$"
articles_regex = re.compile(articles_pattern)

while True:
    current_week = datetime.now().isocalendar()[1]

    if int(fetched_week) == int(current_week):
        if current_requests < int(total_requests):
            html = requests.get("https://scholarhub.ui.ac.id/jessd/")
            parsed_html = BeautifulSoup(html.text, "html.parser")

            for option in parsed_html.find_all("option"):
                if issues_regex.match(option["value"]) is not None:
                    html = requests.get(option["value"])
                    parsed_html = BeautifulSoup(html.text, "html.parser")

                    for anchor in parsed_html.find_all("a"):
                        if articles_regex.match(anchor["href"]) is not None:
                            req = requests.get(anchor["href"])
                            print("Status code of {} is {}".format(anchor["href"], req.status_code))

                            if req.status_code == requests.codes.ok:
                                fetched_week += 1
    else:
        current_requests = 0
        fetched_week = current_week
