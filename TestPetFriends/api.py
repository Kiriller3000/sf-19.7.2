import requests, json

class PetFriends:
    """API библиотека к веб приложению Pet Friends"""

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str) -> json:
        """Получение API ключа"""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers = headers)

        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str='') -> json:
        """Получение списка всех животных"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)

        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_new_pet(self, auth_key: json, age:int=3, animal_type: str='cat', name: str='Petya', pet_photo: str='images/img1.jpg') -> json:
        """Добавление животного"""
        # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        headers = {'auth_key': auth_key['key'], }
        data = {'age': age,
                'animal_type': animal_type,
                'name': name
        }
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data, files=file)

        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, **data_option) -> json:
        """Обновление данных о животном.
        data = data_option
        headers = {'auth_key': auth_key['key']}

        res = requests.put(self.base_url + f'api/pets/{pet_id}', headers=headers, data=data)

        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Удаление животного"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + f'api/pets/{pet_id}', headers=headers)

        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
            print(result)
        return status, result

    def simple_create_new_pet(self, auth_key: json, **data_option) -> json:
        """Добавление животного без фото.
        data = data_option
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
            print(result)
        return status, result

    def set_photo(self, auth_key: json, pet_id: str, pet_photo) -> json:
        """Добавляем/меняем фото первого в списке питомца."""
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(self.base_url + f'api/pets/set_photo/{pet_id}', headers=headers, files=file)

        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
            print(result)
        return status, result

