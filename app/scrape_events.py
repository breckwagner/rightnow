import requests
import datetime
import database
import models


TOURISM_VICTORIA_EVENTS_ENDPOINT = "https://www.eventbrite.ca/directory/json?page=&cat=&format=&q=&loc=Victoria%2C+BC%2C+Canada&date=&start_date=&end_date=&is_paid=&sort=best&crt=regular&slat=&slng=&radius=&vp_ne_lat=&vp_ne_lng=&vp_sw_lat=&vp_sw_lng=&view=list"

def parse_datetime(date_string):
   return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")

def ticket_availability(m_placemark):
    if m_placemark["price_range"] == "Free":
        return True
    else:
        return (m_placemark["ticket_availability"]["remaining_capacity"] > 0)


def run_scraper():
    response = requests.get(TOURISM_VICTORIA_EVENTS_ENDPOINT)

    events = []
    for placemark in response.json()["events"]:
        if placemark["venue"]["address"]["city"] == "Victoria":
            events.append(
                models.Event(
                    placemark["category"]["name"],
                    placemark["name"]["text"],
                    placemark["venue"]["name"] +" ," + placemark["venue"]["address"]["address_1"],
                    placemark["description"]["text"],
                    placemark["venue"]["address"]["latitude"],
                    placemark["venue"]["address"]["longitude"],
                    placemark["venue"]["address"]["postal_code"],
                    placemark["price_range"],
                    ticket_availability(placemark),
                    placemark["start"]["date_header"],
                    parse_datetime(placemark["start"]["local"]),
                    parse_datetime(placemark["end"]["local"]),
                )
            )

    print "Adding {} events to database".format(len(events))
    database.db_session.add_all(events)
    database.db_session.commit()


if __name__ == "__main__":
    run_scraper()
