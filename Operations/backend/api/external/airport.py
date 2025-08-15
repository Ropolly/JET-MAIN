import requests
from bs4 import BeautifulSoup

def get_flight_aware(request):
    url = f"https://flightaware.com/{request}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

    return BeautifulSoup(response.content, "html.parser")

def get_airport(airport_code):
    url = f"resources/airport/{airport_code}"
    return get_flight_aware(url)


def parse_fuel_cost(soup):
    final = []
    for fbo in soup.find_all('tr', class_='fuel_facility'):
        new = {
            'fbo_name' : fbo.find('a').text.strip(),
            'jet_a_cost': fbo.find_all('td')[6].text.strip(),
        }
        if new['jet_a_cost']:
            final.append(new)

    return final


def get_fbo(airport_code, name):
    url = f"resources/airport/{airport_code}/services/FBO/{name.replace(' ', '%20')}"
    return get_flight_aware(url)

def parse_fbo(soup):
    website = soup.find('div', class_="airportBoardContainer").find('a').text.strip()
    phone = soup.find('div', class_="airportBoardContainer").find_all('td')[3].text.strip().replace('+','').replace('-','')
    return website, phone if phone else None

def parse_timezone(soup):
    timezone = soup.find('table').find_all('td')[2].find('span').text.strip()
    return timezone

if __name__ == "__main__":
    soup = get_airport("KTPA")
    print(parse_fuel_cost(soup))
