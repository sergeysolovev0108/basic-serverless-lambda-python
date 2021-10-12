import requests
import json



def get_data() -> list:
    AIRTABLE_BASE_ID = "appsIUCgjVhhGxLi5"
    AIRTABLE_API_KEY = "keyXL3AhnC8uENRd3"
    AIRTABLE_TABLE_NAME = "MainTable"

    endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}?fields%5B%5D=title&sort%5B0%5D%5Bfield%5D=ID&sort%5B0%5D%5Bdirection%5D=asc'

    
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"

    }

    r = requests.get(endpoint, headers=headers).json()

    titles = []

    for title in r['records']:
        if title['fields']:
            titles.append(title['fields']['title'])
    return r

start = -1
end = 2


def func() -> list:

    list_titles = []
    global start
    global end

    data = get_data()

    if end == len(data['records']):
        end = 0
        start += 1
        for i in data['records'][start:]:
            list_titles.append(i['fields']['title'])
        list_titles.append(data['records'][end]['fields']['title'])
        end += 1

        return list_titles

    if start == len(data['records']) - 2 or start == len(data['records']) - 1:
        start += 1
        end += 1
        for i in data['records'][start:]:
            list_titles.append(i['fields']['title'])
        for title in data['records'][0:end]:
            list_titles.append(title['fields']['title'])

        return list_titles

    if start == len(data['records']):
        start = 1
        end += 1
        for i in data['records'][start: end]:
            list_titles.append(i['fields']['title'])

        return list_titles

    start += 1
    end += 1
    for i in data['records'][start:end]:
        try:
            if i['fields']['title']:
                list_titles.append(i['fields']['title'])
        except:
            pass

    return list_titles


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": func(),
            },
            ensure_ascii=False
        ),
    }
 
