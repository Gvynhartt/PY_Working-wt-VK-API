import requests
import time


class VKUser:
    url_stub = 'https://api.vk.ru/method/'
    VK_API_VER = '5.199'

    def __init__(self, TOKEN, input_chars, is_id: bool):
        self.TOKEN = TOKEN
        # следующая развилка нужна. т.к. пользователй можно искать средствами API и по ID, и по screen_name
        if is_id == False:
            self.screen_name = input_chars
            get_id_req = requests.get(self.url_stub + 'utils.resolveScreenName',
                                      params={'v': self.VK_API_VER, 'access_token': self.TOKEN,
                                              'screen_name': input_chars})
            time.sleep(1)
            self.user_id = get_id_req.json()['response']['object_id']
        else:
            self.user_id = input_chars
            req_scr_name = requests.get(self.url_stub + 'users.get',
                                        params={'v': self.VK_API_VER, 'access_token': self.TOKEN,
                                                'user_ids': input_chars,
                                                'fields': 'screen_name'})
            time.sleep(1)
            self.screen_name = req_scr_name.json()['response'][0]['screen_name']

        user_obj = requests.get(self.url_stub + 'users.get',
                                params={'v': self.VK_API_VER, 'access_token': self.TOKEN, 'user_ids': self.user_id})
        time.sleep(1)
        self.first_name = user_obj.json()['response'][0]['first_name']
        self.last_name = user_obj.json()['response'][0]['last_name']

    def __eq__(self, other):
        user1_friends = set()
        user2_friends = set()
        if isinstance(other, VKUser):

            user1_req = requests.get(self.url_stub + 'friends.get',
                                     params={'v': self.VK_API_VER, 'access_token': self.TOKEN,
                                             'screen_name': self.screen_name})
            time.sleep(1)
            user1_ids = user1_req.json()
            for item in user1_ids['response']['items']:
                user1_friends.add(item)
                # добавляет полученный ID друга из списка

            user2_req = requests.get(self.url_stub + 'friends.get',
                                     params={'v': self.VK_API_VER, 'access_token': other.TOKEN,
                                             'screen_name': other.screen_name})
            time.sleep(1)
            user2_ids = user2_req.json()
            for item in user2_ids['response']['items']:
                user2_friends.add(item)

            common_friends = user1_friends.intersection(user2_friends)
            # получает пересечение множеств друзей для первого и второго - в виде списка ID!

            if len(common_friends) == 0:
                print(f'Общих друзей у пользователей {self.screen_name} и {other.screen_name} не обнаружено!')

            else:
                output_friends_obj = []
                for id in common_friends:
                    output_friends_obj.append(VKUser(self.TOKEN, id, True))
        return output_friends_obj

    def print(self):
        print(f'Ссылка на аккаунт пользователя - https://vk.com/{self.screen_name}')
