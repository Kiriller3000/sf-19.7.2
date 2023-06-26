from api import PetFriends
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


def test_add_new_pet_with_valid_key_and_data(age=2, animal_type='dog', name='Kolya', pet_photo='images/img2.jpg'):
    """Добавляем питомца с фото и проверяем, что ответ сервера имеет статус 200 и данные в формате json,
    где содержится поле 'id'"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

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

    status, result = pf.update_pet_info(auth_key, pet_id, name=name, animal_type=animal_type, age=age)
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

    status, result = pf.simple_create_new_pet(auth_key, name='simple_create', animal_type='zver', age='age')

    assert status == 200
    assert 'id' in result

# #2
def tests_set_photo(pet_photo='images/rac2.jpg'):
    """ Добавляем/меняем фото первого в списке питомца.
        Если список животных зарегестрированного пользователя пуст, создаем нового питомца.
        Ответ должен содержать поле 'pet_photo'."""
    auth_key = pf.get_api_key(valid_email, valid_password)[1]
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    try:
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
    except:
        pf.simple_create_new_pet(auth_key, name='from test_set_foto', animal_type='zveruga', age='very young')
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']

    status, result = pf.set_photo(auth_key, pet_id, pet_photo)

    assert status == 200
    assert 'pet_photo' in result

################################ Далее негативные тесты ########################################

# #3
@pytest.mark.xfail
def test_get_api_key_for_invalid_user(email=valid_email, password='valid_password'):
    """Передаем неверные авторизационные данные. Ожидаем код ответа не 200."""
    status = pf.get_api_key(email, password)[0]
    assert status != 200

# #4
@pytest.mark.xfail
def test_get_list_of_pets_with_invalid_key(filter=''):
    """Проверяем не выводится ли список животных с неверным auth_key. Код ответа должен быть, согласно swagger 403."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] += 'Any string in the key'
    status, _ = pf.get_list_of_pets(auth_key, filter)

    assert status == 403

# #5
@pytest.mark.xfail
def test_get_list_of_pets_with_non_exisistant_filter(filter='Pets of other user'):
    """Проверяем не выводится ли список животных с ошибочным фильтром.
       Код ответа сервера не должен быть 200."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.get_list_of_pets(auth_key, filter)

    assert status != 200


# #6
@pytest.mark.xfail
def test_add_new_pet_with_invalid_key(age=2, animal_type='dog', name='Kolya'):
    """Добавляем питомца с фото, с неверным auth_key. Код ответа 403."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] += 'Any string in the key'
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/img2.jpg')

    status, result = pf.add_new_pet(auth_key, age, animal_type, name, pet_photo)
    assert status == 403

# #3
# @pytest.mark.xfail
# def test_add_new_pet_with_non_complete_data(age=2, animal_type='dog', name='Kolya'):
#     """Добавляем питомца с фото, с неверным auth_key. Код ответа 403."""
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     pet_photo = os.path.join(os.path.dirname(__file__), 'images/img2.jpg')
#
#     status, result = pf.add_new_pet(auth_key, age, animal_type, name, pet_photo)
#     assert status == 400


# #7

@pytest.mark.xfail
def tests_simple_create_new_pet_with_invalid_data():
    """Создаем питомца. Передаем не полные данные-без возраста и породы.
       Ответ должен содержать код 400 - неверные данные"""
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    status = pf.simple_create_new_pet(auth_key, age='very young')[0]

    assert status == 400

# # #4 Не подходит для автотеста
# @pytest.mark.xfail
# def tests_set_photo_unsuccess():
#     """ Добавляем/меняем фото первого в списке питомца. Заместо картинки передаем другой формат.
#         Ответ не должен содержать код 200"""
#     auth_key = pf.get_api_key(valid_email, valid_password)[1]
#
#     #Передаем текст вместо фото
#     pet_photo = os.path.join(os.path.dirname(__file__), '../requirements.txt')
#
#     try:
#         pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
#     except:
#         pf.simple_create_new_pet(auth_key, name='from test_set_foto')
#         pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
#
#     status, _ = pf.set_photo(auth_key, pet_id, pet_photo)
#     # Ожидаем, что ответ не равен 200
#     assert status != 200

# #5

# #8
@pytest.mark.xfail
def tests_simple_create_new_pet_with_incorrect_key():
    """Создаем питомца без фото c неверным ключем. Ответ должен содержать код 403"""
    auth_key = pf.get_api_key(valid_email, valid_password)[1]
    auth_key['key'] += 'Any string in the key'

    status = pf.simple_create_new_pet(auth_key, name='simple_create', animal_type='racoon', age='536')[0]

    # Ожидаем код 403 - Неверный ключ
    assert status == 403

# #9 !
@pytest.mark.xfail
def test_update_pet_info_with_invalid_petID(name="Kolya", animal_type='cat', age=6):
    """Обновляем инфо о питомце. Передаем неверный pet_id. Ожидаем, что код ответа сервера не 200."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id'] # Если список пустой,
    except:
        pf.add_new_pet(auth_key)                                                      #создаем питомца
        pet_id = pf.get_list_of_pets(auth_key, filter='my_pets')[1]['pets'][0]['id']
    status, result = pf.update_pet_info(auth_key, 'pet_id', name=name, animal_type=animal_type, age=age)
    assert status != 200

# #10
@pytest.mark.xfail
def test_add_new_pet_with_text_data_of_age(age='unknown', animal_type='unfamiliar', name='nonamed', pet_photo='images/rac1.jpg'):
    """Добавляем питомца, передаем в поле возраст текстовые данные, ожидаем код ответа 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.add_new_pet(auth_key, age=age, animal_type=animal_type, name=name,pet_photo=pet_photo)
    assert status == 400

