from api_ import PetFriends
from settings import valid_email, valid_password
import os, pytest

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_list_of_pets_with_valid_key(filter=''):
    """Проверяем, что запрос списка всех животных возвращает статус 200 и список содержит значения"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_key_and_data(age=2, animal_type='dog', name='Kolya'):
    """Добавляем питомца с фото и проверяем, что ответ сервера имеет статус 200 и данные в формате json,
    где содержится поле 'id'"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/img2.jpg')

    status, result = pf.add_new_pet(auth_key, age, animal_type, name, pet_photo)
    assert status == 200
    assert 'id' in result


def test_update_pet_info_with_valid_key_and_data_and_petID(name="Kolya", animal_type='cat', age=3):
    """Обновляем инфо о питомце и проверяем код 200 и что ответ сервера содержит
    данные в формате json с полем 'id'.
        Если список животных зарегестрированного пользователя пуст, создаем нового питомца."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
    except:
        pf.add_new_pet(auth_key)
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']

    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 200
    assert 'id' in result


def test_delete_pet_with_valid_key_and_petID():
    """Удаляем питомца, проверяем, что id удаленного питомца отсутствует в текущем списке.
    Если список животных зарегестрированного пользователя пуст, создаем нового питомца."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
    except:
        pf.add_new_pet(auth_key)
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']

    status = pf.delete_pet(auth_key, pet_id)[0]

    my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets']
    if not my_pets and pet_id:
        assert status == 200
    else:
        assert status == 200
        assert pet_id not in my_pets[0]['id']

# #1
def tests_simple_create_new_pet():
    """Создаем питомца без фото. Ответ должен содержать id нового питомца"""
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    status, result = pf.simple_create_new_pet(auth_key,name='simple_create')

    assert status == 200
    assert 'id' in result

# #2
def tests_set_photo():
    """ Добавляем/меняем фото первого в списке питомца.
        Если список животных зарегестрированного пользователя пуст, создаем нового питомца.
        Ответ должен содержать поле 'pet_photo'."""
    # auth_key = pf.get_api_key(valid_email, valid_password)[1]
    auth_key = pf.get_api_key(valid_email, valid_password)[1]
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/img1.jpg')

    try:
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
    except:
        pf.simple_create_new_pet(auth_key, name='from test_set_foto')
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']

    status, result = pf.set_photo(auth_key, pet_id, pet_photo)

    assert status == 200
    assert 'pet_photo' in result

# Далее негативные тесты    @pytest.mark.xfail

# @pytest.mark.xfail
# def tests_simple_create_new_pet_with_invalid_data():
#     """Создаем питомца без фото. Ответ должен содержать id нового питомца"""
#     auth_key = pf.get_api_key(valid_email, valid_password)[1]
#
#     status, result = pf.simple_create_new_pet(auth_key,age='very young')
#     print(pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0])
#     assert status == 400
#     assert 'id' not in result

# #3
@pytest.mark.xfail
def tests_set_photo_unsuccess():
    """ Добавляем/меняем фото первого в списке питомца. Заместо картинки передаем другой формат.
        Ответ не должен содержать код 200"""
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    #Передаем текст вместо фото
    pet_photo = os.path.join(os.path.dirname(__file__), '../requirements.txt')

    try:
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
    except:
        pf.simple_create_new_pet(auth_key, name='from test_set_foto')
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']

    status, _ = pf.set_photo(auth_key, pet_id, pet_photo)
    # Ожидаем, что ответ не равен 200
    assert status != 200

# #4
@pytest.mark.xfail
def tests_simple_create_new_pet_with_incorrect_key():
    """Создаем питомца без фото c неверным ключем. Ответ должен содержать код 403"""
    auth_key = pf.get_api_key(valid_email, valid_password)[1]
    auth_key['key'] += 'Any string in the key'

    status, result = pf.simple_create_new_pet(auth_key, name='simple_create')

    # Ожидаем код 403 - Неверный ключ
    assert status == 403

# #5
@pytest.mark.xfail
def tests_():
    pass