from bs4 import BeautifulSoup
from airport import get_flight_aware


def get_current(tailnumber):
    url = f"resources/aircraft/{tailnumber}"
    return get_flight_aware(url)