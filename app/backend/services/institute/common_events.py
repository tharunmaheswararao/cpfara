from flask import jsonify, request
from datetime import datetime
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from sqlalchemy import and_
from selenium import webdriver
import urllib3
import requests

from backend.models.model import Institutions, insert_row, commit_session, rollback_session
from backend.models.database import db

########## --------------------> AICTE APIs START <-------------------- ##########

def aicte_text_formmater(element):
    anchor_text = element.text
    anchor_text = anchor_text.replace('\n', '')
    anchor_text_list = anchor_text.split(' ')
    anchor_text_list = [i for i in anchor_text_list if i]
    anchor_text_list = anchor_text_list[1:-1]
    anchor_text_date = ' '.join(anchor_text_list[1:4])
    new_anchor_text = ' '.join(anchor_text_list)
    anchor_text_date = datetime.strptime(anchor_text_date, '%B %d, %Y')

    return new_anchor_text


def convert_date_format(date_str):
    
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%B %d, %Y')
    
    return formatted_date


def aicte_events_scrapper():
    
    text_list = []
    web_links=[]
   
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    max_pages = 11
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
    
    while current_page <= max_pages:
        url = ""
       
        if(current_page == 0):
            url = "https://aicte-india.org/bulletins/circulars"
        else:
            url = f"https://aicte-india.org/bulletins/circulars?page={current_page}"
        current_url = f'{url}'

        print(current_url)
        try:
            response = http.get(current_url, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Error:", e)
        
        soup = BeautifulSoup(response.content, "html.parser")
        events_div = soup.find('table', {'class': 'views-table cols-4'})
        date_elements_with_class = events_div.find_all(class_='odd')
        event_elements_with_class = events_div.find_all(class_='even')
        
        for element in date_elements_with_class:
            new_anchor_text = aicte_text_formmater(element)
            if(new_anchor_text is not None):
                text_list.append(new_anchor_text)
            else:
                continue

        for element in event_elements_with_class:
            new_anchor_text = aicte_text_formmater(element)
            if(new_anchor_text is not None):
                text_list.append(new_anchor_text)
            else:
                continue
        
        current_page += 1

        web_links.append("https://aicte-india.org/bulletins/circulars")     
       
    return(text_list)


def aicte_events_adder():
    try:
        events_list = aicte_events_scrapper()
        event_list = []
        for event in events_list:
            event_text = event.split(" ")[4:]
            event_text = " ".join(event_text)
            
            existing_event = Institutions.query.filter_by(event_description = event_text).first()

            if existing_event is None:
                event_date = event.split(", ")[1]
                event_year = event.split(" ")[3].split(" ")[0]
                event_date = event_date + " " + event_year
                parsed_date = datetime.strptime(event_date, "%B %d %Y")
                formatted_date = parsed_date.strftime("%Y-%m-%d")
                event_list.append([formatted_date, event_text])
                new_event = Institutions(event_description = event_text, event_date = formatted_date)
                insert_row(new_event)
                commit_session()
            else:
                continue
            
        response = jsonify({'events_data': list(event_list), 'message': True})
        return response
    except Exception as e:
        rollback_session()
        return jsonify({"status": False, "error": str(e)})


def aicte_events_renderer(user_data):
    try:
        event_list = []    
        if user_data["fromDateValue"] == "" and user_data["toDateValue"] == "":
            print("full event list")
            get_events = Institutions.query.filter(Institutions.college_name == "AICTE").order_by(Institutions.event_date.desc()).all()
        elif user_data["fromDateValue"] and user_data["toDateValue"] == "":
            print("only from date")
            get_events = Institutions.query.filter(and_(Institutions.event_date >= user_data["fromDateValue"], Institutions.college_name == "AICTE")).order_by(Institutions.event_date).all()
        elif user_data["fromDateValue"] == "" and user_data["toDateValue"]:
            print("only to date")
            get_events = Institutions.query.filter(and_(Institutions.event_date <= user_data["toDateValue"], Institutions.college_name == "AICTE")).order_by(Institutions.event_date).all()
        else:
            print("both")
            get_events = Institutions.query.filter(and_(Institutions.event_date >= user_data["fromDateValue"],
                                        Institutions.event_date <= user_data["toDateValue"], Institutions.college_name == "AICTE")).order_by(Institutions.event_date).all()
        for eve in get_events:
            date_obj = datetime.strptime(str(eve.event_date), "%Y-%m-%d")
            formatted_date_str = date_obj.strftime("%a, %d %b %Y")
            event_list.append([formatted_date_str, eve.event_description])
        print(event_list)
        response = jsonify({'events_data': list(event_list), 'message': True})
        return response
       
    except Exception as e:
        rollback_session()
        return jsonify({"status": False, "error": str(e)})
    
########## --------------------> AICTE APIs END <-------------------- ##########
    
########## --------------------> IIT APIs START <-------------------- ##########
    
def iit_scrapper(link): 
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    print(f"https://www.iitm.ac.in{link}")
    try:
        response = http.get(f"https://www.iitm.ac.in{link}", verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error:", e)       

    soup = BeautifulSoup(response.content, "html.parser")
    event_name_div = soup.find('div', {'class': 'section__cardposition'})
    event_name = event_name_div.find_all('p')    
    event_date_element = soup.find('div', {'class': 'eventsdate__venue'})
    event_date = event_date_element.find_all('p')
    event_date = str(event_date[0].text)[4:]
    event_date = event_date.strip()
    day_part, month_year_part = event_date.split(" ", 1)
    day_part = day_part.rstrip("rdnht")
    date_string_without_suffix = f"{day_part} {month_year_part}"
    event_date_obj = datetime.strptime(date_string_without_suffix, "%d %b %Y")
    formatted_date = event_date_obj.strftime("%Y-%m-%d")
    return(formatted_date + ' ' + event_name[0].text)


def iit_events_scrapper():
    text_list = []
    web_links=[]
   
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    max_pages = 9
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

    while current_page <= max_pages:
        url = ""
       
        if(current_page == 0):
            url = "https://www.iitm.ac.in/happenings/events"
        else:
            url = f"https://www.iitm.ac.in/happenings/events?page={current_page}"
        current_url = f'{url}'

        try:
            response = http.get(current_url, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Error:", e)

        soup = BeautifulSoup(response.content, "html.parser")
        events_div = soup.find('div', {'data-block-plugin-id': 'views_block:happenings-happ_events_list'})
        anchor_tags = events_div.find_all('a', class_='block__element')
    
        for anchor_tag in anchor_tags:
            href = anchor_tag.get('href')
            text_list.append(iit_scrapper(href))
        
        current_page += 1
        web_links.append("https://www.iitm.ac.in/happenings/events") 

    return text_list


def iit_events_adder():
    try:
        events_list = iit_events_scrapper()
        print(events_list)
        event_list = []
        for event in events_list:
            event_text = event.split(" ")[1: ]
            event_text = " ".join(event_text)
            print(event_text)
            
            existing_event = Institutions.query.filter_by(event_description = event_text).first()

            if existing_event is None:
                event_date = event.split(" ")[0]
                event_list.append([event_date, event_text])
                new_event = Institutions(event_description = event_text, event_date = event_date, college_name = "IIT")
                insert_row(new_event)
                commit_session()
            else:
                continue
            
        response = jsonify({'events_data': list(event_list), 'message': True})
        return response
    except Exception as e:
        rollback_session()
        return jsonify({"status": False, "error": str(e)})
    

def iit_events_renderer(user_data):
    try:
        # iit_events_adder()
        event_list = []    
        if user_data["fromDateValue"] == "" and user_data["toDateValue"] == "":
            print("full event list")
            get_events = Institutions.query.filter(Institutions.college_name == "IIT").order_by(Institutions.event_date.desc()).all()
        elif user_data["fromDateValue"] and user_data["toDateValue"] == "":
            print("only from date")
            get_events = Institutions.query.filter(and_(Institutions.event_date >= user_data["fromDateValue"], Institutions.college_name == "IIT")).order_by(Institutions.event_date).all()
        elif user_data["fromDateValue"] == "" and user_data["toDateValue"]:
            print("only to date")
            get_events = Institutions.query.filter(and_(Institutions.event_date <= user_data["toDateValue"], Institutions.college_name == "IIT")).order_by(Institutions.event_date).all()
        else:
            print("both")
            get_events = Institutions.query.filter(and_(Institutions.event_date >= user_data["fromDateValue"],
                                        Institutions.event_date <= user_data["toDateValue"], Institutions.college_name == "IIT")).order_by(Institutions.event_date).all()
        for eve in get_events:
            date_obj = datetime.strptime(str(eve.event_date), "%Y-%m-%d")
            formatted_date_str = date_obj.strftime("%a, %d %b %Y")
            event_list.append([formatted_date_str, eve.event_description])
        print(event_list)
        response = jsonify({'events_data': list(event_list), 'message': True})
        return response
       
    except Exception as e:
        rollback_session()
        return jsonify({"status": False, "error": str(e)})
    
########## --------------------> IIT APIs END <-------------------- ##########
    
########## --------------------> IITA APIs START <-------------------- ##########
    
def iiita_events_scrapper():
    text_list = []
    web_links=[]
   
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    max_pages = 9
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

    while current_page <= max_pages:
        url = f"https://www.iiita.ac.in/events.php?page={current_page+1}"
        current_url = f'{url}'

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
            response = http.get(current_url, headers=headers, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Error:", e)

        print(str(current_page + 1))

        soup = BeautifulSoup(response.content, "html.parser")
        events_div = soup.find_all('div', {'class': 'span8 eventGrid'})
        
        for event in events_div:
            event_name = event.find('div', class_='span7 eventGridHeading')
            event_name = event_name.find('h2')
            event_date = event.find('div', class_='span1 eventDateTag')
            event_date = event_date.find_all('p')
            date_text = ""
            for i in event_date:  
                date_text += i.text  
            text_list.append(date_text + " " + event_name.text)
        
        current_page += 1
        web_links.append("https://www.iiita.ac.in/events.php") 

    return text_list


def iiita_events_adder():
    try:
        events_list = iiita_events_scrapper()
        print(events_list)
        event_list = []
        for event in events_list:
            event_text = event.split(" ")[1: ]
            event_text = " ".join(event_text)
            print(event_text)
            
            existing_event = Institutions.query.filter_by(event_description = event_text).first()

            if existing_event is None:
                event_date = event.split(" ")[0]
                month_dict = {
                    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
                    "May": "05", "June": "06", "July": "07", "Aug": "08",
                    "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
                }

                year = int(event_date[:4])
                day = event_date[4:6]
                month_str = event_date[6:]

                if month_str in month_dict:
                    month = month_dict[month_str]
                else:
                    month = month_str
                    
                date_object = datetime.strptime(f"{year}{day}{month}", "%Y%d%m")
                formatted_date = date_object.strftime("%Y-%m-%d")
                event_list.append([formatted_date, event_text])
                new_event = Institutions(event_description = event_text, event_date = formatted_date, college_name = "IIITA")
                insert_row(new_event)
                commit_session()
            else:
                continue
            
        response = jsonify({'events_data': list(event_list), 'message': True})
        return response
    except Exception as e:
        rollback_session()
        return jsonify({"status": False, "error": str(e)})


def iiita_events_renderer(user_data):
    try:
        # iiita_events_adder()
        event_list = []    
        if user_data["fromDateValue"] == "" and user_data["toDateValue"] == "":
            print("full event list")
            get_events = Institutions.query.filter(Institutions.college_name == "IIITA").order_by(Institutions.event_date.desc()).all()
        elif user_data["fromDateValue"] and user_data["toDateValue"] == "":
            print("only from date")
            get_events = Institutions.query.filter(and_(Institutions.event_date >= user_data["fromDateValue"], Institutions.college_name == "IIITA")).order_by(Institutions.event_date).all()
        elif user_data["fromDateValue"] == "" and user_data["toDateValue"]:
            print("only to date")
            get_events = Institutions.query.filter(and_(Institutions.event_date <= user_data["toDateValue"], Institutions.college_name == "IIITA")).order_by(Institutions.event_date).all()
        else:
            print("both")
            get_events = Institutions.query.filter(and_(Institutions.event_date >= user_data["fromDateValue"],
                                        Institutions.event_date <= user_data["toDateValue"], Institutions.college_name == "IIITA")).order_by(Institutions.event_date).all()
        for eve in get_events:
            date_obj = datetime.strptime(str(eve.event_date), "%Y-%m-%d")
            formatted_date_str = date_obj.strftime("%a, %d %b %Y")
            event_list.append([formatted_date_str, eve.event_description])
        print(event_list)
        response = jsonify({'events_data': list(event_list), 'message': True})
        return response
       
    except Exception as e:
        rollback_session()
        return jsonify({"status": False, "error": str(e)})

########## --------------------> IITA APIs END <-------------------- ##########
    
########## --------------------> SRM APIs START <-------------------- ##########
    
def srm_events_scrapper():
    text_list = []
    web_links=[]
   
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    max_pages = 9
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

    while current_page <= max_pages:
        url = "https://www.srmist.edu.in/events/"
        current_url = f'{url}'

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
            response = http.get(current_url, headers=headers, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Error:", e)
        print(str(current_page + 1))
        soup = BeautifulSoup(response.content, "html.parser")
        events_div = soup.find('div', {'class': 'jet-listing-grid__items grid-col-desk-4 grid-col-tablet-2 grid-col-mobile-1 jet-listing-grid--39408'})
        event_date = events_div.find_all('div', class_='jet-listing-dynamic-field__content')
        event_name = events_div.find_all('a')
        print(event_date, event_name)

        next_button_container = soup.find('div', {'class': 'elementor-element elementor-element-60cb50ed elementor-widget elementor-widget-jet-smart-filters-pagination'})
        print(next_button_container)
        next_button = next_button_container.find_all('div')
        print(next_button)
        next_button.click()
        
        current_page += 1
        web_links.append("https://www.srmist.edu.in/events/") 

    return text_list


def srm_events_adder():
    try:
        events_list = srm_events_scrapper()
        print(events_list)
        event_list = []
        # for event in events_list:
        #     event_text = event.split(" ")[1: ]
        #     event_text = " ".join(event_text)
        #     print(event_text)
            
        #     existing_event = Institutions.query.filter_by(event_description = event_text).first()

        #     if existing_event is None:
        #         event_date = event.split(" ")[0]
        #         event_list.append([event_date, event_text])
        #         new_event = Institutions(event_description = event_text, event_date = event_date, college_name = "IIT")
        #         insert_row(new_event)
        #         commit_session()
        #     else:
        #         continue
            
        response = jsonify({'events_data': list(event_list), 'message': True})
        return response
    except Exception as e:
        rollback_session()
        return jsonify({"status": False, "error": str(e)})


def srm_events_renderer(user_data):
    try:
        srm_events_adder()
        event_list = []    
        # if user_data["fromDateValue"] == "" and user_data["toDateValue"] == "":
        #     print("full event list")
        #     get_events = Institutions.query.filter(Institutions.college_name == "IIT").order_by(Institutions.event_date.desc()).all()
        # elif user_data["fromDateValue"] and user_data["toDateValue"] == "":
        #     print("only from date")
        #     get_events = Institutions.query.filter(and_(Institutions.event_date >= user_data["fromDateValue"], Institutions.college_name == "IIT")).order_by(Institutions.event_date).all()
        # elif user_data["fromDateValue"] == "" and user_data["toDateValue"]:
        #     print("only to date")
        #     get_events = Institutions.query.filter(and_(Institutions.event_date <= user_data["toDateValue"], Institutions.college_name == "IIT")).order_by(Institutions.event_date).all()
        # else:
        #     print("both")
        #     get_events = Institutions.query.filter(and_(Institutions.event_date >= user_data["fromDateValue"],
        #                                 Institutions.event_date <= user_data["toDateValue"], Institutions.college_name == "IIT")).order_by(Institutions.event_date).all()
        # for eve in get_events:
        #     date_obj = datetime.strptime(str(eve.event_date), "%Y-%m-%d")
        #     formatted_date_str = date_obj.strftime("%a, %d %b %Y")
        #     event_list.append([formatted_date_str, eve.event_description])
        print(event_list)
        response = jsonify({'events_data': list(event_list), 'message': True})
        return response
       
    except Exception as e:
        rollback_session()
        return jsonify({"status": False, "error": str(e)})

########## --------------------> SRM APIs START <-------------------- ##########