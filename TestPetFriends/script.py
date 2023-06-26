import json, requests
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def delete_excess(name=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pf.get_list_of_pets()

    headers = {'auth_key': auth_key['key']}
    filter = {'filter': filter}
    res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)