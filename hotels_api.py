import json
import requests
from pprint import pprint


LOCALE = 'en_US'
CURRENCY = 'USD'
URL = "https://hotels4.p.rapidapi.com/locations/v2/search"
HEADERS = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': "14cb351c01msh1c48214e3041834p18ae28jsndbaf16e16c16"
}


def api_request(querystring, url, headers=HEADERS):
    api_response = requests.request("GET", url, headers=headers, params=querystring)
    print(api_response)
    api_response = json.loads(api_response.text)
    return api_response


def get_destination_id(city, locale=LOCALE, currency=CURRENCY):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": locale, "currency": currency}
    if city:
        response = api_request(querystring, url)
        try:
            destination_id = response['suggestions'][0]['entities'][0]['destinationId']
        except IndexError as error:
            destination_id = None
        return destination_id
    else:
        print('city is empty')


def get_properties_list(destination_id, locale=LOCALE, currency=CURRENCY):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": destination_id, "pageNumber": "1", "pageSize": "25", "checkIn": "2022-01-08",
                   "checkOut": "2022-01-15", "adults1": "1", "sortOrder": "PRICE", "locale": locale, "currency": currency}

    response = api_request(querystring, url)
    response = response['data']['body']['searchResults']['results']
    return response


def get_hotel_photos(hotel_id):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}

    response = api_request(querystring, url)
    return response


def get_hotels(city):
    destination = get_destination_id(city)
    hotels = get_properties_list(destination)
    for hotel in hotels:
        response = {'hotel_name': hotel['name'], 'hotel_rating': hotel['starRating']}
        images = get_hotel_photos(hotel['id'])
        hotel_images = []
        for image in images['hotelImages']:
            hotel_images.append(image['baseUrl'].replace('{size}', 'z'))
        response['hotel_images'] = hotel_images[:5]
        yield response
