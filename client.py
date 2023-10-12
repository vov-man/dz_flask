import requests

# создание обьявления
response = requests.post("http://127.0.0.1:5000/advertisements/",
                        json={'title': 'laptop',
                              'creator': 'Vladimir',
                              "description": "super laptop", 
                              },)
print(response.status_code)
print(response.json())

#добавление записи
response = requests.get("http://127.0.0.1:5000/advertisements/1",)
print(response.status_code)
print(response.json())

#обновление записи
response = requests.patch('http://127.0.0.1:5000/advertisements/1',
                           json={'email': 'user_new@email.org', })
print(response.status_code)
print(response.json())

# вывод записи на экран
response = requests.get('http://127.0.0.1:5000/advertisements/1',)
print(response.status_code)
print(response.json())

#удаление записи
response = requests.delete(
    "http://127.0.0.1:5000/advertisements/1",
)
print(response.status_code)
print(response.json())

