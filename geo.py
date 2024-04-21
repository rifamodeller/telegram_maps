import requests
import sys

apikey = "40d1649f-0493-4b70-98ba-98533de7710b"

capitals_europe = ['Великобритания', 'Ирландия', 'Норвегия', 'Швеция', 'Швейцария', 'Монголия', 'Австрия', 'Италия',
                   'Германия', 'Испания']


def geocode(s):
    st = f'https://geocode-maps.yandex.ru/1.x/?apikey={apikey}&geocode={s}&format=json'
    response = requests.get(st)
    param = response.json()
    toponym = param["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    up = toponym["boundedBy"]["Envelope"]["upperCorner"]
    low = toponym["boundedBy"]["Envelope"]["lowerCorner"]
    up1 = (float(up.split()[0]) + 180) % 360 - 180
    up2 = (float(up.split()[1]) + 180) % 360 - 180
    low1 = (float(low.split()[0]) + 180) % 360 - 180
    low2 = (float(low.split()[1]) + 180) % 360 - 180
    ll = (toponym["Point"]['pos']).split()
    ll1 = (float(ll[0]) + 180) % 360 - 180
    ll2 = (float(ll[1]) + 180) % 360 - 180
    # print(f'bbox={low1},{low2}~{up1},{up2}&l=sat')
    return f'bbox={low1},{low2}~{up1},{up2}&l=sat&pt={ll1},{ll2},pm2rdl'
    # return f'll={l1},{l2}'


def load_map(param):
    map_request = f"http://static-maps.yandex.ru/1.x/?{param}"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file

# while input() != "0":
#     load_map(geocode(capitals_europe[random.randint(0, 9)]))
