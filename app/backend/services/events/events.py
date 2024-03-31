from flask import jsonify, request
from datetime import datetime
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from sqlalchemy import and_
import urllib3
import requests

from backend.models.model import Events, insert_row, commit_session, rollback_session
from backend.models.database import db


########## --------------------> EVENTS APIs START <-------------------- ##########

def kr_events_scrapper():
    text_list = []
    web_links=[]
   
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    max_pages = 2
    current_page = 0

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    links = [
        "https://www.resurchify.com/e/conference/all-categories/india/2024/page/", 
        "https://www.resurchify.com/e/journal/all-categories/india/2024/page/",
        "https://www.resurchify.com/e/seminar/all-categories/india/2024/page/",
        "https://www.resurchify.com/e/workshop/all-categories/india/2024/page/",
        "https://www.resurchify.com/e/symposium/all-categories/india/2024/page/",
        "https://www.resurchify.com/e/meeting/all-categories/india/2024/page/"
    ]

    for i in links:
        while current_page <= max_pages:
            url = f"{i}{current_page+1}/"
            current_url = f'{url}'

            try:
                response = http.get(current_url, verify=False)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print("Error:", e)
            print(current_url)
            soup = BeautifulSoup(response.content, "html.parser")
            events_div = soup.find('div', {'class': 'w3-col l7 m7 s12'})
            anchor_tags = events_div.find_all('div', class_='w3-card-4 w3-round w3-white w3-center w3-responsive')
            for anchor in anchor_tags:
                events_name_div = anchor.find_all('h4', class_='w3-medium w3-hover-text-blue add_underline')
                events_date_div = anchor.find_all('tr', class_='w3-theme-l4')
                event_categories_div = anchor.find_all('tr')
                
                for event_name, event_date, event_cat in zip(events_name_div, events_date_div, [event_categories_div[3]]):
                    # print(event_name.text)
                    event_date = event_date.find_all('b')[1].text.split('-')[0]
                    # print(event_date)
                    # print(event_cat.text)
                    text_list.append([event_name.text, event_date.strip(), event_cat.text.strip().replace('\n', ','), url.split('/')[4]])
            
            current_page += 1
            web_links.append(i)
        current_page = 0
    return text_list


def kr_events_adder():
    try:
        events_list = kr_events_scrapper()
        events_list = [
            [data.replace('\n', '').replace('\xa0', '') for data in event] 
            for event in events_list
        ]
        print(events_list)
        event_list = []
        for event in events_list:
            event_text = event[0]
            print(event_text)
            
            existing_event = Events.query.filter_by(event_description = event_text).first()

            if existing_event is None:
                event_date = event[1]
                date_obj = datetime.strptime(event_date, "%b %d, %Y")
                formatted_date = date_obj.strftime("%Y-%m-%d")
                domain = event[2]
                category = event[3]
                event_list.append([formatted_date, event_text, domain, category])
                new_event = Events(event_description = event_text, event_date = formatted_date, domain = domain, event_type = category)
                insert_row(new_event)
                commit_session()
            else:
                continue
            
        response = jsonify({'events_data': list(event_list), 'message': True})
        return response
    except Exception as e:
        rollback_session()
        return jsonify({"status": False, "error": str(e)})


def kr_events_renderer(user_data):
    try:
        # kr_events_adder()
        event_list = []  
        from_date = user_data["fromDateValue"]
        to_date = user_data["toDateValue"]
        event_type = user_data["checkedValues"] 
        domain_value = user_data["selectedValue"].upper()

        get_domains = Events.query.with_entities(Events.domain).all()
        domain_values = [row[0] for row in get_domains]
        domains = []
        for domain in domain_values:
            domain = domain.split(",")
            for d in domain:
                if(d.strip() != ""):
                    domains.append(d.strip().title())
        domains = list(set(domains))

        if from_date == "" and to_date == "" and not event_type:
            get_events = Events.query.filter(Events.domain.ilike(f'%{domain_value}%')).order_by(Events.event_date.desc()).all()
        else:
            query = Events.query

            if from_date:
                query = query.filter(Events.event_date >= from_date)
            if to_date:
                query = query.filter(Events.event_date <= to_date)
            if event_type:
                query = query.filter(Events.event_type.in_(event_type))
            if domain_value:
                query = query.filter(Events.domain.ilike(f'%{domain_value}%'))

            get_events = query.order_by(Events.event_date).all()

        # Format the retrieved events for response
        for eve in get_events:
            date_obj = datetime.strptime(str(eve.event_date), "%Y-%m-%d")
            formatted_date_str = date_obj.strftime("%a, %d %b %Y")
            event_list.append([formatted_date_str, eve.event_description])

        response = jsonify({'events_data': event_list, 'domains': domains, 'message': True})
        return response
       
    except Exception as e:
        rollback_session()
        return jsonify({"status": False, "error": str(e)})

########## --------------------> EVENTS APIs START <-------------------- ##########