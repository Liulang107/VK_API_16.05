import requests
import time

TOKEN = 'af146ade9a53acc70d6e60cde6cf3ad6ec97744463455e9e3ab5576a0b17f9bd9d768cf21a6941e89faec'
params = {'access_token': TOKEN,
          'v': '5.95'
          }

# Задача 1. Пользователя нужно описать с помощью класса и реализовать метод поиска общих друзей, используя API VK

class User:
    def __init__(self, uid, first_name=None, last_name=None):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_params(self):
        return dict(
            access_token=TOKEN,
            v='5.95'
        )

    def search_for_mutual_friends(self, other):
        params = self.get_params()
        params['source_uid'] = self.uid
        params['target_uid'] = other.uid
        response = requests.get(
            'https://api.vk.com/method/friends.getMutual',
            params
        )
        return response.json()['response']

    def get_info(self):
        params = self.get_params()
        params['user_ids'] = self.uid
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        self.first_name = response.json()['response'][0]['first_name']
        self.last_name = response.json()['response'][0]['last_name']
        return response.json()


def search_user(users):
    user_list = []
    for user in users:
        params['q'] = user
        response = requests.get(
            'https://api.vk.com/method/users.search',
            params
        )
        user_list.append(response.json()['response']['items'][0])
    return user_list


def main():
    while True:
        user_input = input('Введите двух пользователей vk через запятую или q для выхода: ')
        # Михаил Мед, Руслан Мазитов - можно использовать для проверки
        if user_input == 'q':
            break
        else:
            users = user_input.split(', ')
            user_list = search_user(users)
            user1 = User(user_list[0]['id'], user_list[0]['first_name'], user_list[0]['last_name'])
            user2 = User(user_list[1]['id'], user_list[1]['first_name'], user_list[1]['last_name'])
            mutual_friends = user1.search_for_mutual_friends(user2)
            print(f'{user1.full_name} и {user2.full_name} имеют следующих общих друзей: ')
            for id in mutual_friends:
                user = User(id)
                user.get_info()
                print(user.full_name)
                time.sleep(1)

main()


# Задача 2. Поиск общих друзей должен происходить с помощью оператора &, т.е. user1 & user2 должен выдать список общих друзей пользователей user1 и user2, в этом списке должны быть экземпляры классов.

class User_extended(User):
    def __and__(self,other):
        return self.search_for_mutual_friends(other)


def main_v1():
    while True:
        user_input = input('Введите двух пользователей vk через запятую или q для выхода: ')
        # Михаил Мед, Руслан Мазитов - можно использовать для проверки
        if user_input == 'q':
            break
        else:
            users = user_input.split(', ')
            user_list = search_user(users)
            user1 = User_extended(user_list[0]['id'], user_list[0]['first_name'], user_list[0]['last_name'])
            user2 = User_extended(user_list[1]['id'], user_list[1]['first_name'], user_list[1]['last_name'])
            mutual_friends = user1 & user2
            mutual_friend_list = []
            print(f'{user1.full_name} и {user2.full_name} имеют следующих общих друзей: ')
            for id in mutual_friends:
                user = User_extended(id)
                user.get_info()
                mutual_friend_list.append(user.full_name)
                time.sleep(1)
            print(mutual_friend_list)

main_v1()


# Задача 3. Вывод print(user) должен выводить ссылку на профиль пользователя в сети VK

class User_more_extended(User):
    def __str__(self):
        return f'https://vk.com/id{self.uid}'


def main_v2():
    while True:
        users = []
        users.append(input('Введите пользователя vk для получения ссылки на профиль или q для выхода: '))
        if users == ['q']:
            break
        else:
            user_info = search_user(users)
            user = User_more_extended(user_info[0]['id'], user_info[0]['first_name'], user_info[0]['last_name'])
            print(user.full_name, end=' ')
            print(user)

main_v2()